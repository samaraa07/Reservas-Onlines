# Script PowerShell para executar o Sistema de Reservas

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sistema de Reservas Online" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Python não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Python 3.8 ou superior." -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verifica se Flask está instalado
Write-Host "[1/4] Verificando dependências..." -ForegroundColor Yellow
$flaskInstalled = pip show Flask 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[2/4] Instalando dependências..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao instalar dependências!" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
} else {
    Write-Host "[2/4] Dependências já instaladas." -ForegroundColor Green
}

# Verifica se o banco de dados existe
Write-Host "[3/4] Verificando banco de dados..." -ForegroundColor Yellow
if (-not (Test-Path "banco_de_dados\salon_reservas.db")) {
    Write-Host "Banco de dados não encontrado. Criando..." -ForegroundColor Yellow
    python db_create.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao criar banco de dados!" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
} else {
    Write-Host "Banco de dados encontrado." -ForegroundColor Green
}

# Inicia o servidor
Write-Host "[4/4] Iniciando servidor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Servidor iniciado com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Acesse: " -NoNewline
Write-Host "http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pressione CTRL+C para parar o servidor" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python app.py

