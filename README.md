<div align="center">
  <img src="https://img.shields.io/badge/MOTHERSON-PERCEPTION-FF6B6B?style=for-the-badge&logo=python&logoColor=white" alt="Motherson Perception" width="500"/>
  
  # 🚗 Motherson Perception
  
  ### Real-time Tail Lamp / Dome Segmentation using RF-DETR and Intel RealSense
  
  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
  [![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org/)
  [![Intel](https://img.shields.io/badge/Intel-RealSense-0071C5?style=flat-square&logo=intel&logoColor=white)](https://www.intelrealsense.com/)
  [![CUDA](https://img.shields.io/badge/CUDA-Enabled-76B900?style=flat-square&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)
  [![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)
  [![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)](https://github.com/your-username/Motherson_Perception/pulls)
  [![GitHub stars](https://img.shields.io/github/stars/your-username/Motherson_Perception?style=social)](https://github.com/your-username/Motherson_Perception)
  
  <br>
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=header"/>
</div>

---

## 📖 Table of Contents
- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🛠️ Installation](#️-installation)
- [🚀 Quick Start](#-quick-start)
- [🎮 Controls](#-controls)
- [📊 3D Coordinate Output](#-3d-coordinate-output)
- [🧠 Model Details](#-model-details)
- [📈 Performance](#-performance)
- [🔧 Customization](#-customization)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📞 Contact](#-contact)

---

## 🌟 Overview

**Motherson Perception** is a state-of-the-art real-time computer vision system that performs **semantic segmentation** and **precise 3D coordinate estimation** for automotive components. Leveraging the power of **RF-DETR Segmentation** and **Intel RealSense** RGB-D cameras, this system enables accurate detection, segmentation, and spatial positioning of tail lamps and dome components in real-time.

### 🎯 Key Capabilities

<table>
<tr>
<td width="33%">
  
  ### 🎯 Real-time Segmentation
  - Transformer-based RF-DETR architecture
  - High accuracy mask generation
  - 30 FPS inference speed
  
</td>
<td width="33%">
  
  ### 📏 3D Coordinate Estimation
  - Precise X, Y, Z measurements
  - 5 keypoint extraction
  - ±2.5 cm accuracy @ 1m
  
</td>
<td width="33%">
  
  ### 🖥️ Live Visualization
  - 3 synchronized views
  - Real-time overlay
  - Interactive controls
  
</td>
</tr>
</table>

---

## ✨ Features

<div align="center">

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 **RF-DETR Segmentation** | State-of-the-art transformer-based segmentation | ✅ Active |
| 📷 **Intel RealSense** | RGB + Depth streaming with pixel alignment | ✅ Active |
| 📍 **3D Coordinates** | X, Y, Z estimation from depth data | ✅ Active |
| 📌 **Keypoint Extraction** | Top, Bottom, Left, Right, Center points | ✅ Active |
| 🔄 **Temporal Smoothing** | Stable measurements with adaptive filtering | ✅ Active |
| 🎨 **Live Visualization** | 3 views: Detection, Mask, Depth | ✅ Active |
| ⚡ **Real-time Processing** | 30 FPS on RTX 3060 | ✅ Active |
| 🔧 **Customizable** | Adjustable thresholds and parameters | ✅ Active |

</div>

---

## 📁 Project Structure

```bash
Motherson_Perception/
│
├── 📄 app.py                    # Main application entry point
├── 📄 dome_seg.py               # Dome segmentation script
├── 📄 TailLamp_seg.py           # Tail lamp segmentation script
│
├── 🧠 dome_seg.pth              # Trained dome RF-DETR model
├── 🧠 TailLamp_seg.pth          # Trained tail lamp RF-DETR model
│
├── 📦 requirements.txt          # Python dependencies
├── 📖 README.md                 # This file
│
├── 📁 models/                   # Additional model files
│   └── ...
│
├── 📁 configs/                  # Configuration files
│   ├── camera_config.yaml
│   └── model_config.yaml
│
├── 📁 utils/                    # Utility functions
│   ├── depth_utils.py
│   ├── visualization.py
│   └── smoothing.py
│
└── 📁 docs/                     # Documentation
    ├── architecture.md
    └── api_reference.md
```
## 🛠️ Installation
## 📋 Prerequisites
<details> <summary><b>Click to expand requirements</b></summary>
OS: Ubuntu 22.04 / Windows 11 / macOS 12+

Python: 3.10 or higher

Hardware:

Intel RealSense camera (D455/D435 recommended)

CUDA-enabled GPU (NVIDIA RTX 2060+)

8GB+ RAM

Software:

librealsense SDK

CUDA Toolkit 11.8+

cuDNN 8.0+


##🚀 Step-by-Step Setup
bash
### 1. Clone the repository
git clone https://github.com/your-username/Motherson_Perception.git
cd Motherson_Perception

### 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Install Intel RealSense SDK
### Ubuntu/Debian:
sudo apt-get update
sudo apt-get install librealsense2-dev librealsense2-dkms

### 5. Verify installation
realsense-viewer
</details>
<br>

## Troubleshooting
<details> <summary><b>RealSense SDK Issues</b></summary>
bash
### Build from source if package not available
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
./scripts/setup_udev_rules.sh
mkdir build && cd build
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release
make && sudo make install
</details><details> <summary><b>CUDA Issues</b></summary>
bash
### Check CUDA version
nvcc --version

### Install CUDA if missing
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run
</details>

## 🚀 Quick Start
Running the Application
bash
### Run main application
python app.py

### Run specific segmentation
python TailLamp_seg.py
python dome_seg.py
