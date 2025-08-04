# Reservas-Onlines

### Estruturação dos diretórios:
```
|Reservas-Online/
│  ├──__pycache__/
│  ├──banco_de_dados/
|  │  ├──database.sql
|  │  └──db_fisico.png
│  ├──static/
|  │  ├──pageStart.css
|  │  ├──painel.css
|  │  └──style.css
│  ├──templates/
|  │  ├──cadastro.html
|  │  ├──lista_reservas.html
|  │  ├──login.html
|  │  ├──pageStart.html
|  │  ├──painel.html
|  │  └──reservas.html
│  ├──venv/
├──app.py
├──requeriments.txt
└──usuarios.json
```

---

### Conteúdo do arquivo `banco_de_dados/database.sql`/:
```sql
CREATE DATABASE `db_reserva_cabeleireiro`;
/*DROP DATABASE IF EXISTS `db_reserva_cabeleireiro`;*/

USE `db_reserva_cabeleireiro`;

CREATE TABLE `tb_usuarios` (
	`usu_id` INT AUTO_INCREMENT PRIMARY KEY,
    `usu_name` VARCHAR(200),
    `uso_contato` VARCHAR(200),
    `usu_tipo` ENUM('cliente', 'profissional'),
    `usu_email` VARCHAR(200) UNIQUE,
    `usu_senha` VARCHAR(200)
);

CREATE TABLE `tb_clientes` (
	`cli_id` INT AUTO_INCREMENT PRIMARY KEY,
    `cli_nome` VARCHAR(200),
    `cli_contato` VARCHAR(200),
    `cli_email` VARCHAR(200) UNIQUE,
    `cli_usu_id` INT,
    FOREIGN KEY (`cli_usu_id`) REFERENCES `tb_usuarios`(`usu_id`)
);

CREATE TABLE `tb_profissionais` (
	`pro_id` INT AUTO_INCREMENT PRIMARY KEY,
    `pro_nome` VARCHAR(200),
    `pro_email` VARCHAR(200),
    `pro_contato` VARCHAR(200),
    `pro_horario` DATETIME,
    `pro_usu_id` INT,
    FOREIGN KEY (`pro_usu_id`) REFERENCES `tb_usuarios`(`usu_id`)
);

CREATE TABLE `tb_servicos` (
	`ser_id` INT AUTO_INCREMENT PRIMARY KEY,
    `ser_categoria` ENUM(
    'Corte Masculino', 'Corte Feminino', 'Corte Infantil',
    'Hidratação', 'Escova', 'Progressiva', 
    'Coloração', 'Luzes', 'Mechas', 
    'Penteado', 'Maquiagem', 'Design de Sobrancelhas', 
    'Manicure', 'Pedicure', 'Depilação') NOT NULL,
    `ser_descricao` VARCHAR(600),
    `ser_duracao` TIME,
    `ser_preco` FLOAT,
    `ser_pro_id` INT,
    FOREIGN KEY (`ser_pro_id`) REFERENCES `tb_profissionais`(`pro_id`)
);

CREATE TABLE `tb_agendamentos` (
	`age_id` INT AUTO_INCREMENT PRIMARY KEY,
    `age_cli_id` INT,
    FOREIGN KEY (`age_cli_id`) REFERENCES `tb_clientes`(`cli_id`),
    `age_pro_id` INT,
    FOREIGN KEY (`age_pro_id`) REFERENCES `tb_profissionais`(`pro_id`),
    `age_ser_id` INT,
    FOREIGN KEY (`age_ser_id`) REFERENCES `tb_servicos`(`ser_id`),
    `age_data_hora` DATETIME,
    `age_status` ENUM('pendente', 'confirmado', 'cancelado'),
    `age_criacao` DATETIME
);
```

---

