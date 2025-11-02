import os
import subprocess
import time
from pyngrok import ngrok

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banbas_resort.settings')

def run_django_server():
    print("Starting Django development server...")
    subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])

def run_ngrok():
    print("Starting ngrok tunnel...")
    # Wait for Django server to start (you might need a more robust check)
    time.sleep(5) 
    
    ngrok.set_auth_token("34nRJlsPBNiWK0sutXBrTqKiCk1_3RecZ8yA5mf7BNcFagttT") # Replace with your actual ngrok authtoken
    
    # Connect to ngrok
    tunnel = ngrok.connect(8000)
    public_url = tunnel.public_url
    print(f"Ngrok tunnel established at: {public_url}")
    
    # Keep the ngrok tunnel alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down ngrok tunnel.")
        ngrok.disconnect(public_url)
        ngrok.kill()

if __name__ == "__main__":
    import threading

    django_thread = threading.Thread(target=run_django_server)
    django_thread.daemon = True  # Allow main program to exit even if thread is still running
    django_thread.start()

    run_ngrok()
