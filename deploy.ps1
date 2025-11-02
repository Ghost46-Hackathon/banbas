# Banbas Resort Auto-Deployment Script
# This script pulls latest changes, restarts the Django server, and updates ngrok

param(
    [string]$NgrokUrl = "",
    [switch]$RunMigrations = $false
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Banbas Resort Auto-Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory (project root)
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Step 1: Pull latest changes from GitHub
Write-Host "[1/5] Pulling latest changes from GitHub..." -ForegroundColor Yellow
try {
    git pull origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Warning: Git pull had issues. Continuing anyway..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error pulling changes: $_" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Code updated" -ForegroundColor Green
Write-Host ""

# Step 2: Activate virtual environment and install dependencies
Write-Host "[2/5] Updating dependencies..." -ForegroundColor Yellow
& "C:\Users\RanjanMarasini\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
& "python" -m pip install --upgrade pip --quiet
& "python" -m pip install -r requirements.txt --quiet
Write-Host "[OK] Dependencies updated" -ForegroundColor Green
Write-Host ""

# Step 3: Run migrations
if ($RunMigrations) {
    Write-Host "[3/5] Running database migrations..." -ForegroundColor Yellow
    & "python" manage.py migrate --no-input
    Write-Host "[OK] Migrations applied" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[SKIP] Database migrations (Run with -RunMigrations to apply)" -ForegroundColor Yellow
    Write-Host ""
}

# Step 4: Stop existing Django server and ngrok
Write-Host "[4/5] Stopping existing services..." -ForegroundColor Yellow

# Stop Django server (port 8000)
$djangoProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($djangoProcess) {
    foreach ($pid in $djangoProcess) {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
}

# Stop ngrok
$ngrokProcess = Get-Process -Name "ngrok" -ErrorAction SilentlyContinue
if ($ngrokProcess) {
    Stop-Process -Name "ngrok" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

Write-Host "[OK] Services stopped" -ForegroundColor Green
Write-Host ""

# Step 5: Start Django server
Write-Host "[5/5] Starting Django server..." -ForegroundColor Yellow
$djangoJob = Start-Job -ScriptBlock {
    Set-Location $using:projectRoot
    & "$using:projectRoot\.venv\Scripts\python.exe" "$using:projectRoot\manage.py" runserver 0.0.0.0:8000
}
Start-Sleep -Seconds 3

# Verify Django is running
$maxAttempts = 10
$attempt = 0
while ($attempt -lt $maxAttempts) {
    $test = Test-NetConnection -ComputerName localhost -Port 8000 -WarningAction SilentlyContinue
    if ($test.TcpTestSucceeded) {
        Write-Host "[OK] Django server is running on port 8000" -ForegroundColor Green
        break
    }
    Start-Sleep -Seconds 1
    $attempt++
}

if ($attempt -eq $maxAttempts) {
    Write-Host "[ERROR] Django server failed to start" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 6: Start ngrok and get public URL
Write-Host "[6/6] Starting ngrok tunnel..." -ForegroundColor Yellow

# Start ngrok in background
$ngrokJob = Start-Job -ScriptBlock {
    Set-Location $env:USERPROFILE
    & "ngrok" http 8000
}

Start-Sleep -Seconds 5

# Get ngrok URL from API
$maxAttempts = 15
$attempt = 0
$publicUrl = ""

while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction SilentlyContinue
        if ($response -and $response.tunnels) {
            $publicUrl = $response.tunnels[0].public_url
            if ($publicUrl) {
                break
            }
        }
    } catch {
        # Ngrok API not ready yet
    }
    Start-Sleep -Seconds 2
    $attempt++
}

if ($publicUrl) {
    Write-Host "[OK] Ngrok tunnel established" -ForegroundColor Green
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host "Deployment Complete!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Public URL (via ngrok):" -ForegroundColor Yellow
    Write-Host "  $publicUrl" -ForegroundColor White
    Write-Host ""
    Write-Host "Local URL:" -ForegroundColor Yellow
    Write-Host "  http://127.0.0.1:8000/" -ForegroundColor White
    Write-Host ""
    Write-Host "Admin Panel:" -ForegroundColor Yellow
    Write-Host "  $publicUrl/admin/" -ForegroundColor White
    Write-Host ""
    
    # Update CSRF_TRUSTED_ORIGINS in settings.py
    Write-Host "Updating CSRF_TRUSTED_ORIGINS..." -ForegroundColor Yellow
    $settingsFile = Join-Path $projectRoot "banbas_resort\settings.py"
    $settingsContent = Get-Content $settingsFile -Raw
    
    # Replace any existing ngrok URL with the new one
    # Pattern matches: 'https://something.ngrok-free.dev' or 'https://something.ngrok.io'
    $ngrokPattern = "'https://[^']+\.ngrok[^']*'"
    
    if ($settingsContent -match $ngrokPattern) {
        # Replace the first ngrok URL found with the new one
        $settingsContent = $settingsContent -replace $ngrokPattern, "'$publicUrl'"
        Set-Content -Path $settingsFile -Value $settingsContent -NoNewline
        Write-Host "[OK] CSRF_TRUSTED_ORIGINS updated to: $publicUrl" -ForegroundColor Green
        
        # Restart Django to apply new settings
        Write-Host "Restarting Django to apply new CSRF settings..." -ForegroundColor Yellow
        Start-Sleep -Seconds 1
        $djangoProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
        if ($djangoProcess) {
            foreach ($pid in $djangoProcess) {
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            }
            Start-Sleep -Seconds 2
            
            # Restart Django
            $djangoJob = Start-Job -ScriptBlock {
                Set-Location $using:projectRoot
                & "$using:projectRoot\.venv\Scripts\python.exe" "$using:projectRoot\manage.py" runserver 0.0.0.0:8000
            }
            Start-Sleep -Seconds 3
            
            # Verify it's running
            $test = Test-NetConnection -ComputerName localhost -Port 8000 -WarningAction SilentlyContinue
            if ($test.TcpTestSucceeded) {
                Write-Host "[OK] Django restarted with new CSRF settings" -ForegroundColor Green
            } else {
                Write-Host "[WARNING] Django may not have restarted properly" -ForegroundColor Yellow
            }
        }
    } else {
        # No ngrok URL found, add it to the list
        $newLine = "    '$publicUrl',  # Current ngrok URL (auto-updated)"
        $settingsContent = $settingsContent -replace "(\[)", "`$1`n$newLine"
        Set-Content -Path $settingsFile -Value $settingsContent -NoNewline
        Write-Host "[OK] Added new ngrok URL to CSRF_TRUSTED_ORIGINS" -ForegroundColor Green
        Write-Host "[INFO] You may need to manually restart Django for this to take effect" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] Failed to get ngrok URL" -ForegroundColor Red
    Write-Host "Ngrok may still be starting. Check http://localhost:4040" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Deployment scripts are running in background jobs." -ForegroundColor Cyan
Write-Host "To view logs or stop services, check the jobs:" -ForegroundColor Cyan
Write-Host "  Get-Job                    # List all jobs" -ForegroundColor Gray
Write-Host "  Receive-Job -Id <ID>      # View job output" -ForegroundColor Gray
Write-Host "  Stop-Job -Id <ID>          # Stop a job" -ForegroundColor Gray
Write-Host ""