### Conteúdo do arquivo `static/pageStart.css`/:
```css
body {
      background-color: #fdf6f0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      color: #5C3A21;
    }

    .modal-content {
      background-color: #fff9f5;
      border-radius: 15px;
      padding: 2rem;
      border: none;
      box-shadow: 0 8px 30px rgba(91, 61, 39, 0.2);
    }

    .modal-header {
      border-bottom: none;
    }

    .modal-title {
      color: #8B5E3C;
      font-weight: bold;
    }

    .nav-tabs .nav-link.active {
      background-color: #8B5E3C;
      color: white;
      border-color: #8B5E3C;
    }

    .nav-tabs .nav-link {
      color: #5C3A21;
    }

    .form-control {
      border-radius: 8px;
      border: 1px solid #D6A77A;
      background-color: #FFF9F5;
    }

    .btn-marrom {
      background-color: #8B5E3C;
      color: white;
      border: none;
    }

    .btn-marrom:hover {
      background-color: #5C3A21;
    }

    .title {
      font-size: 2rem;
      margin-bottom: 1rem;
      color: #8B5E3C;
    }

    .descricao {
      color: #6e4a33;
    }
```

---

### Conteúdo do arquivo `static/painel.css`/:
```css
.reserva-form {
      margin-top: 2rem;
      background-color: #fff9f5;
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 6px 18px rgba(91, 61, 39, 0.15);
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }

    .btn-marrom {
      background-color: #8B5E3C;
      color: white;
      font-weight: bold;
      border: none;
    }

    .btn-marrom:hover {
      background-color: #5C3A21;
    }

    .icon {
      font-variation-settings: 'FILL' 0, 'wght' 500, 'GRAD' 0, 'opsz' 24;
    }

    .gap-2 {
      gap: 0.5rem;
    }

    .gap-3 {
      gap: 1rem;
    }
```

---

### Conteúdo do arquivo `static/style.css`/:
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #fdf6f0;
  color: #5C3A21;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem;
}

/* ----------------------------------------------------- Cabeçalho */
h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #8B5E3C;
}

/* ----------------------------------------------------- Formulário */
form {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(91, 61, 39, 0.15);
}

form input,
form select,
form button {
  width: 100%;
  padding: 0.9rem;
  margin: 0.6rem 0 1.2rem;
  border-radius: 8px;
  border: 1px solid #D6A77A;
  font-size: 1rem;
  background-color: #FFF9F5;
  color: #5C3A21;
}

form input:focus,
form select:focus {
  outline: none;
  border-color: #8B5E3C;
  box-shadow: 0 0 6px rgba(139, 94, 60, 0.4);
}

form label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.4rem;
  color: #5C3A21;
}

form button,
.btn {
  background-color: #8B5E3C;
  color: #fff;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

form button:hover,
.btn:hover {
  background-color: #5C3A21;
}

.btn-2 {
  background-color: #D6A77A;
  color: #fff;
}

.btn-2:hover {
  background-color: #B47A4B;
}

/* --------------------------------------------------- Mensagens */
.erro-msg {
  color: #b00020;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1rem;
}

.sucesso-msg {
  color: #4CAF50;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1rem;
}

/* ------------------------------------------------ Lista das reservas */
ul {
  list-style: none;
  padding: 0;
}

ul li {
  background-color: #fff;
  padding: 1.2rem;
  margin-bottom: 1rem;
  border-left: 6px solid #8B5E3C;
  border-radius: 10px;
  box-shadow: 0 3px 8px rgba(91, 61, 39, 0.1);
  line-height: 1.5;
}

a {
  text-decoration: none;
  color: #8B5E3C;
}

a:hover {
  text-decoration: underline;
}

/* --------------------------------------------- Alinhamento */
.text-center {
  text-align: center;
}

.mt-3 {
  margin-top: 1rem;
}

.mt-4 {
  margin-top: 1.5rem;
  padding: 10px;
  border-radius: 20px;
  font-size: 18px;
}

.mt-5 {
  margin-top: 3rem;
}

/* ---------------------------------------------- Layout Responsivo */
@media (max-width: 600px) {
  .container {
    margin: 1rem;
    padding: 1rem;
  }

  form {
    padding: 1rem;
  }

  form input,
  form select,
  form button {
    font-size: 1rem;
  }
}

/* Estilo do modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 5; /* Z-index abaixo do modal */
}

