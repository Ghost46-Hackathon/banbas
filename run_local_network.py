#!/usr/bin/env python
"""
Script to run Django development server accessible from local network.
This allows other devices on your network to access the website.
"""

import os
import sys
import subprocess
import socket

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use Google's DNS server to determine route
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"

def main():
    # Add the project directory to Python path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banbas_resort.settings')
    
    # Get local IP address
    local_ip = get_local_ip()
    port = 8000
    
    print("=" * 60)
    print("🏨 BANBAS RESORT - Django Development Server")
    print("=" * 60)
    print(f"🌐 Your local IP address: {local_ip}")
    print(f"🚀 Starting server on port {port}")
    print()
    print("📱 Access the website from any device on your network:")
    print(f"   • Local: http://127.0.0.1:{port}/")
    print(f"   • Network: http://{local_ip}:{port}/")
    print(f"   • Admin: http://{local_ip}:{port}/admin/")
    print()
    print("🔧 Make sure your firewall allows connections on port", port)
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        # Run Django development server on all interfaces
        subprocess.run([
            sys.executable, 
            "manage.py", 
            "runserver", 
            f"0.0.0.0:{port}"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()