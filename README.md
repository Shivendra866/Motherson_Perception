# Motherson Perception

Real-time Tail Lamp / Dome Segmentation using RF-DETR Segmentation and Intel RealSense.

This project performs:

- Real-time segmentation using a trained RF-DETR Segmentation model
- Intel RealSense RGB + Depth streaming
- 3D coordinate estimation (X, Y, Z)
- Object boundary keypoint extraction
- Segmentation mask visualization
- Bounding box visualization
- Depth map visualization
- Keypoint smoothing for stable measurements

---

## Project Structure

```
Motherson_Perception/
│
├── app.py                     # Main application
├── dome_seg.py                # Dome segmentation script
├── TailLamp_seg.py            # Tail lamp segmentation script
├── dome_seg.pth               # Dome RF-DETR model
├── TailLamp_seg.pth           # Tail Lamp RF-DETR model
├── requirements.txt
└── README.md
```

---

## Features

- RF-DETR Segmentation inference
- Intel RealSense RGB + Depth support
- Automatic depth alignment
- 3D coordinate estimation
- Border keypoint extraction
    - Top
    - Bottom
    - Left
    - Right
    - Center
- Temporal smoothing
- Outlier filtering
- Live visualization
- Depth map visualization

---

## Requirements

- Ubuntu 22.04 (recommended)
- Python 3.10+
- Intel RealSense SDK
- CUDA-enabled GPU (recommended)
- Intel RealSense Camera (D455/D435)

---

## Installation

### Clone repository

```bash
git clone <repository_url>
cd Motherson_Perception
```

### Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Install Intel RealSense SDK

Install librealsense following Intel's official guide.

Verify installation:

```bash
realsense-viewer
```

---

## Running the Project

Run the application:

```bash
python app.py
```

or

```bash
python TailLamp_seg.py
```

or

```bash
python dome_seg.py
```

---

## Output Windows

The application opens three windows:

- Detection with 3D
- Segmentation Mask
- Depth Map

---

## Keyboard Controls

| Key | Function |
|------|----------|
| q | Quit application |
| + | Increase smoothing buffer |
| - | Decrease smoothing buffer |

---

## 3D Coordinate Output

For every detected object, the following points are computed:

- Top
- Bottom
- Left
- Right
- Center

Each point outputs:

- Pixel Coordinate
- X (meters)
- Y (meters)
- Z (meters)
- Depth

Example:

```
POINT      PIXEL          X          Y          Z       DEPTH
TOP      (320,120)   -0.0241   -0.0562    0.4821    0.4821
CENTER   (318,240)   -0.0012    0.0034    0.4788    0.4788
```

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Intel RealSense SDK
- RF-DETR Segmentation
- PyTorch

---

## Model

The project uses trained RF-DETR Segmentation models:

- `TailLamp_seg.pth`
- `dome_seg.pth`

These models perform semantic segmentation of the target object.

---

## Notes

- Update the model path inside the Python file before running.
- Ensure Intel RealSense camera is connected.
- CUDA is recommended for real-time inference.

---

## License

For internal development and research purposes.
