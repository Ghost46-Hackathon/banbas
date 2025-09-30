# Banbas Resort - Run on Local Network
# This script starts the Django server accessible from your local network

# Set environment PATH to include Python
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

# Get local IP address
$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*" | Where-Object {$_.IPAddress -like "10.*" -or $_.IPAddress -like "192.168.*" -or $_.IPAddress -like "172.*"}).IPAddress
if (-not $localIP) {
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -ne "127.0.0.1"}).IPAddress | Select-Object -First 1
}

$port = 8000

Write-Host "=" -NoNewline; for ($i=1; $i -le 60; $i++) { Write-Host "=" -NoNewline }; Write-Host ""
Write-Host "BANBAS RESORT - Django Development Server"
Write-Host "=" -NoNewline; for ($i=1; $i -le 60; $i++) { Write-Host "=" -NoNewline }; Write-Host ""
Write-Host "Your local IP address: $localIP"
Write-Host "Starting server on port $port"
Write-Host ""
Write-Host "Access the website from any device on your network:"
Write-Host "   Local: http://127.0.0.1:$port/"
Write-Host "   Network: http://${localIP}:$port/"
Write-Host "   Admin: http://${localIP}:$port/admin/"
Write-Host ""
Write-Host "Make sure Windows Firewall allows connections on port $port"
Write-Host "Press Ctrl+C to stop the server"
Write-Host "=" -NoNewline; for ($i=1; $i -le 60; $i++) { Write-Host "=" -NoNewline }; Write-Host ""
Write-Host ""

# Check if Windows Firewall rule exists
$firewallRule = Get-NetFirewallRule -DisplayName "Django Development Server" -ErrorAction SilentlyContinue
if (-not $firewallRule) {
    Write-Host "Creating Windows Firewall rule for port $port..."
    try {
        New-NetFirewallRule -DisplayName "Django Development Server" -Direction Inbound -Protocol TCP -LocalPort $port -Action Allow | Out-Null
        Write-Host "Firewall rule created successfully"
    } catch {
        Write-Host "Could not create firewall rule automatically. You may need to allow port $port manually."
    }
    Write-Host ""
}

# Start Django server
try {
    python manage.py runserver 0.0.0.0:$port
} catch {
    Write-Host "Error starting server. Make sure Python and Django are installed."
    Write-Host "Try running: pip install -r requirements.txt"
}
