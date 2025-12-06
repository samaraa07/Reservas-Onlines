# 🚀 Guia de Instalação e Execução do Sistema de Reservas

## 📋 Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

## 🔧 Passo a Passo para Rodar o Sistema

### 1. Navegue até a pasta do projeto

Abra o terminal/PowerShell e navegue até a pasta do sistema:

```bash
cd "Reservas-Onlines-main\Sistema_de_Reservas"
```

### 2. Crie um ambiente virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados (se necessário)

Se o banco de dados ainda não foi criado, execute:

```bash
python db_create.py
```

### 5. Execute o sistema

```bash
python app.py
```

### 6. Acesse o sistema

Abra seu navegador e acesse:

```
http://localhost:5000
```

ou

```
http://127.0.0.1:5000
```

## ⚙️ Configuração de E-mail (Opcional)

Para habilitar o envio de e-mails, configure as variáveis de ambiente:

**Windows (PowerShell):**
```powershell
$env:MAIL_SERVER="smtp.gmail.com"
$env:MAIL_PORT="587"
$env:MAIL_USE_TLS="true"
$env:MAIL_USERNAME="seu-email@gmail.com"
$env:MAIL_PASSWORD="sua-senha-app"
$env:MAIL_DEFAULT_SENDER="seu-email@gmail.com"
```

**Windows (CMD):**
```cmd
set MAIL_SERVER=smtp.gmail.com
set MAIL_PORT=587
set MAIL_USE_TLS=true
set MAIL_USERNAME=seu-email@gmail.com
set MAIL_PASSWORD=sua-senha-app
set MAIL_DEFAULT_SENDER=seu-email@gmail.com
```

**Linux/Mac:**
```bash
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT="587"
export MAIL_USE_TLS="true"
export MAIL_USERNAME="seu-email@gmail.com"
export MAIL_PASSWORD="sua-senha-app"
export MAIL_DEFAULT_SENDER="seu-email@gmail.com"
```

**Nota:** Se não configurar o e-mail, o sistema funcionará normalmente, mas apenas simulará o envio de e-mails (útil para desenvolvimento).

## 🎯 Primeiros Passos

1. **Acesse a página inicial** - Você verá os cards de Cliente, Profissional e Administrador
2. **Cadastre-se como Cliente** - Clique em "Cadastrar" no card Cliente
3. **Faça login** - Use suas credenciais para acessar o sistema

## 🔐 Contas de Administrador Padrão

O sistema pode ter administradores padrão já cadastrados. Verifique o arquivo `db_create.py` para mais informações.

## 🛠️ Solução de Problemas

### Erro: "ModuleNotFoundError"
- Certifique-se de que todas as dependências foram instaladas: `pip install -r requirements.txt`

### Erro: "No such file or directory: salon_reservas.db"
- Execute o script de criação do banco: `python db_create.py`

### Erro: "Address already in use"
- A porta 5000 já está em uso. Altere a porta no `app.py`:
  ```python
  app.run(debug=True, port=5001)
  ```

### Erro ao enviar e-mail
- Verifique se as credenciais de e-mail estão corretas
- Para Gmail, você precisa usar uma "Senha de App" em vez da senha normal
- Se não configurar, o sistema funcionará normalmente (apenas simula o envio)

## 📝 Estrutura do Projeto

```
Sistema_de_Reservas/
├── app.py                 # Aplicação principal Flask
├── models.py              # Modelos do banco de dados
├── db_create.py           # Script de criação do banco
├── requirements.txt       # Dependências do projeto
├── banco_de_dados/        # Pasta do banco de dados SQLite
├── templates/             # Templates HTML
├── static/                # Arquivos estáticos (CSS, JS, imagens)
└── README_INSTALACAO.md  # Este arquivo
```

## 🎉 Pronto!

Agora você pode usar o sistema de reservas. Aproveite!

