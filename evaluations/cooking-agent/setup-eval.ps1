# Quick Setup Script for Cooking Agent Evaluation
# This script helps you set up the evaluation environment

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🍳 Cooking AI Agent - Evaluation Setup" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "🔍 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor Gray

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Install evaluation dependencies
Write-Host ""
Write-Host "📦 Installing evaluation dependencies..." -ForegroundColor Yellow
Write-Host "   This includes azure-ai-evaluation and promptflow-tracing" -ForegroundColor Gray
Write-Host ""

pip install -r requirements-eval.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Failed to install evaluation dependencies." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Evaluation dependencies installed successfully!" -ForegroundColor Green

# Check for Azure authentication
Write-Host ""
Write-Host "🔑 Checking Azure authentication..." -ForegroundColor Yellow

# Check if logged in to Azure
$azAccount = az account show 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Azure authentication found (az login)" -ForegroundColor Green
    $accountInfo = $azAccount | ConvertFrom-Json
    Write-Host "   📧 Logged in as: $($accountInfo.user.name)" -ForegroundColor Gray
} else {
    Write-Host "   ⚠️  Not logged in to Azure" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   The evaluation uses Azure AI Foundry for AI-assisted evaluators." -ForegroundColor Gray
    Write-Host "   You need to authenticate with Azure." -ForegroundColor Gray
    Write-Host ""
    Write-Host "   Options:" -ForegroundColor Cyan
    Write-Host "   1. Run: " -NoNewline -ForegroundColor Gray
    Write-Host "az login" -ForegroundColor White
    Write-Host "   2. Use managed identity (if running in Azure)" -ForegroundColor Gray
    Write-Host ""
    
    $response = Read-Host "   Would you like to run 'az login' now? (y/N)"
    
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host ""
        az login
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Azure login successful" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Azure login failed" -ForegroundColor Red
        }
    } else {
        Write-Host "   ⏭️  Skipping Azure login - you can run 'az login' later" -ForegroundColor Yellow
    }
}

# Check for Azure OpenAI configuration
Write-Host ""
Write-Host "🔧 Checking Azure OpenAI configuration..." -ForegroundColor Yellow

if ($env:AZURE_OPENAI_ENDPOINT) {
    Write-Host "   ✅ AZURE_OPENAI_ENDPOINT: $env:AZURE_OPENAI_ENDPOINT" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  AZURE_OPENAI_ENDPOINT not set" -ForegroundColor Yellow
}

if ($env:AZURE_OPENAI_DEPLOYMENT) {
    Write-Host "   ✅ AZURE_OPENAI_DEPLOYMENT: $env:AZURE_OPENAI_DEPLOYMENT" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  AZURE_OPENAI_DEPLOYMENT not set (will use default: gpt-4o-mini)" -ForegroundColor Gray
}

if (-not $env:AZURE_OPENAI_ENDPOINT) {
    Write-Host ""
    Write-Host "   You'll need to set AZURE_OPENAI_ENDPOINT before running evaluation:" -ForegroundColor Gray
    Write-Host "   `$env:AZURE_OPENAI_ENDPOINT = 'https://your-resource.openai.azure.com/'" -ForegroundColor White
    Write-Host "   `$env:AZURE_OPENAI_DEPLOYMENT = 'gpt-4o-mini'" -ForegroundColor White
}

# Summary
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   1. Ensure Azure authentication:" -ForegroundColor Gray
Write-Host "      az login" -ForegroundColor White
Write-Host ""
Write-Host "   2. Set Azure OpenAI configuration:" -ForegroundColor Gray
Write-Host "      `$env:AZURE_OPENAI_ENDPOINT = 'https://your-resource.openai.azure.com/'" -ForegroundColor White
Write-Host "      `$env:AZURE_OPENAI_DEPLOYMENT = 'gpt-4o-mini'" -ForegroundColor White
Write-Host ""
Write-Host "   3. Review test data:" -ForegroundColor Gray
Write-Host "      - test_queries.json (10 test queries)" -ForegroundColor White
Write-Host "      - test_responses.json (sample responses)" -ForegroundColor White
Write-Host ""
Write-Host "   4. Run evaluation:" -ForegroundColor Gray
Write-Host "      python evaluate.py" -ForegroundColor White
Write-Host ""
Write-Host "   5. View results:" -ForegroundColor Gray
Write-Host "      evaluation_results/evaluation_results.json" -ForegroundColor White
Write-Host "      evaluation_results/metrics.json" -ForegroundColor White
Write-Host ""
Write-Host "   6. Read the guide:" -ForegroundColor Gray
Write-Host "      EVALUATION.md (comprehensive documentation)" -ForegroundColor White
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Ready to evaluate! Run: " -NoNewline -ForegroundColor Green
Write-Host "python evaluate.py" -ForegroundColor White
Write-Host ""
