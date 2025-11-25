# Azure App Service Deployment Guide

This guide provides step-by-step instructions for deploying the web search application to Azure App Service.

## Prerequisites

Before you begin, ensure you have:

1. **Azure Account**: Active Azure subscription ([Create free account](https://azure.microsoft.com/free/))
2. **Azure CLI**: Installed and configured ([Installation guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
3. **Git**: Installed for version control
4. **Python 3.9+**: Installed locally for testing

## Step 1: Prepare Your Application Locally

### 1.1 Verify Project Structure

Ensure your project follows this structure:

```
project-root/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── search.py
│   ├── formatter.py
│   ├── static/
│   └── templates/
├── app.py
├── requirements.txt
└── .gitignore
```

### 1.2 Test Locally

Before deploying, test the application locally:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

# Test in browser
# Open http://localhost:5000
```

Verify that:
- Homepage loads correctly
- Search functionality works
- Results display properly with ASCII art
- No errors in terminal/console

### 1.3 Update requirements.txt

Ensure your `requirements.txt` includes all necessary packages:

```txt
Flask>=3.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
Pillow>=10.0.0
ascii-magic>=2.3.0
gunicorn>=21.2.0
```

**Note**: `gunicorn` is the production WSGI server for Azure App Service on Linux.

## Step 2: Install and Configure Azure CLI

### 2.1 Install Azure CLI

**On Windows:**
```bash
# Download and run the MSI installer from:
# https://aka.ms/installazurecliwindows
```

**On macOS:**
```bash
brew update && brew install azure-cli
```

**On Linux:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### 2.2 Login to Azure

```bash
az login
```

This will open a browser window for authentication. Sign in with your Azure credentials.

### 2.3 Set Your Subscription

If you have multiple subscriptions:

```bash
# List subscriptions
az account list --output table

# Set active subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

## Step 3: Create Azure Resources

### 3.1 Create Resource Group

A resource group is a container for related Azure resources.

```bash
# Create resource group
az group create \
  --name rg-search-app \
  --location eastus
```

**Locations**: Common options include `eastus`, `westus2`, `westeurope`, `centralus`. Choose one closest to your users.

### 3.2 Create App Service Plan

The App Service Plan defines the compute resources for your web app.

```bash
# Create App Service Plan (Linux, Free tier)
az appservice plan create \
  --name plan-search-app \
  --resource-group rg-search-app \
  --sku F1 \
  --is-linux
```

**SKU Options:**
- `F1`: Free tier (shared compute, 1GB memory, 60 min/day compute)
- `B1`: Basic tier ($~13/month, dedicated compute, 1.75GB memory)
- `S1`: Standard tier ($~70/month, auto-scaling, 1.75GB memory)

**Note**: Free tier has limitations (60 min CPU/day, always-on disabled). For production, use B1 or higher.

### 3.3 Create Web App

```bash
# Create Web App with Python 3.11 runtime
az webapp create \
  --resource-group rg-search-app \
  --plan plan-search-app \
  --name your-unique-app-name \
  --runtime "PYTHON:3.11"
```

**Important**:
- Replace `your-unique-app-name` with a globally unique name (letters, numbers, hyphens only)
- This name will be your app's URL: `https://your-unique-app-name.azurewebsites.net`
- If the name is taken, you'll get an error. Try a different name.

### 3.4 Configure Startup Command

Azure needs to know how to start your Flask app:

```bash
az webapp config set \
  --resource-group rg-search-app \
  --name your-unique-app-name \
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

**Explanation**:
- `gunicorn`: Production WSGI server
- `--bind=0.0.0.0`: Listen on all interfaces
- `--timeout 600`: 10-minute timeout (web scraping can be slow)
- `app:app`: Module name (`app.py`) and Flask instance name

## Step 4: Deploy Your Application

You have multiple deployment options. Choose one:

### Option A: Deploy from Local Git (Recommended for Development)

#### 4.1 Configure Local Git Deployment

```bash
# Enable local git deployment
az webapp deployment source config-local-git \
  --name your-unique-app-name \
  --resource-group rg-search-app
```

This command returns a Git URL like:
```
https://your-unique-app-name.scm.azurewebsites.net/your-unique-app-name.git
```

#### 4.2 Get Deployment Credentials

```bash
# Get deployment credentials
az webapp deployment list-publishing-credentials \
  --name your-unique-app-name \
  --resource-group rg-search-app \
  --query "{username:publishingUserName, password:publishingPassword}" \
  --output table
```

Save these credentials - you'll need them for Git push.

#### 4.3 Initialize Git and Deploy

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for Azure deployment"

# Add Azure remote
git remote add azure https://your-unique-app-name.scm.azurewebsites.net/your-unique-app-name.git

# Push to Azure (you'll be prompted for credentials)
git push azure main
```

**Note**: Use the deployment credentials from step 4.2 when prompted.

### Option B: Deploy from GitHub

#### 4.1 Push to GitHub

```bash
# Create GitHub repository and push your code
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main
```

#### 4.2 Configure GitHub Deployment

```bash
az webapp deployment source config \
  --name your-unique-app-name \
  --resource-group rg-search-app \
  --repo-url https://github.com/yourusername/your-repo \
  --branch main \
  --manual-integration
```

For continuous deployment (automatic updates on push), omit `--manual-integration` and follow the GitHub Actions setup.

### Option C: Deploy using ZIP

#### 4.1 Create ZIP file

```bash
# On Linux/Mac:
zip -r app.zip . -x "*.git*" "venv/*" "__pycache__/*" "*.pyc"

# On Windows (PowerShell):
Compress-Archive -Path * -DestinationPath app.zip -Force
```

#### 4.2 Deploy ZIP

```bash
az webapp deployment source config-zip \
  --resource-group rg-search-app \
  --name your-unique-app-name \
  --src app.zip
```

## Step 5: Configure Application Settings

### 5.1 Set Environment Variables (Optional)

If you need environment variables:

```bash
az webapp config appsettings set \
  --resource-group rg-search-app \
  --name your-unique-app-name \
  --settings FLASK_ENV=production SECRET_KEY=your-secret-key
```

### 5.2 Enable Application Logging

```bash
# Enable application logging
az webapp log config \
  --name your-unique-app-name \
  --resource-group rg-search-app \
  --application-logging filesystem \
  --detailed-error-messages true \
  --failed-request-tracing true \
  --web-server-logging filesystem
```

## Step 6: Verify Deployment

### 6.1 Check Deployment Status

```bash
# Stream live logs
az webapp log tail \
  --name your-unique-app-name \
  --resource-group rg-search-app
```

Watch for:
- `Booting worker with pid: XXXX`
- No Python errors or import failures
- Gunicorn startup messages

### 6.2 Open Your Application

```bash
# Open in browser
az webapp browse \
  --name your-unique-app-name \
  --resource-group rg-search-app
```

Or visit: `https://your-unique-app-name.azurewebsites.net`

### 6.3 Test Functionality

1. Load homepage
2. Enter a search query
3. Verify results display with ASCII art
4. Check browser console for JavaScript errors
5. Test multiple searches

## Step 7: Monitoring and Troubleshooting

### 7.1 View Application Logs

```bash
# Tail logs in real-time
az webapp log tail \
  --name your-unique-app-name \
  --resource-group rg-search-app

# Download logs
az webapp log download \
  --name your-unique-app-name \
  --resource-group rg-search-app \
  --log-file logs.zip
```

### 7.2 Access Kudu Console

Kudu is Azure's diagnostic console:

```
https://your-unique-app-name.scm.azurewebsites.net
```

From Kudu you can:
- Browse files: `/home/site/wwwroot`
- Check environment variables
- Run Python commands
- Debug deployment issues

### 7.3 Common Issues and Solutions

**Issue: Application won't start**
```bash
# Check logs for errors
az webapp log tail --name your-unique-app-name --resource-group rg-search-app

# Verify startup command
az webapp config show --name your-unique-app-name --resource-group rg-search-app --query "appCommandLine"
```

**Issue: Import errors or missing modules**
```bash
# Ensure requirements.txt is in root directory
# Redeploy after fixing requirements.txt
git add requirements.txt
git commit -m "Fix requirements"
git push azure main
```

**Issue: Search returns 500 errors**
- Check web scraping is allowed from Azure IP addresses
- Verify requests library has proper User-Agent headers
- Check logs for specific Python exceptions

**Issue: App is slow or times out**
- Increase timeout in startup command: `--timeout 900`
- Consider upgrading to B1 or higher App Service Plan
- DuckDuckGo scraping can be slow; set user expectations

### 7.4 Restart Application

```bash
az webapp restart \
  --name your-unique-app-name \
  --resource-group rg-search-app
```

## Step 8: Update and Redeploy

### 8.1 Update Code

When you make changes to your application:

```bash
# Make changes to your code
# Test locally first

# Commit changes
git add .
git commit -m "Description of changes"

# Push to Azure
git push azure main
```

Azure will automatically:
1. Detect the push
2. Install dependencies from requirements.txt
3. Restart the application

### 8.2 View Deployment History

```bash
az webapp deployment list \
  --name your-unique-app-name \
  --resource-group rg-search-app \
  --output table
```

## Step 9: Configure Custom Domain (Optional)

### 9.1 Add Custom Domain

```bash
# Add custom domain
az webapp config hostname add \
  --webapp-name your-unique-app-name \
  --resource-group rg-search-app \
  --hostname www.yourdomain.com
```

### 9.2 Enable HTTPS

```bash
# Enable HTTPS only
az webapp update \
  --name your-unique-app-name \
  --resource-group rg-search-app \
  --https-only true
```

## Step 10: Production Considerations

### 10.1 Upgrade to Paid Tier

For production use, upgrade from Free (F1) to at least Basic (B1):

```bash
az appservice plan update \
  --name plan-search-app \
  --resource-group rg-search-app \
  --sku B1
```

**Benefits of B1+:**
- No daily compute time limit
- Always-on (app stays loaded)
- Custom domains with SSL
- Better performance

### 10.2 Enable Always On

Prevents app from going idle (requires B1+):

```bash
az webapp config set \
  --name your-unique-app-name \
  --resource-group rg-search-app \
  --always-on true
```

### 10.3 Configure Auto-Scaling (S1+ only)

```bash
az monitor autoscale create \
  --resource-group rg-search-app \
  --resource your-app-plan-id \
  --min-count 1 \
  --max-count 3 \
  --count 1
```

### 10.4 Add Application Insights

Monitor performance and errors:

```bash
# Create Application Insights
az monitor app-insights component create \
  --app your-unique-app-name-insights \
  --location eastus \
  --resource-group rg-search-app

# Link to Web App
az monitor app-insights component connect-webapp \
  --app your-unique-app-name-insights \
  --resource-group rg-search-app \
  --web-app your-unique-app-name
```

## Step 11: Cleanup (Delete Resources)

When you're done or want to start over:

```bash
# Delete entire resource group (deletes all resources)
az group delete \
  --name rg-search-app \
  --yes \
  --no-wait
```

**Warning**: This permanently deletes:
- App Service Plan
- Web App
- All configuration and data

## Quick Reference Commands

### Deploy Update
```bash
git add .
git commit -m "Update"
git push azure main
```

### View Logs
```bash
az webapp log tail --name your-unique-app-name --resource-group rg-search-app
```

### Restart App
```bash
az webapp restart --name your-unique-app-name --resource-group rg-search-app
```

### Check Status
```bash
az webapp show --name your-unique-app-name --resource-group rg-search-app --query state
```

### List All Resources
```bash
az resource list --resource-group rg-search-app --output table
```

## Additional Resources

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Python on Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/webapp)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Kudu Wiki](https://github.com/projectkudu/kudu/wiki)

## Support

For issues specific to:
- **Azure**: [Azure Support](https://azure.microsoft.com/support/)
- **Flask**: [Flask Documentation](https://flask.palletsprojects.com/)
- **This Application**: Check application logs and GitHub issues
