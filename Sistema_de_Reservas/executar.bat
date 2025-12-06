@echo off
echo ========================================
echo   Sistema de Reservas Online
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.8 ou superior.
    pause
    exit /b 1
)

echo [1/4] Verificando dependencias...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [2/4] Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
) else (
    echo [2/4] Dependencias ja instaladas.
)

echo [3/4] Verificando banco de dados...
if not exist "banco_de_dados\salon_reservas.db" (
    echo Banco de dados nao encontrado. Criando...
    python db_create.py
    if errorlevel 1 (
        echo ERRO: Falha ao criar banco de dados!
        pause
        exit /b 1
    )
) else (
    echo Banco de dados encontrado.
)

echo [4/4] Iniciando servidor...
echo.
echo ========================================
echo   Servidor iniciado com sucesso!
echo ========================================
echo.
echo Acesse: http://localhost:5000
echo.
echo Pressione CTRL+C para parar o servidor
echo ========================================
echo.

python app.py

pause

