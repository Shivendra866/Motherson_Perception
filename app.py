import streamlit as st
import cv2
import numpy as np
from PIL import Image
import torch
import gc
from rfdetr import RFDETRSegPreview
import math
import os

# ==========================================
# MEMORY OPTIMIZATION
# ==========================================
# Set PyTorch memory configuration
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

# Force PyTorch to use memory efficiently
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="RF-DETR Segmentation Demo",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 RF-DETR Segmentation & Detection")
st.markdown("Upload an image to perform object detection and segmentation")

# ==========================================
# MODEL LOADING WITH MEMORY OPTIMIZATION
# ==========================================
@st.cache_resource
def load_model():
    MODEL_PATH = "/home/tecnical/Desktop/tail_detection/dome_seg.pth"
    
    with st.spinner("Loading model... This may take a moment."):
        try:
            # Clear GPU cache before loading
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Load model with memory optimization
            model = RFDETRSegPreview.from_checkpoint(
                MODEL_PATH, 
                num_classes=21,
                device="cuda" if torch.cuda.is_available() else "cpu"
            )
            
            # RF-DETR model doesn't need explicit eval() - it's handled internally
            
            # Optimize for inference
            try:
                model.optimize_for_inference()
            except Exception as e:
                st.warning(f"Optimization skipped: {str(e)}")
            
            # Force memory cleanup
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            st.success("Model loaded successfully!")
            return model
            
        except Exception as e:
            st.error(f"Failed to load model: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return None

model = load_model()

if model is None:
    st.stop()

# ==========================================
# FUNCTIONS
# ==========================================
CONFIDENCE_THRESHOLD = 0.5

def get_object_border_keypoints(mask, frame_shape):
    """Extract border keypoints from segmentation mask."""
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
    
    return {
        'top': top, 
        'bottom': bottom, 
        'left': left, 
        'right': right,
        'centroid': centroid, 
        'contour': contour
    }

def resize_image(image, max_size=800):
    """Resize image to reduce memory usage."""
    h, w = image.shape[:2]
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h))
    return image

