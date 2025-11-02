# Auto-Deploy Service - Polls GitHub for changes and auto-deploys
# This is a simpler alternative to webhooks that polls GitHub periodically
# 
# Usage: Run this script and it will check for new commits every 60 seconds
# If new commits are found, it automatically runs deploy.ps1

param(
    [int]$PollInterval = 60,  # Check every 60 seconds
    [string]$Branch = "main"
)

$ErrorActionPreference = "Continue"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Auto-Deploy Service" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Polling GitHub every $PollInterval seconds for changes..." -ForegroundColor Yellow
Write-Host "Branch: $Branch" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$deployScript = Join-Path $projectRoot "deploy.ps1"
$lastCommit = ""

# Get the last commit hash locally
try {
    $lastCommit = (git rev-parse HEAD).Trim()
    Write-Host "Current local commit: $($lastCommit.Substring(0, [Math]::Min(8, $lastCommit.Length)))" -ForegroundColor Cyan
} catch {
    Write-Host "[ERROR] Not a git repository or git not found" -ForegroundColor Red
    exit 1
}

while ($true) {
    try {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Checking for updates..." -ForegroundColor Gray
        
        # Fetch latest from GitHub
        git fetch origin $Branch --quiet
        
        # Get remote commit
        $remoteCommit = (git rev-parse "origin/$Branch").Trim()
        
        if ($remoteCommit -ne $lastCommit) {
            Write-Host ""
            Write-Host "=========================================" -ForegroundColor Green
            Write-Host "🆕 New commits detected!" -ForegroundColor Green
            Write-Host "=========================================" -ForegroundColor Green
            Write-Host "Local:  $($lastCommit.Substring(0, [Math]::Min(8, $lastCommit.Length)))" -ForegroundColor Gray
            Write-Host "Remote: $($remoteCommit.Substring(0, [Math]::Min(8, $remoteCommit.Length)))" -ForegroundColor Gray
            Write-Host ""
            
            # Show commit message
            $commitMessage = (git log -1 --pretty=format:"%s" "origin/$Branch").Trim()
            Write-Host "Latest commit message:" -ForegroundColor Yellow
            Write-Host "  $commitMessage" -ForegroundColor White
            Write-Host ""
            
            Write-Host "Starting deployment..." -ForegroundColor Yellow
            Write-Host ""
            
            # Run deployment script
            & $deployScript
            
            # Update last commit
            $lastCommit = $remoteCommit
            
            Write-Host ""
            Write-Host "[OK] Deployment complete. Resuming polling..." -ForegroundColor Green
            Write-Host ""
        } else {
            Write-Host "  No changes detected" -ForegroundColor Gray
        }
        
        Start-Sleep -Seconds $PollInterval
        
    } catch {
        Write-Host "[ERROR] Error checking for updates: $_" -ForegroundColor Red
        Write-Host "Retrying in $PollInterval seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds $PollInterval
    }
}

