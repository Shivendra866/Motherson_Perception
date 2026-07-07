import cv2
import numpy as np
import pyrealsense2 as rs
from rfdetr import RFDETRSegPreview
from collections import deque
import math

# ==========================================
# MODEL
# ==========================================

MODEL_PATH = "/home/tecnical/Desktop/tail_detection/dome_seg.pth"

print("Loading model...")
model = RFDETRSegPreview.from_checkpoint(MODEL_PATH, num_classes=21)
try:
    model.optimize_for_inference()
except Exception:
    pass
print("Model loaded.")

# ==========================================
# REALSENSE WITH DEPTH
# ==========================================

pipeline = rs.pipeline()
config = rs.config()

# Enable both color and depth streams
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)
print("RealSense started with depth.")

# ==========================================
# ALIGN DEPTH TO COLOR
# ==========================================
align_to = rs.stream.color
align = rs.align(align_to)

# Get camera intrinsics for depth to 3D conversion
profile = pipeline.get_active_profile()
color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
intrinsics = color_profile.get_intrinsics()

CONFIDENCE_THRESHOLD = 0.5

# ==========================================
# ENHANCED STABILIZATION
# ==========================================
BUFFER_SIZE = 10
SMOOTHING_FACTOR = 0.3

keypoint_buffers = {
    'top': deque(maxlen=BUFFER_SIZE),
    'bottom': deque(maxlen=BUFFER_SIZE),
    'left': deque(maxlen=BUFFER_SIZE),
    'right': deque(maxlen=BUFFER_SIZE),
    'centroid': deque(maxlen=BUFFER_SIZE)
}

previous_keypoints = None

# ==========================================
# FUNCTIONS
# ==========================================