def process_image(image, model):
    """Process image with RF-DETR model with memory optimization."""
    # Convert PIL to numpy
    if isinstance(image, Image.Image):
        frame = np.array(image)
    else:
        frame = image.copy()
    
    # Resize image to reduce memory usage
    frame = resize_image(frame, max_size=800)
    
    # Clear GPU cache before inference
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()
    
    # Run inference with lower memory usage
    try:
        with torch.no_grad():
            detections = model.predict(
                frame, 
                threshold=CONFIDENCE_THRESHOLD
            )
    except Exception as e:
        st.error(f"Inference error: {str(e)}")
        return frame, np.zeros_like(frame), None, []
    
    # Clear GPU cache after inference
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()
    
    # Create annotated image
    annotated = frame.copy()
    seg_mask_image = np.zeros_like(frame)
    
    # Process masks
    keypoints_list = []
    if hasattr(detections, "mask"):
        masks = detections.mask
        if masks is not None:
            # Limit number of masks processed to reduce memory
            max_masks = min(len(masks), 10)
            for idx in range(max_masks):
                mask = masks[idx].astype(np.uint8)
                if mask.shape != (frame.shape[0], frame.shape[1]):
                    mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                
                seg_mask_image[:, :, 1] = cv2.bitwise_or(seg_mask_image[:, :, 1], mask * 255)
                
                current_keypoints = get_object_border_keypoints(mask, frame.shape)
                if current_keypoints is not None:
                    keypoints_list.append(current_keypoints)
                    
                    # Draw contour
                    cv2.drawContours(annotated, [current_keypoints['contour']], -1, (255, 255, 0), 2)
                    
                    # Draw border points
                    cv2.circle(annotated, current_keypoints['top'], 6, (0, 255, 255), -1)
                    cv2.circle(annotated, current_keypoints['bottom'], 6, (255, 255, 0), -1)
                    cv2.circle(annotated, current_keypoints['left'], 6, (255, 0, 255), -1)
                    cv2.circle(annotated, current_keypoints['right'], 6, (0, 255, 0), -1)
                    cv2.circle(annotated, current_keypoints['centroid'], 8, (0, 0, 255), -1)
                    
                    # Draw diamond connections
                    cv2.line(annotated, current_keypoints['top'], current_keypoints['right'], (200, 200, 200), 1)
                    cv2.line(annotated, current_keypoints['right'], current_keypoints['bottom'], (200, 200, 200), 1)
                    cv2.line(annotated, current_keypoints['bottom'], current_keypoints['left'], (200, 200, 200), 1)
                    cv2.line(annotated, current_keypoints['left'], current_keypoints['top'], (200, 200, 200), 1)
                    
                    # Add labels
                    cv2.putText(annotated, "Top", 
                               (current_keypoints['top'][0] - 20, current_keypoints['top'][1] - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                    cv2.putText(annotated, "Bottom", 
                               (current_keypoints['bottom'][0] - 30, current_keypoints['bottom'][1] + 15),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
                    cv2.putText(annotated, "Left", 
                               (current_keypoints['left'][0] - 30, current_keypoints['left'][1]),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)
                    cv2.putText(annotated, "Right", 
                               (current_keypoints['right'][0] + 5, current_keypoints['right'][1]),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                    cv2.putText(annotated, "Center", 
                               (current_keypoints['centroid'][0] + 10, current_keypoints['centroid'][1]),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    
    # Draw bounding boxes
    if len(detections) > 0:
        for i in range(min(len(detections), 10)):  # Limit number of boxes drawn
            box = detections.xyxy[i]
            conf = float(detections.confidence[i])
            if conf < CONFIDENCE_THRESHOLD:
                continue
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Confidence label
            label = f"Class {detections.class_id[i] if hasattr(detections, 'class_id') else 'Object'} {conf:.2f}"
            cv2.putText(annotated, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return annotated, seg_mask_image, detections, keypoints_list

# ==========================================
# SIDEBAR - SETTINGS
# ==========================================
with st.sidebar:
    st.header("⚙️ Settings")
    confidence = st.slider("Confidence Threshold", 0.1, 1.0, 0.5, 0.05)
    CONFIDENCE_THRESHOLD = confidence
    
    image_size = st.slider("Max Image Size", 400, 1200, 800, 100, 
                           help="Reduce size to save memory")
    
    # Update the resize function to use the slider value
    def process_image_with_size(image, model, max_size):
        # Convert PIL to numpy
        if isinstance(image, Image.Image):
            frame = np.array(image)
        else:
            frame = image.copy()
        
        # Resize image based on slider
        frame = resize_image(frame, max_size=max_size)
        
        # Clear GPU cache before inference
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
        
        # Run inference
        try:
            with torch.no_grad():
                detections = model.predict(
                    frame, 
                    threshold=CONFIDENCE_THRESHOLD
                )
        except Exception as e:
            st.error(f"Inference error: {str(e)}")
            return frame, np.zeros_like(frame), None, []
        
        # Clear GPU cache after inference
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
        
        # Create annotated image
        annotated = frame.copy()
        seg_mask_image = np.zeros_like(frame)
        
        # Process masks
        keypoints_list = []
        if hasattr(detections, "mask"):
            masks = detections.mask
            if masks is not None:
                max_masks = min(len(masks), 10)
                for idx in range(max_masks):
                    mask = masks[idx].astype(np.uint8)
                    if mask.shape != (frame.shape[0], frame.shape[1]):
                        mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                    
                    seg_mask_image[:, :, 1] = cv2.bitwise_or(seg_mask_image[:, :, 1], mask * 255)
                    
                    current_keypoints = get_object_border_keypoints(mask, frame.shape)
                    if current_keypoints is not None:
                        keypoints_list.append(current_keypoints)
                        
                        # Draw contour
                        cv2.drawContours(annotated, [current_keypoints['contour']], -1, (255, 255, 0), 2)
                        
                        # Draw border points
                        cv2.circle(annotated, current_keypoints['top'], 6, (0, 255, 255), -1)
                        cv2.circle(annotated, current_keypoints['bottom'], 6, (255, 255, 0), -1)
                        cv2.circle(annotated, current_keypoints['left'], 6, (255, 0, 255), -1)
                        cv2.circle(annotated, current_keypoints['right'], 6, (0, 255, 0), -1)
                        cv2.circle(annotated, current_keypoints['centroid'], 8, (0, 0, 255), -1)
                        
                        # Draw diamond connections
                        cv2.line(annotated, current_keypoints['top'], current_keypoints['right'], (200, 200, 200), 1)
                        cv2.line(annotated, current_keypoints['right'], current_keypoints['bottom'], (200, 200, 200), 1)
                        cv2.line(annotated, current_keypoints['bottom'], current_keypoints['left'], (200, 200, 200), 1)
                        cv2.line(annotated, current_keypoints['left'], current_keypoints['top'], (200, 200, 200), 1)
                        
                        # Add labels
                        cv2.putText(annotated, "Top", 
                                   (current_keypoints['top'][0] - 20, current_keypoints['top'][1] - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                        cv2.putText(annotated, "Bottom", 
                                   (current_keypoints['bottom'][0] - 30, current_keypoints['bottom'][1] + 15),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
                        cv2.putText(annotated, "Left", 
                                   (current_keypoints['left'][0] - 30, current_keypoints['left'][1]),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)
                        cv2.putText(annotated, "Right", 
                                   (current_keypoints['right'][0] + 5, current_keypoints['right'][1]),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                        cv2.putText(annotated, "Center", 
                                   (current_keypoints['centroid'][0] + 10, current_keypoints['centroid'][1]),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        
        # Draw bounding boxes
        if len(detections) > 0:
            for i in range(min(len(detections), 10)):
                box = detections.xyxy[i]
                conf = float(detections.confidence[i])
                if conf < CONFIDENCE_THRESHOLD:
                    continue
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                label = f"Class {detections.class_id[i] if hasattr(detections, 'class_id') else 'Object'} {conf:.2f}"
                cv2.putText(annotated, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return annotated, seg_mask_image, detections, keypoints_list
    
    st.divider()
    st.header("📊 Detection Info")
    detection_count = st.empty()
    keypoint_count = st.empty()
    
    st.divider()
    st.header("💡 Instructions")
    st.markdown("""
    1. Upload an image using the file uploader
    2. Adjust confidence threshold if needed
    3. View detection results with:
       - Bounding boxes
       - Segmentation masks
       - Key points (Top, Bottom, Left, Right, Center)
       - Diamond connections
    """)
    
    st.divider()
    st.header("🔧 Memory Info")
    if torch.cuda.is_available():
        total_mem = torch.cuda.get_device_properties(0).total_memory / 1e9
        allocated = torch.cuda.memory_allocated(0) / 1e9
        cached = torch.cuda.memory_reserved(0) / 1e9
        st.write(f"Total: {total_mem:.2f} GB")
        st.write(f"Allocated: {allocated:.2f} GB")
        st.write(f"Cached: {cached:.2f} GB")
        
        # Memory clear button
        if st.button("Clear GPU Memory"):
            torch.cuda.empty_cache()
            gc.collect()
            st.success("GPU memory cleared!")
            st.rerun()
    else:
        st.info("Running on CPU")

# ==========================================
# MAIN CONTENT
# ==========================================

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
    help="Upload an image for object detection and segmentation"
)

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Original Image")
        st.image(image, use_container_width=True)
    
    # Process image with memory management
    with st.spinner("Processing image..."):
        try:
            # Use the image size from slider
            annotated, seg_mask, detections, keypoints = process_image_with_size(
                image, model, image_size
            )
            
            # Update info
            num_detections = len(detections) if detections is not None else 0
            detection_count.metric("Detections", num_detections)
            keypoint_count.metric("Objects with Keypoints", len(keypoints))
            
            # Convert to RGB for display
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            seg_mask_rgb = cv2.cvtColor(seg_mask, cv2.COLOR_BGR2RGB)
            
            with col2:
                st.subheader("🎯 Detection Result")
                st.image(annotated_rgb, use_container_width=True)
            
            # Display additional visualizations
            st.divider()
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("🎨 Segmentation Mask")
                st.image(seg_mask_rgb, use_container_width=True)
                
                # Show overlay
                if annotated.shape[0] > 0 and annotated.shape[1] > 0:
                    overlay = cv2.addWeighted(
                        cv2.cvtColor(np.array(image.resize((annotated.shape[1], annotated.shape[0]))), 
                                    cv2.COLOR_RGB2BGR), 
                        0.6, seg_mask, 0.4, 0
                    )
                    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
                    st.subheader("🔄 Overlay")
                    st.image(overlay_rgb, use_container_width=True)
            
            with col4:
                st.subheader("📋 Detection Details")
                
                if len(detections) > 0:
                    # Create a table of detections
                    detection_data = []
                    for i in range(min(len(detections), 10)):
                        conf = float(detections.confidence[i])
                        if conf < CONFIDENCE_THRESHOLD:
                            continue
                        box = detections.xyxy[i]
                        class_id = detections.class_id[i] if hasattr(detections, 'class_id') else 'N/A'
                        detection_data.append({
                            "Class": class_id,
                            "Confidence": f"{conf:.2f}",
                            "BBox": f"[{box[0]:.0f}, {box[1]:.0f}, {box[2]:.0f}, {box[3]:.0f}]"
                        })
                    
                    if detection_data:
                        st.dataframe(detection_data, use_container_width=True)
                    else:
                        st.info("No detections above confidence threshold")
                else:
                    st.info("No detections found")
                
                # Keypoints information
                if keypoints:
                    st.subheader("📍 Keypoints")
                    for i, kp in enumerate(keypoints):
                        st.write(f"**Object {i+1}:**")
                        st.write(f"- Top: {kp['top']}")
                        st.write(f"- Bottom: {kp['bottom']}")
                        st.write(f"- Left: {kp['left']}")
                        st.write(f"- Right: {kp['right']}")
                        st.write(f"- Center: {kp['centroid']}")
                        st.divider()
            
            # Clear memory after processing
            del annotated, seg_mask, detections, keypoints
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
                
        except torch.cuda.OutOfMemoryError as e:
            st.error(f"Out of memory! Try reducing the image size or closing other applications.")
            st.error(f"Error details: {str(e)}")
            
            # Clear memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            # Suggest solution
            st.info("💡 Try reducing the 'Max Image Size' in the sidebar settings")
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()

else:
    # Show placeholder when no image uploaded
    st.info("👆 Upload an image to get started")
    
    # Display sample instructions
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 📤 Upload
        Upload an image using the file uploader above
        """)
    with col2:
        st.markdown("""
        ### 🎯 Detect
        The model will detect objects and generate segmentation masks
        """)
    with col3:
        st.markdown("""
        ### 📊 Analyze
        View detection results, keypoints, and detailed information
        """)

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("RF-DETR Segmentation Demo | Powered by Streamlit")

# Periodic memory cleanup
def cleanup():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

# Register cleanup on page refresh
import atexit
atexit.register(cleanup)