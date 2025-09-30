# Network Access Troubleshooting

If you can't access the Django server from other devices on your network, follow these steps:

## Your Network Details
- **Your PC IP**: `10.10.152.117`
- **Server Port**: `8000`
- **Network Access URL**: `http://10.10.152.117:8000/`

## Step 1: Start Server Correctly
```bash
# Make sure to use 0.0.0.0 to listen on all interfaces
python manage.py runserver 0.0.0.0:8000

# OR use the batch file
run-network.bat
```

## Step 2: Check Windows Firewall
### Option A: Windows Defender Firewall GUI
1. Open **Windows Defender Firewall**
2. Click **Allow an app or feature through Windows Defender Firewall**
3. Click **Change Settings**
4. Look for **Python** in the list
5. Make sure both **Private** and **Public** boxes are checked
6. If Python is not in the list:
   - Click **Allow another app...**
   - Browse to your Python executable (usually in `C:\Users\PC\AppData\Local\Programs\Python\Python311\python.exe`)
   - Add it and check both boxes

### Option B: Command Line (Run as Administrator)
```cmd
netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow protocol=TCP localport=8000
```

### Option C: Temporary - Disable Firewall (NOT RECOMMENDED for production)
1. Open Windows Defender Firewall
2. Click **Turn Windows Defender Firewall on or off**
3. Temporarily turn off firewall for Private networks only
4. **Remember to turn it back on later!**

## Step 3: Test Connectivity

### From your PC (should work):
- http://127.0.0.1:8000/
- http://localhost:8000/
- http://10.10.152.117:8000/

### From other devices:
- http://10.10.152.117:8000/

### Test with command line:
```cmd
# On your PC, test if the port is listening
netstat -an | findstr :8000

# Should show something like:
# TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING
```

## Step 4: Check Network Settings
1. Make sure all devices are on the **same network** (same WiFi/Ethernet)
2. Make sure your PC's network is set to **Private** (not Public)
3. Check that other devices can ping your PC:
   ```bash
   # From another device, try:
   ping 10.10.152.117
   ```

## Step 5: Test with Simple HTTP Server
If Django still doesn't work, test with Python's built-in server:
```bash
# In your project directory
python -m http.server 8000 --bind 0.0.0.0
```
Then try accessing `http://10.10.152.117:8000/` from another device.

## Step 6: Check Antivirus/Security Software
Some antivirus programs block incoming connections. Temporarily disable real-time protection to test.

## Common Issues:
1. **"Bad Request (400)"**: Django ALLOWED_HOSTS is not configured properly
2. **Connection timeout**: Windows Firewall is blocking the connection
3. **Connection refused**: Server is not listening on 0.0.0.0 (using 127.0.0.1 instead)
4. **Can't connect**: Devices are on different networks or network discovery is disabled

## Quick Test Commands:
```bash
# 1. Check if server is running and listening on all interfaces
netstat -an | findstr :8000

# 2. Check your IP address
ipconfig | findstr "IPv4"

# 3. Test firewall rule exists
netsh advfirewall firewall show rule name="Django Dev Server"
```

## Still Not Working?
1. Try a different port (e.g., 8080):
   ```bash
   python manage.py runserver 0.0.0.0:8080
   ```
2. Check Windows Event Viewer for blocked connections
3. Use Windows Resource Monitor to see if Python is listening on the correct port