def get_object_border_keypoints(mask, frame_shape):
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    if mask.shape != (frame_shape[0], frame_shape[1]):
        mask = cv2.resize(mask, (frame_shape[1], frame_shape[0]))
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    
    contour = max(contours, key=cv2.contourArea)
    if len(contour) < 5:
        return None
    
    hull = cv2.convexHull(contour)
    
    top_idx = np.argmin(hull[:, 0, 1])
    bottom_idx = np.argmax(hull[:, 0, 1])
    left_idx = np.argmin(hull[:, 0, 0])
    right_idx = np.argmax(hull[:, 0, 0])
    
    top = tuple(hull[top_idx, 0])
    bottom = tuple(hull[bottom_idx, 0])
    left = tuple(hull[left_idx, 0])
    right = tuple(hull[right_idx, 0])
    
    M = cv2.moments(contour)
    if M['m00'] != 0:
        centroid = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
    else:
        centroid = ((top[0] + bottom[0] + left[0] + right[0]) // 4,
                    (top[1] + bottom[1] + left[1] + right[1]) // 4)
    
    return {'top': top, 'bottom': bottom, 'left': left, 'right': right,
            'centroid': centroid, 'contour': contour}

def smooth_keypoints(current):
    global previous_keypoints
    
    if current is None:
        return None
    
    smoothed = {}
    
    for key in ['top', 'bottom', 'left', 'right', 'centroid']:
        keypoint_buffers[key].append(current[key])
        
        if len(keypoint_buffers[key]) > 0:
            avg_x = int(sum([p[0] for p in keypoint_buffers[key]]) / len(keypoint_buffers[key]))
            avg_y = int(sum([p[1] for p in keypoint_buffers[key]]) / len(keypoint_buffers[key]))
            moving_avg = (avg_x, avg_y)
        else:
            moving_avg = current[key]
        
        if previous_keypoints is not None and key in previous_keypoints:
            prev_x, prev_y = previous_keypoints[key]
            smooth_x = int(SMOOTHING_FACTOR * moving_avg[0] + (1 - SMOOTHING_FACTOR) * prev_x)
            smooth_y = int(SMOOTHING_FACTOR * moving_avg[1] + (1 - SMOOTHING_FACTOR) * prev_y)
            smoothed[key] = (smooth_x, smooth_y)
        else:
            smoothed[key] = moving_avg
    
    smoothed['contour'] = current.get('contour', None)
    previous_keypoints = smoothed.copy()
    
    return smoothed

def get_3d_coordinates(depth_frame, pixel_x, pixel_y, intrinsics):
    """Convert pixel coordinates to 3D coordinates (X, Y, Z) in meters."""
    radius = 2
    depths = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            px = max(0, min(pixel_x + dx, depth_frame.width - 1))
            py = max(0, min(pixel_y + dy, depth_frame.height - 1))
            d = depth_frame.get_distance(px, py)
            if d > 0:
                depths.append(d)
    
    if not depths:
        return None
    
    depth = np.median(depths)
    
    if depth == 0:
        return None
    
    depth_point = rs.rs2_deproject_pixel_to_point(intrinsics, [pixel_x, pixel_y], depth)
    
    return {
        'x': depth_point[0],
        'y': depth_point[1],
        'z': depth_point[2],
        'depth_m': depth
    }

def distance_between_points(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def filter_outliers(keypoints, threshold=20):
    if keypoints is None or len(keypoints) < 2:
        return keypoints
    
    filtered = {}
    for key in ['top', 'bottom', 'left', 'right', 'centroid']:
        if key in keypoints:
            if previous_keypoints is not None and key in previous_keypoints:
                dist = distance_between_points(keypoints[key], previous_keypoints[key])
                if dist > threshold:
                    filtered[key] = previous_keypoints[key]
                else:
                    filtered[key] = keypoints[key]
            else:
                filtered[key] = keypoints[key]
    
    if 'contour' in keypoints:
        filtered['contour'] = keypoints['contour']
    
    return filtered

def print_coordinates_to_terminal(point_name, coords_3d, pixel_coords):
    """Print 3D coordinates to terminal in a formatted way."""
    if coords_3d:
        print(f"{point_name:8} | Pixel: ({pixel_coords[0]:4d}, {pixel_coords[1]:4d}) | "
              f"X: {coords_3d['x']:7.4f}m | Y: {coords_3d['y']:7.4f}m | Z: {coords_3d['z']:7.4f}m | "
              f"Depth: {coords_3d['depth_m']:7.4f}m")
    else:
        print(f"{point_name:8} | Pixel: ({pixel_coords[0]:4d}, {pixel_coords[1]:4d}) | "
              f"X: {'N/A':>7} | Y: {'N/A':>7} | Z: {'N/A':>7} | Depth: {'N/A':>7}")

# ==========================================
# MAIN LOOP
# ==========================================
try:
    frame_counter = 0
    print("\n" + "="*80)
    print("POINT COORDINATES (X, Y, Z in meters)")
    print("="*80)
    print(f"{'POINT':8} | {'PIXEL':12} | {'X':>10} | {'Y':>10} | {'Z':>10} | {'DEPTH':>10}")
    print("-"*80)
    
    while True:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        
        # Align depth to color
        aligned_frames = align.process(frames)
        
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        
        if not color_frame or not depth_frame:
            continue

        frame = np.asanyarray(color_frame.get_data())
        detections = model.predict(frame, threshold=CONFIDENCE_THRESHOLD)

        seg_mask_image = np.zeros_like(frame)
        annotated = frame.copy()

        if hasattr(detections, "mask"):
            masks = detections.mask
            if masks is not None:
                for mask in masks:
                    mask = mask.astype(np.uint8)
                    if mask.shape != (frame.shape[0], frame.shape[1]):
                        mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

                    seg_mask_image[:, :, 1] = cv2.bitwise_or(seg_mask_image[:, :, 1], mask * 255)

                    current_keypoints = get_object_border_keypoints(mask, frame.shape)
                    if current_keypoints is not None:
                        # Smooth keypoints
                        keypoints = smooth_keypoints(current_keypoints)
                        
                        # Filter outliers
                        keypoints = filter_outliers(keypoints, threshold=15)
                        
                        if keypoints is not None:
                            # ─── GET 3D COORDINATES FOR ALL POINTS ───
                            center_3d = get_3d_coordinates(
                                depth_frame, 
                                keypoints['centroid'][0], 
                                keypoints['centroid'][1], 
                                intrinsics
                            )
                            
                            top_3d = get_3d_coordinates(
                                depth_frame, 
                                keypoints['top'][0], 
                                keypoints['top'][1], 
                                intrinsics
                            )
                            
                            bottom_3d = get_3d_coordinates(
                                depth_frame, 
                                keypoints['bottom'][0], 
                                keypoints['bottom'][1], 
                                intrinsics
                            )
                            
                            left_3d = get_3d_coordinates(
                                depth_frame, 
                                keypoints['left'][0], 
                                keypoints['left'][1], 
                                intrinsics
                            )
                            
                            right_3d = get_3d_coordinates(
                                depth_frame, 
                                keypoints['right'][0], 
                                keypoints['right'][1], 
                                intrinsics
                            )
                            
                            # ─── PRINT COORDINATES TO TERMINAL ───
                            # Clear previous lines (optional - only print every frame)
                            # Uncomment the following line to clear terminal each frame
                            # os.system('clear' if os.name == 'posix' else 'cls')
                            
                            print("\033[F"*6, end="")  # Move cursor up 6 lines
                            print("\r" + " "*80)
                            print(f"{'POINT':8} | {'PIXEL':12} | {'X':>10} | {'Y':>10} | {'Z':>10} | {'DEPTH':>10}")
                            print("-"*80)
                            
                            print_coordinates_to_terminal("TOP", top_3d, keypoints['top'])
                            print_coordinates_to_terminal("BOTTOM", bottom_3d, keypoints['bottom'])
                            print_coordinates_to_terminal("LEFT", left_3d, keypoints['left'])
                            print_coordinates_to_terminal("RIGHT", right_3d, keypoints['right'])
                            print_coordinates_to_terminal("CENTER", center_3d, keypoints['centroid'])
                            print("-"*80)
                            
                            # ─── DRAW CONTOUR ───
                            cv2.drawContours(annotated, [keypoints['contour']], -1, (255, 255, 0), 1)
                            
                            # ─── DRAW POINTS ───
                            # 4 border points
                            cv2.circle(annotated, keypoints['top'], 6, (0, 255, 255), -1)
                            cv2.circle(annotated, keypoints['top'], 6, (255, 255, 255), 1)
                            
                            cv2.circle(annotated, keypoints['bottom'], 6, (255, 255, 0), -1)
                            cv2.circle(annotated, keypoints['bottom'], 6, (255, 255, 255), 1)
                            
                            cv2.circle(annotated, keypoints['left'], 6, (255, 0, 255), -1)
                            cv2.circle(annotated, keypoints['left'], 6, (255, 255, 255), 1)
                            
                            cv2.circle(annotated, keypoints['right'], 6, (0, 255, 0), -1)
                            cv2.circle(annotated, keypoints['right'], 6, (255, 255, 255), 1)
                            
                            # Center point
                            cv2.circle(annotated, keypoints['centroid'], 8, (0, 0, 255), -1)
                            cv2.circle(annotated, keypoints['centroid'], 8, (255, 255, 255), 1)
                            
                            # ─── DISPLAY 3D COORDINATES ON FRAME ───
                            y_offset = 0
                            coord_info = [
                                ("TOP", top_3d, (0, 255, 255)),
                                ("BOTTOM", bottom_3d, (255, 255, 0)),
                                ("LEFT", left_3d, (255, 0, 255)),
                                ("RIGHT", right_3d, (0, 255, 0)),
                                ("CENTER", center_3d, (0, 0, 255))
                            ]
                            
                            for name, coords, color in coord_info:
                                if coords:
                                    text = f"{name}: X:{coords['x']:.3f} Y:{coords['y']:.3f} Z:{coords['z']:.3f}m"
                                    cv2.putText(annotated, text,
                                        (10, 90 + y_offset),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                                    y_offset += 20
                            
                            # ─── DIAMOND ───
                            cv2.line(annotated, keypoints['top'], keypoints['right'], (200, 200, 200), 1)
                            cv2.line(annotated, keypoints['right'], keypoints['bottom'], (200, 200, 200), 1)
                            cv2.line(annotated, keypoints['bottom'], keypoints['left'], (200, 200, 200), 1)
                            cv2.line(annotated, keypoints['left'], keypoints['top'], (200, 200, 200), 1)

        # Bounding box only (no labels)
        if len(detections) > 0:
            for i in range(len(detections)):
                box = detections.xyxy[i]
                conf = float(detections.confidence[i])
                if conf < CONFIDENCE_THRESHOLD:
                    continue
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 1)

        # Minimal info
        cv2.putText(annotated, f"Objects: {len(detections)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(annotated, f"Buffer: {BUFFER_SIZE}", (10, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

        # Show depth map
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(np.asanyarray(depth_frame.get_data()), alpha=0.03), 
            cv2.COLORMAP_JET
        )

        cv2.imshow("Detection with 3D", annotated)
        cv2.imshow("Segmentation Mask", seg_mask_image)
        cv2.imshow("Depth Map", depth_colormap)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('+'):
            BUFFER_SIZE = min(20, BUFFER_SIZE + 1)
            print(f"Buffer size: {BUFFER_SIZE}")
        elif key == ord('-'):
            BUFFER_SIZE = max(2, BUFFER_SIZE - 1)
            print(f"Buffer size: {BUFFER_SIZE}")

finally:
    pipeline.stop()
    cv2.destroyAllWindows()