.modal-form {
  position: fixed;
  z-index: 10;
  background: #f0eae5;
  padding: 2rem;
  border-radius: 12px;
  max-width: 400px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: none; /* Inicialmente escondido */
}

/* Botões de aba */
.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.tab {
  background: none;
  border: none;
  font-size: 16px;
  color: #8b5e3c;
  padding: 10px 20px;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
  border-radius: 5px;
  margin: 0 5px; /* Espaçamento entre os botões */
}

.tab:hover {
  background: #f0e0d6; /* Fundo ao passar o mouse */
}

.tab.active {
  background: #8b5e3c; /* Fundo do botão ativo */
  color: #fff; /* Cor do texto do botão ativo */
}

/* Estilo do botão de fechar */
.close-modal-btn {
  position: absolute;
  top: 12px;
  right: 16px; /* Mantido para alinhamento à direita */
  background: none;
  border: none; /* Remover borda */
  font-size: 26px; /* Aumentar o tamanho */
  font-weight: bold;
  color: #8B5E3C; /* Cor marrom */
  cursor: pointer;
  z-index: 10;
  transition: color 0.3s; /* Efeito de transição na cor */
}

.close-modal-btn:hover {
  color: #7b3e26; /* Cor mais escura ao passar o mouse */
}
```

---

### Conteúdo do arquivo `templates/cadastro.html`/:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Cadastro</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <div id="modal-backdrop" class="modal-backdrop"></div>

  <form method="POST" action="{{ url_for('cadastro') }}" class="modal-form" id="cadastro-form">
    <button type="button" class="close-modal-btn" onclick="fecharModal()">✖</button>
    <h2>Cadastro</h2>

    {% if erro %}
      <p class="erro-msg">{{ erro }}</p>
    {% endif %}

    <label>Nome de usuário</label>
    <input type="text" name="nome" placeholder="Nome de usuário" required />

    <label>Email</label>
    <input type="email" name="email" placeholder="Email" required />

    <label>Senha</label>
    <input type="password" name="senha" placeholder="Senha" required />

    <button type="submit">Cadastrar</button>
    <p class="text-center mt-2"><a href="/?aba=login">Já tem conta? Faça login</a></p>
  </form>

  <script>
    function fecharModal() {
      document.getElementById('cadastro-form').style.display = 'none';
      document.getElementById('modal-backdrop').style.display = 'none';
    }
  </script>
</body>
</html>
```

---

