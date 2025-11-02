# Auto-Deployment Setup Guide

This guide explains how to set up automatic deployment that triggers whenever code is pushed to the GitHub repository.

## Overview

We've created three deployment options:

1. **Manual Deployment Script** (`deploy.ps1`) - Run manually when you want to deploy
2. **Auto-Polling Service** (`auto-deploy-service.ps1`) - Automatically checks GitHub every 60 seconds
3. **Webhook Listener** (`webhook-listener.ps1`) - Listens for GitHub webhooks (most efficient)

## Option 1: Manual Deployment (Simplest)

Just run the deployment script whenever you want to update:

```powershell
cd C:\Banbas\banbas
.\deploy.ps1
```

This will:
- Pull latest code from GitHub
- Update dependencies
- Run migrations
- Restart Django server
- Restart ngrok and get new URL
- Update CSRF_TRUSTED_ORIGINS automatically

## Option 2: Auto-Polling Service (Recommended for Testing)

This service runs continuously and checks GitHub for changes every 60 seconds.

### Setup

1. **Start the auto-deploy service:**

```powershell
cd C:\Banbas\banbas
.\auto-deploy-service.ps1
```

2. **Keep this terminal window open** - The service will run in the foreground.

3. **That's it!** The service will automatically deploy whenever new commits are pushed to the `main` branch.

### Customization

You can change the polling interval (default: 60 seconds):

```powershell
.\auto-deploy-service.ps1 -PollInterval 30  # Check every 30 seconds
```

### Running as Background Service

To run it in the background on Windows:

```powershell
# Create a scheduled task or use Windows Task Scheduler
Start-Process powershell.exe -ArgumentList "-File `"$PWD\auto-deploy-service.ps1`"" -WindowStyle Hidden
```

## Option 3: Webhook Listener (Most Efficient)

This listens for GitHub webhooks and deploys instantly when code is pushed.

### Setup Steps

1. **Start the webhook listener:**

```powershell
cd C:\Banbas\banbas
.\webhook-listener.ps1
```

2. **Expose the listener with ngrok** (in a separate terminal):

```powershell
ngrok http 9000
```

You'll get a URL like: `https://xxxx-xxx-xxx-xxx.ngrok-free.dev`

3. **Configure GitHub Webhook:**

   - Go to: `https://github.com/Ghost46-Hackathon/banbas/settings/hooks`
   - Click **"Add webhook"**
   - **Payload URL:** `https://xxxx-xxx-xxx-xxx.ngrok-free.dev/webhook` (use your ngrok URL)
   - **Content type:** `application/json`
   - **Secret:** (optional, but recommended for production)
   - **Which events:** Select "Just the push event"
   - Click **"Add webhook"**

4. **That's it!** Now whenever you push to the main branch, GitHub will send a webhook, and your server will automatically deploy.

### Webhook Listener Port

Default port is 9000. To change it:

```powershell
.\webhook-listener.ps1 -Port 8080
```

## GitHub Actions Workflow

We've also created a GitHub Actions workflow (`.github/workflows/deploy.yml`) that:

- Triggers on every push to `main` branch
- Logs deployment information
- Can be extended to send notifications

Note: The GitHub Actions workflow currently just logs the deployment. The actual deployment happens on your local machine via one of the three methods above.

## How It Works

### Deployment Process

1. **Pull Code:** Fetches latest changes from GitHub
2. **Update Dependencies:** Installs/updates Python packages
3. **Run Migrations:** Applies database migrations
4. **Stop Services:** Stops existing Django and ngrok processes
5. **Start Django:** Starts Django server on port 8000
6. **Start Ngrok:** Creates tunnel and gets public URL
7. **Update CSRF:** Automatically updates `CSRF_TRUSTED_ORIGINS` in settings.py
8. **Restart Django:** Restarts Django to apply new CSRF settings

### Automatic CSRF Update

The deployment script automatically:
- Detects the new ngrok URL
- Updates `banbas_resort/settings.py` with the new URL in `CSRF_TRUSTED_ORIGINS`
- Restarts Django to apply the changes

This means you don't need to manually update settings when ngrok URLs change!

## Troubleshooting

### Deployment Script Fails

1. **Check Python installation:**
   ```powershell
   python --version
   ```

2. **Verify virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Check Git repository:**
   ```powershell
   git status
   ```

### Ngrok URL Not Updating

If the CSRF settings aren't updating automatically:

1. Manually edit `banbas_resort/settings.py`
2. Find `CSRF_TRUSTED_ORIGINS`
3. Replace the ngrok URL with your current one from `ngrok http 8000`

### Port Already in Use

If port 8000 is already in use:

```powershell
# Find process using port 8000
netstat -ano | findstr ":8000"

# Kill the process (replace PID with actual process ID)
Stop-Process -Id <PID> -Force
```

### Webhook Not Working

1. Check that the webhook listener is running
2. Verify ngrok is running and forwarding to port 9000
3. Check GitHub webhook settings - look for recent deliveries
4. Check the webhook listener terminal for incoming requests

## Stopping Services

To stop all services:

```powershell
# Stop Django (port 8000)
Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Stop ngrok
Stop-Process -Name "ngrok" -Force

# Stop webhook listener (if running)
# Just press Ctrl+C in the terminal
```

## Next Steps

1. **Choose your deployment method** (auto-polling is easiest to start with)
2. **Test it** by making a small change and pushing to GitHub
3. **Monitor the deployment** to ensure everything works correctly
4. **Consider setting up the webhook listener** for instant deployments

## Security Notes

- ⚠️ The current setup is for **development/testing only**
- 🔒 For production, add webhook secret verification
- 🔒 Use environment variables for sensitive data
- 🔒 Set up proper authentication for the webhook listener
- 🔒 Consider using a reverse proxy (nginx) instead of direct Django access

---

**Questions?** Check the deployment script comments or open an issue on GitHub.

