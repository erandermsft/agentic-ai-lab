# Setup script for Azure AI Foundry Cloud Evaluation
# Run this script to configure your environment for cloud evaluation

param(
    [switch]$Install,
    [switch]$Configure,
    [switch]$Test
)

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  Azure AI Foundry Cloud Evaluation Setup" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command {
    param($Command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $Command) { return $true }
    }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
if (-not (Test-Command python)) {
    Write-Host "  ERROR: Python not found. Please install Python 3.9+." -ForegroundColor Red
    exit 1
}
$pythonVersion = python --version
Write-Host "  Python: $pythonVersion" -ForegroundColor Green

# Check Azure CLI
if (-not (Test-Command az)) {
    Write-Host "  WARNING: Azure CLI not found. You'll need it for authentication." -ForegroundColor Yellow
    Write-Host "    Install from: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
}
else {
    $azVersion = az --version | Select-Object -First 1
    Write-Host "  Azure CLI: $azVersion" -ForegroundColor Green
}

Write-Host ""

# Install dependencies
if ($Install -or $PSBoundParameters.Count -eq 0) {
    Write-Host "Installing evaluation dependencies..." -ForegroundColor Yellow
    
    try {
        python -m pip install --upgrade pip
        pip install -r requirements-eval.txt
        
        Write-Host "  Dependencies installed successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "  ERROR: Failed to install dependencies." -ForegroundColor Red
        Write-Host "  $_" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
}

# Configure environment
if ($Configure -or $PSBoundParameters.Count -eq 0) {
    Write-Host "Configuring environment..." -ForegroundColor Yellow
    
    # Check if .env exists
    if (-not (Test-Path ".env")) {
        Write-Host "  .env file not found. Creating from template..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "  .env created. Please update with your values." -ForegroundColor Yellow
    }
    else {
        Write-Host "  .env file found." -ForegroundColor Green
    }
    
    # Load and validate .env
    if (Test-Path ".env") {
        $envVars = Get-Content ".env" | Where-Object { $_ -match '^\s*[A-Z]' -and $_ -notmatch '^\s*#' }
        
        $required = @(
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT",
            "PROJECT_ENDPOINT",
            "MODEL_ENDPOINT"
        )
        
        Write-Host ""
        Write-Host "  Environment Variables:" -ForegroundColor Cyan
        
        foreach ($var in $required) {
            $found = $envVars | Where-Object { $_ -match "^$var=" }
            if ($found -and $found -notmatch "your-") {
                Write-Host "    $var" -NoNewline -ForegroundColor White
                Write-Host " ✓" -ForegroundColor Green
            }
            else {
                Write-Host "    $var" -NoNewline -ForegroundColor White
                Write-Host " ✗ (not configured)" -ForegroundColor Red
            }
        }
    }
    
    Write-Host ""
    Write-Host "  Configuration Guide:" -ForegroundColor Cyan
    Write-Host "    1. Open .env file" -ForegroundColor White
    Write-Host "    2. Set PROJECT_ENDPOINT from Azure AI Foundry portal" -ForegroundColor White
    Write-Host "    3. Set MODEL_ENDPOINT from your Azure AI Foundry project" -ForegroundColor White
    Write-Host "    4. Set AZURE_OPENAI_ENDPOINT from Azure OpenAI resource" -ForegroundColor White
    Write-Host "    5. Set AZURE_OPENAI_DEPLOYMENT to your model deployment name" -ForegroundColor White
    
    Write-Host ""
}

# Test authentication
if ($Test -or $PSBoundParameters.Count -eq 0) {
    Write-Host "Testing Azure authentication..." -ForegroundColor Yellow
    
    if (-not (Test-Command az)) {
        Write-Host "  SKIPPED: Azure CLI not installed." -ForegroundColor Yellow
    }
    else {
        try {
            $account = az account show 2>$null | ConvertFrom-Json
            if ($account) {
                Write-Host "  Logged in as: $($account.user.name)" -ForegroundColor Green
                Write-Host "  Subscription: $($account.name)" -ForegroundColor Green
            }
            else {
                Write-Host "  Not logged in. Run: az login" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "  Not logged in. Run: az login" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
}

# Summary
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Update .env with your Azure AI Foundry endpoints" -ForegroundColor White
Write-Host "  2. Authenticate: az login" -ForegroundColor White
Write-Host "  3. Generate test responses: python run_agent.py" -ForegroundColor White
Write-Host "  4. Submit evaluation: python evaluate.py" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - EVALUATION_CLOUD.md - Cloud evaluation guide" -ForegroundColor White
Write-Host "  - .env.example - Environment variable template" -ForegroundColor White
Write-Host ""