### Conteúdo do arquivo `templates/lista_reservas.html`/:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Minhas Reservas</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    .btn-marrom {
      background-color: #8B5E3C;
      color: white;
      font-weight: bold;
      border: none;
    }
    .btn-marrom:hover {
      background-color: #5C3A21;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2 class="text-center mb-4">Suas Reservas</h2>

    {% if reservas and reservas|length > 0 %}
      <ul>
        {% for r in reservas %}
          <li>
            <strong>{{ r.nome }}</strong> - {{ r.email }} <br>
            Tipo: {{ r.tipo }} <br>
            Data: {{ r.data }} | Hora: {{ r.hora }}
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p class="text-center">Você ainda não fez nenhuma reserva.</p>
    {% endif %}

    <div class="text-center mt-4">
      <a href="/painel" class="btn btn-marrom d-inline-flex align-items-center gap-2 px-4 py-2">
        <span class="icon">arrow_back</span> Voltar ao Painel
      </a>
    </div>
  </div>
</body>
</html>

```

---

### Conteúdo do arquivo `templates/login.html`/:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <div id="modal-backdrop" class="modal-backdrop"></div>

  <form method="POST" class="modal-form" id="login-form">
    <button type="button" class="close-modal-btn" onclick="fecharModal()">✖</button>
    <h2>Acesse sua conta</h2>

    {% if sucesso %}
      <p class="sucesso-msg">{{ sucesso }}</p>
    {% endif %}
    {% if erro %}
      <p class="erro-msg">{{ erro }}</p>
    {% endif %}

    <label>Nome ou Email</label>
    <input type="text" name="usuario" placeholder="Usuário" required />

    <label>Senha</label>
    <input type="password" name="senha" placeholder="Senha" required />

    <button type="submit">Entrar</button>
    <p class="text-center mt-2"><a href="/cadastro">Não tem conta? Cadastre-se</a></p>
  </form>

  <script>
    function fecharModal() {
      document.getElementById('login-form').style.display = 'none';
      document.getElementById('modal-backdrop').style.display = 'none';
    }
  </script>
</body>
</html>
```

---

### Conteúdo do arquivo `templates/pageStart.html`/:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Página Inicial</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
</head>
<body>

  <div class="text-center mt-5">
    <h1 class="title">Bem-vindo ao Sistema de Agendamento</h1>
    <p class="descricao">Facilite sua vida, agende com praticidade e estilo.</p>

    <button class="btn btn-marrom mt-4" id="btnAbrirModal">Entrar / Cadastrar</button>
  </div>

  <!-- Backdrop do modal -->
  <div id="modal-backdrop" class="modal-backdrop" style="display:none;"></div>

  <!-- Modal -->
  <div class="modal-form" id="modal-box" style="display:none;">
    <button type="button" class="close-modal-btn" onclick="fecharModal()">✖</button>

    <h2>Acesse sua conta</h2>

    {% with messages = get_flashed_messages(with_categories=True) %}
      {% if messages %}
        {% for category, message in messages %}
          {% if category == 'sucesso' %}
            <p class="sucesso-msg">{{ message }}</p>
          {% elif category == 'message' %}
            <p class="erro-msg">{{ message }}</p>
          {% endif %}
        {% endfor %}
      {% endif %}
    {% endwith %}

    <div class="tabs">
      <button class="tab active" onclick="mostrarAba('login')">Login</button>
      <button class="tab" onclick="mostrarAba('cadastro')">Cadastro</button>
    </div>

    <!-- Formulário Login -->
    <form id="aba-login" method="POST" action="/login">
      <label>Nome ou Email</label>
      <input type="text" name="usuario" placeholder="Usuário" required />
      <label>Senha</label>
      <input type="password" name="senha" placeholder="Senha" required />
      <button type="submit" class="btn btn-marrom">Entrar</button>
    </form>

    <!-- Formulário Cadastro -->
    <form id="aba-cadastro" method="POST" action="/cadastro" style="display:none;">
      <label>Nome completo</label>
      <input type="text" name="nome" placeholder="Nome completo" required />
      <label>Email</label>
      <input type="email" name="email" placeholder="Digite seu email" required />
      <label>Senha</label>
      <input type="password" name="senha" placeholder="Crie uma senha" required />
      <button type="submit" class="btn btn-marrom">Cadastrar</button>
    </form>
  </div>

  <script>
    const modalBox = document.getElementById('modal-box');
    const backdrop = document.getElementById('modal-backdrop');
    const btnAbrirModal = document.getElementById('btnAbrirModal');

    function mostrarAba(aba) {
      const abaLoginForm = document.getElementById('aba-login');
      const abaCadastroForm = document.getElementById('aba-cadastro');
      const tabLoginBtn = document.querySelector('.tab.active');
      const tabCadastroBtn = document.querySelector('.tab:not(.active)');

      if (aba === 'login') {
        abaLoginForm.style.display = 'block';
        abaCadastroForm.style.display = 'none';
        tabLoginBtn.classList.add('active');
        tabCadastroBtn.classList.remove('active');
      } else {
        abaLoginForm.style.display = 'none';
        abaCadastroForm.style.display = 'block';
        tabLoginBtn.classList.remove('active');
        tabCadastroBtn.classList.add('active');
      }
    }

    function abrirModal(aba = 'login') {
      modalBox.style.display = 'block';
      backdrop.style.display = 'block';
      mostrarAba(aba);
    }

    function fecharModal() {
      modalBox.style.display = 'none';
      backdrop.style.display = 'none';
    }

    btnAbrirModal.addEventListener('click', () => abrirModal('login'));
    backdrop.addEventListener('click', fecharModal);

    // Abre modal automaticamente pela query string ?aba=login ou ?aba=cadastro
    window.addEventListener('DOMContentLoaded', () => {
      const params = new URLSearchParams(window.location.search);
      const aba = params.get('aba');
      if (aba === 'login' || aba === 'cadastro') {
        abrirModal(aba);
      }
    });
  </script>

</body>
</html>
```

---

### Conteúdo do arquivo `templates/painel.html`/:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Painel</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
  <link rel="stylesheet" href="/static/painel.css">
</head>
<body>
  <div class="container text-center mt-5">
    <h2>Bem-vindo, {{ usuario }}</h2>

    <div class="d-flex justify-content-center gap-3 flex-wrap mt-4">
      <button class="btn btn-marrom d-flex align-items-center gap-2" onclick="toggleReserva()">
        <span class="icon">event</span> Fazer Reserva
      </button>

      <a href="/reservas" class="btn btn-2 d-flex align-items-center gap-2">
        <span class="icon">list_alt</span> Minhas Reservas
      </a>

      <a href="/logout" class="btn btn-danger d-flex align-items-center gap-2">
        <span class="icon">logout</span> Sair
      </a>
    </div>

    <div id="formReserva" class="reserva-form" style="display: none;">
      <form method="POST" action="/reserva">
        <h4 class="mb-3">Nova Reserva</h4>

        {% if erro %}
          <div class="alert alert-danger">{{ erro }}</div>
        {% endif %}

        <div class="mb-3 text-start">
          <label for="nome">Nome completo</label>
          <input type="text" class="form-control" name="nome" required>
        </div>

        <div class="mb-3 text-start">
          <label for="email">Email</label>
          <input type="email" class="form-control" name="email" required>
        </div>

        <div class="mb-3 text-start">
          <label for="tipo">Tipo de Serviço</label>
          <select name="tipo" class="form-control" required>
            <option value="">Selecione...</option>
            <option value="Cabelereiro">Cabelereiro</option>
            <option value="Barbeiro">Barbeiro</option>
            <option value="Manicure">Manicure</option>
            <option value="Estética">Estética</option>
            <option value="Depilação">Depilação</option>
            <option value="Massagem">Massagem</option>
            <option value="Maquiagem">Maquiagem</option>
            <option value="Outro">Outro</option>
          </select>
        </div>

        <div class="mb-3 text-start">
          <label for="data">Data da Reserva</label>
          <input type="date" class="form-control" name="data" required>
        </div>

        <div class="mb-3 text-start">
          <label for="hora">Horário da Reserva</label>
          <input type="time" class="form-control" name="hora" required>
        </div>

        <button type="submit" class="btn btn-marrom w-100">Reservar</button>
      </form>
    </div>
  </div>

  <script> //caso o formulário esteja invicível ele vai mostrar, porém se estiver à mostra ele esconde
    function toggleReserva() {
      const form = document.getElementById('formReserva');
      form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
  </script>
  
</body>
</html>

```

---

### Conteúdo do arquivo `templates/reservas.html`/:
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Reserva de Atendimento</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
</head>
<body>
  <form method="POST" action="{{ url_for('reserva') }}">
    <h2>Fazer Reserva</h2>

    {% if erro %}
      <p class="erro-msg">{{ erro }}</p>
    {% endif %}

    <label for="nome" class="sr-only">Seu nome completo</label>
    <input type="text" id="nome" name="nome" placeholder="Seu nome completo" required />

    <label for="tipo">Tipo de Serviço:</label>
    <select id="tipo" name="tipo" required>
      <option value="" disabled selected>Selecione...</option>
      <option value="Cabelereiro">Cabelereiro</option>
      <option value="Barbeiro">Barbeiro</option>
      <option value="Manicure">Manicure</option>
      <option value="Estética">Estética</option>
      <option value="Depilação">Depilação</option>
      <option value="Massagem">Massagem</option>
      <option value="Maquiagem">Maquiagem</option>
      <option value="Outro">Outro</option>
    </select>

    <label for="data">Data da Reserva:</label>
    <input type="date" id="data" name="data" required />

    <label for="hora">Horário da Reserva:</label>
    <input type="time" id="hora" name="hora" required />

    <button type="submit">Reservar</button>

    <p class="text-center mt-2"><a href="{{ url_for('painel_profissional') }}">Voltar ao Painel</a></p>
  </form>
</body>
</html>

```

---

### Conteúdo do arquivo `app.py`/:
```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configurando o flask-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'email@gmail.com'
app.config['MAIL_PASSWORD'] = 'senha'
mail = Mail(app)

USUARIOS_FILE = 'usuarios.json'

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=2)

