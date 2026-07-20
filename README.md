# IVCANSniffer v1.3.0

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

This project is a desktop application that filters and visualizes telemetry data received from a serial port in real time. It is designed to provide smooth, high-performance monitoring of sensor metrics.

## 🚀 Features

* **Real-Time Telemetry:** Monitors and visualizes incoming serial data instantaneously without UI blocking.
* **Modular Widget System:** Features dedicated custom components for critical system data:
  * Speedometer & Gauge displays
  * Thermometer & Altitude bars
* **Advanced Data Filtering:** Custom filter widgets to manage, parse, and process raw serial data packets efficiently.
* **Safe Data Parsing:** Built-in fail-safes for incomplete data packets to prevent application crashes during signal loss.

## 🛠️ Technologies Used

* **Language:** Python 3.13
* **GUI Framework:** PySide6
* **Hardware Communication:** PySerial
* **Version Control:** Git

## ⚙️ Installation & Setup

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/yigit-arda/IVCANSniffer.git
cd IVCANSniffer
```

### 2. Create and Activate a Virtual Environment
**For Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Linux Specific Requirement (Serial Port Permissions)
If you are running this on a Linux distribution, you might need permission to access the serial ports (`/dev/ttyUSB0`, etc.). Run the following command and **reboot** to apply changes:
```bash
sudo usermod -a -G dialout $USER
```

### 5. Run the Application
**For Linux:**
```bash
python3 ui_main.py
```
**For Windows:**
```bash
python ui_main.py
```
## 📦 Building the Executable (.exe) for Windows

If you want to compile the Python source code into a standalone Windows executable, follow these release steps:

### 1. Update the Version Title
Before building, open `ui_main.py` and update the window title to reflect your new version number:
```python
self.setWindowTitle("IVCANSniffer-v1.x.x")
```

### 2. Clean Previous Build Artifacts
To prevent conflicts and oversized files, delete any existing `build/` folder, `dist/` folder, and `.spec` files from your project's root directory.

### 3. Run PyInstaller
Ensure your virtual environment `(venv)` is activated, then run the following command to generate the executable:
```bash
pyinstaller --onefile --windowed --name "IVCANSniffer_v1.x.x" ui_main.py
```
*(Remember to replace `v1.x.x` with your actual version number).*

Once the process completes successfully, your new standalone executable will be located inside the newly generated `dist/` folder.
