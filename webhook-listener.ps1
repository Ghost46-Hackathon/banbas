# GitHub Webhook Listener for Auto-Deployment
# This script listens for GitHub webhooks and triggers deployment automatically
# 
# Setup Instructions:
# 1. Install ngrok if not already installed: https://ngrok.com/download
# 2. Create a GitHub webhook:
#    - Go to: https://github.com/Ghost46-Hackathon/banbas/settings/hooks
#    - Click "Add webhook"
#    - Payload URL: Your ngrok URL for this listener (e.g., https://xxxx.ngrok.io/webhook)
#    - Content type: application/json
#    - Secret: (optional, but recommended)
#    - Events: Just the push event
# 3. Run this script: .\webhook-listener.ps1
# 4. The listener will run on http://localhost:9000
# 5. Expose it with ngrok: ngrok http 9000 (in a separate terminal)
# 6. Use that ngrok URL as your webhook URL in GitHub

param(
    [int]$Port = 9000
)

$ErrorActionPreference = "Continue"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "GitHub Webhook Listener" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Listening on: http://localhost:$Port/webhook" -ForegroundColor Yellow
Write-Host ""
Write-Host "To expose this listener to GitHub:" -ForegroundColor Yellow
Write-Host "  1. Open a new terminal" -ForegroundColor Gray
Write-Host "  2. Run: ngrok http $Port" -ForegroundColor Gray
Write-Host "  3. Use the ngrok URL as your GitHub webhook URL" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Simple HTTP listener using HttpListener
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()

Write-Host "[OK] Listener started" -ForegroundColor Green
Write-Host ""

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$deployScript = Join-Path $projectRoot "deploy.ps1"

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Incoming request: $($request.HttpMethod) $($request.Url.PathAndQuery)" -ForegroundColor Cyan
        
        if ($request.Url.PathAndQuery -eq "/webhook" -and $request.HttpMethod -eq "POST") {
            # Read the webhook payload
            $reader = New-Object System.IO.StreamReader($request.InputStream)
            $payload = $reader.ReadToEnd()
            $reader.Close()
            
            try {
                $data = $payload | ConvertFrom-Json
                
                # Check if this is a push event to main branch
                if ($data.ref -eq "refs/heads/main" -and $data.commits) {
                    Write-Host "[OK] Push detected to main branch" -ForegroundColor Green
                    Write-Host "     Commit: $($data.after[0..7])" -ForegroundColor Gray
                    Write-Host "     Author: $($data.head_commit.author.name)" -ForegroundColor Gray
                    Write-Host "     Message: $($data.head_commit.message)" -ForegroundColor Gray
                    Write-Host ""
                    Write-Host "Triggering deployment..." -ForegroundColor Yellow
                    
                    # Trigger deployment
                    Start-Process -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy Bypass -File `"$deployScript`"" -NoNewWindow -Wait
                    
                    $response.StatusCode = 200
                    $responseBody = @{
                        status = "success"
                        message = "Deployment triggered"
                        commit = $data.after
                    } | ConvertTo-Json
                } else {
                    Write-Host "[SKIP] Not a push to main branch" -ForegroundColor Yellow
                    $response.StatusCode = 200
                    $responseBody = @{
                        status = "skipped"
                        message = "Not a push to main branch"
                    } | ConvertTo-Json
                }
            } catch {
                Write-Host "[ERROR] Failed to parse webhook payload: $_" -ForegroundColor Red
                $response.StatusCode = 400
                $responseBody = @{
                    status = "error"
                    message = "Invalid payload"
                } | ConvertTo-Json
            }
        } elseif ($request.Url.PathAndQuery -eq "/health") {
            # Health check endpoint
            $response.StatusCode = 200
            $responseBody = @{
                status = "healthy"
                timestamp = (Get-Date).ToString("o")
            } | ConvertTo-Json
        } else {
            $response.StatusCode = 404
            $responseBody = @{
                status = "not_found"
                message = "Endpoint not found"
            } | ConvertTo-Json
        }
        
        # Send response
        $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseBody)
        $response.ContentLength64 = $buffer.Length
        $response.ContentType = "application/json"
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
        $response.OutputStream.Close()
        
    } catch {
        Write-Host "[ERROR] Error processing request: $_" -ForegroundColor Red
    }
}

$listener.Stop()

