import socket
import os
from dotenv import load_dotenv

load_dotenv()

def check_port():
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", 3306))
    
    print(f"--- Local Network Connectivity Test ---")
    print(f"Targeting: {host}:{port}")
    
    # Check DNS
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS Resolved: {host} -> {ip}")
    except Exception as e:
        print(f"❌ DNS Resolution Failed: {e}")
        return

    # Check TCP Connection
    print(f"Testing TCP connection to {ip}:{port}...")
    try:
        s = socket.create_connection((ip, port), timeout=10)
        print(f"✅ SUCCESS: Port {port} is OPEN and reachable!")
        s.close()
    except socket.timeout:
        print(f"❌ FAILED: Connection Timed Out (10060).")
        print("This usually means your Wi-Fi, Router, or ISP is blocking the port.")
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    check_port()
