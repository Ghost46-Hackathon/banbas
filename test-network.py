#!/usr/bin/env python
"""
Network connectivity test script for Django server
"""
import socket
import subprocess
import sys
import time
from threading import Thread

def get_local_ip():
    """Get local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def check_port_listening(host, port):
    """Check if a port is listening"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

def start_django_server():
    """Start Django server in background"""
    try:
        cmd = [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def main():
    local_ip = get_local_ip()
    port = 8000
    
    print("=" * 60)
    print("BANBAS RESORT - Network Connectivity Test")
    print("=" * 60)
    print(f"Your IP Address: {local_ip}")
    print(f"Server Port: {port}")
    print()
    
    # Test 1: Check if port is already in use
    print("Test 1: Checking if port 8000 is available...")
    if check_port_listening("127.0.0.1", port):
        print("✓ Port 8000 is already in use (server might be running)")
    else:
        print("✓ Port 8000 is available")
    
    print()
    
    # Test 2: Start server and test
    print("Test 2: Starting Django server...")
    server_process = start_django_server()
    
    if server_process:
        print("✓ Django server started")
        
        # Wait for server to start
        print("Waiting 3 seconds for server to initialize...")
        time.sleep(3)
        
        # Test local connections
        print("\nTest 3: Testing local connections...")
        
        test_urls = [
            ("localhost", "http://127.0.0.1:8000/"),
            ("local IP", f"http://{local_ip}:8000/"),
        ]
        
        for name, url in test_urls:
            host = url.split("://")[1].split(":")[0]
            if check_port_listening(host, port):
                print(f"✓ {name} connection: {url} - ACCESSIBLE")
            else:
                print(f"✗ {name} connection: {url} - NOT ACCESSIBLE")
        
        print(f"\nNetwork Access URLs:")
        print(f"  • Local: http://127.0.0.1:{port}/")
        print(f"  • Network: http://{local_ip}:{port}/")
        print(f"  • Admin: http://{local_ip}:{port}/admin/")
        
        print(f"\n🔧 If not accessible from other devices:")
        print(f"  1. Check Windows Firewall (allow Python)")
        print(f"  2. Ensure devices are on same network")
        print(f"  3. Try: ping {local_ip} from another device")
        print(f"  4. See NETWORK_TROUBLESHOOTING.md for detailed help")
        
        # Stop server
        print(f"\nStopping test server...")
        server_process.terminate()
        server_process.wait()
        print("✓ Server stopped")
        
    else:
        print("✗ Failed to start Django server")
    
    print("\n" + "=" * 60)
    print("Test completed. Run 'python manage.py runserver 0.0.0.0:8000' to start normally.")

if __name__ == "__main__":
    main()