@app.route('/')
def pagina_inicial():
    return render_template('pageStart.html')

@app.route('/login', methods=['POST'])
def login():
    usuarios = carregar_usuarios()
    entrada = request.form['usuario']
    senha = request.form['senha']

    for u in usuarios:
        if (entrada == u['nome'] or entrada == u['email']) and senha == u['senha']:
            session['usuario'] = u['nome']
            session['email'] = u['email']
            return redirect(url_for('painel_profissional'))

    flash("Usuário ou senha inválidos.", "message")
    return redirect(url_for('pagina_inicial') + "?aba=login")

@app.route('/cadastro', methods=['POST'])
def cadastro():
    usuarios = carregar_usuarios()
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if any(u['nome'] == nome or u['email'] == email for u in usuarios):
        flash("Usuário ou email já cadastrado.", "message")
        return redirect(url_for('pagina_inicial') + "?aba=cadastro")

    usuarios.append({'nome': nome, 'email': email, 'senha': senha})
    salvar_usuarios(usuarios)

    flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
    return redirect(url_for('pagina_inicial') + "?aba=login")

@app.route('/painel')
def painel_profissional():
    if 'usuario' not in session:
        return redirect(url_for('pagina_inicial'))
    return render_template('painel.html', usuario=session['usuario'])

