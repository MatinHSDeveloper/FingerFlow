# 🖐️ FingerFlow

**Control your computer with your finger — no physical mouse required.**

FingerFlow is a Python-based air mouse that uses your computer's camera and real-time hand tracking to control the mouse cursor and perform clicks using simple hand gestures.

## ✨ Features

* 🖐️ Real-time hand tracking
* 🖱️ Move the mouse using your index finger
* 👆 Left click using a pinch gesture
* ✌️ Right click using a two-finger pinch gesture
* 🎯 Screen calibration for better accuracy
* 🎥 Uses your computer's camera
* ⚡ Real-time processing
* 🔘 Enable/disable mouse control with `F8`
* 🛑 Exit instantly with `ESC`
* 💻 Designed for Windows

## 🎮 Gestures

| Gesture                 | Action      |
| ----------------------- | ----------- |
| ☝️ Index finger         | Move cursor |
| 🤏 Thumb + index finger | Left click  |
| ✌️ + 🤏                 | Right click |

## ⌨️ Controls

| Key   | Action                         |
| ----- | ------------------------------ |
| `C`   | Start calibration              |
| `F8`  | Enable / Disable mouse control |
| `ESC` | Exit FingerFlow                |

## 🛠️ Requirements

* Windows
* Python 3.8
* A working camera
* OpenCV
* MediaPipe
* NumPy
* PyAutoGUI

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/MatinHSDeveloper/FingerFlow.git
cd FingerFlow
```

Install the required packages:

```bash
pip install opencv-python mediapipe numpy pyautogui
```

## ▶️ Run

Start FingerFlow with:

```bash
python main.py
```

After launching:

1. Make sure your camera is available.
2. Place your hand in front of the camera.
3. Use your index finger to control the cursor.
4. Pinch your thumb and index finger to left-click.
5. Use the two-finger gesture for right-click.
6. Press `C` if you need to recalibrate the screen.

## 🎯 Calibration

Calibration allows FingerFlow to map the camera's coordinate system to your screen more accurately.

Press:

```text
C
```

Then point your index finger at each target shown on the screen and keep it steady until the next target appears.

## 🔐 Privacy

FingerFlow processes the camera feed locally on your computer.

The project does not require uploading camera frames to an external server.

## 🚧 Project Status

**Version 1.0.0 — Initial Release**

FingerFlow is currently focused on basic air-mouse functionality.

Future versions may introduce additional gestures and system controls.

## 🗺️ Roadmap

* [x] Hand tracking
* [x] Cursor movement
* [x] Left click
* [x] Right click
* [x] Screen calibration
* [x] Windows support
* [ ] Double click gesture
* [ ] Drag & drop gesture
* [ ] Scroll gesture
* [ ] Custom gesture configuration
* [ ] Settings interface
* [ ] Standalone `.exe` release

## 🤝 Contributing

Contributions, suggestions, bug reports, and feature requests are welcome.

If you find a bug, please open an issue with:

* Windows version
* Python version
* Camera model
* Error message
* Steps to reproduce the issue

## 📄 License

Copyright © 2026 Matin Haji Seftjani.

This project is provided for personal, educational, and development purposes.

See the `LICENSE` file for the complete license terms.

---

**FingerFlow**
*Control beyond touch.*