@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if 'usuario' not in session:
        return redirect(url_for('pagina_inicial'))
    # Lógica de reservas
    return render_template('reservas.html')

@app.route('/reservas')
def ver_reservas():
    if 'usuario' not in session:
        return redirect(url_for('pagina_inicial'))
    # Lógica para mostrar reservas
    return render_template('lista_reservas.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('email', None)
    return redirect(url_for('pagina_inicial') + "?aba=login")

if __name__ == '__main__':
    app.run(debug=True)
```

---

### Conteúdo do arquivo `requeriments.txt`/:
```txt
blinker==1.9.0
click==8.2.1
colorama==0.4.6
Flask==3.1.1
Flask-Email==1.4.4
Flask-Mail==0.10.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
Werkzeug==3.1.3

```

---

### Conteúdo do arquivo `usuarios.json`/:
```json
[
  {
    "nome": " ",
    "email": " ",
    "senha": " "
  },
  {
    "nome": "Sthefany Dantas Brito",
    "email": "adm@gmail.com",
    "senha": "12345678"
  },
  {
    "nome": "Clarisse Dantas",
    "email": "admin@admin",
    "senha": "123"
  },
  {
    "nome": "Chiliu",
    "email": "chiliu@admin",
    "senha": "123"
  },
  {
    "nome": "Carmelita",
    "email": "carmelita@gmail",
    "senha": "123"
  },
  {
    "nome": "Samara",
    "email": "samaraA@gmail",
    "senha": "123"
  },
  {
    "nome": "ana",
    "email": "ana@gmail.com",
    "senha": "2005"
  },
  {
    "nome": "anna",
    "email": "anadearaujofsrc@gmail.com",
    "senha": "ana2005"
  },
  {
    "nome": "aninha",
    "email": "annadearaujofsrc@gmail.com",
    "senha": "ana2005"
  },
  {
    "nome": "samara",
    "email": "samara@gmail.com",
    "senha": "123"
  },
  {
    "nome": "lucas",
    "email": "lucas@gmail.com",
    "senha": "123"
  },
  {
    "nome": "Algu\u00e9m",
    "email": "alguem@gmail.com",
    "senha": "123"
  }
]
```

---