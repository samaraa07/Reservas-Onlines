# Reservas-Onlines

### Organização dos Diretórios:
```
|Reservas-Onlines/
|   ├──__pycache__/
|   ├──banco_de_dados/
|   |   └──database.sql
|   ├──env/
|   ├──instance/
|   |   └──salon_reservas.db
|   ├──static/
|   |   ├──css/
|   |   |   └──style.css
|   |   └──imgs/
|   ├──templates/
|   |   ├──base.html
|   |   ├──dashboard_admin.html
|   |   ├──dashboard_cliente.html
|   |   ├──dashboard_profissional.html
|   |   ├──index.html
|   |   ├──login.html
|   |   ├──minhas_reservas.html
|   |   ├──notificacoes.html
|   |   ├──register_admin.html
|   |   ├──register_cliente.html
|   |   ├──register_profissional.html
|   |   ├──register_servico.html
|   |   └──reservar.html
|   ├──app.py
|   ├──db_create.py
|   ├──LICENSE
|   ├──models.py
|   ├──README.md
|   └──requirements.txt
```

#### Conteúdo do arquivo `Reservas-Onlines/banco_de_dados/database.sql`:
```
Em desuso!
```

---


#### Conteúdo do arquivo `Reservas-Onlines/static/css/style.css`:
```css
/* =========================
   RESET & BASE
========================= */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --cor-primaria: #8B5E3C;
  --cor-secundaria: #F4E1D2;
  --cor-destaque: #FF6B35;
  --cor-fundo: #f9f7f6;
  --cor-texto: #333;
  --cor-sucesso: #d4edda;
  --cor-perigo: #f8d7da;
  --cor-aviso: #fff3cd;
  --cor-info: #d1ecf1;
}

body {
  font-family: 'Poppins', sans-serif;
  color: var(--cor-texto);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-image: url('../imgs/plano_de_fundo(2).jpg');
  background-repeat: no-repeat;
  background-size: 100%;
  background-position: center;
}

/* =========================
   CONTAINER
========================= */
.container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 1rem;
}

/* =========================
   NAVEGAÇÃO
========================= */
.nav {
  background: var(--cor-primaria);
  color: #fff;
  padding: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}

.nav a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  padding: 0.5rem 0.8rem;
  border-radius: 6px;
  transition: background 0.3s;
}

.nav a:hover {
  background: rgba(255, 255, 255, 0.2);
}

.nav span {
  margin-right: auto;
  font-style: italic;
}

/* =========================
   BOTÕES
========================= */
button, .btn {
  background: var(--cor-primaria);
  color: #fff;
  border: none;
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s, background 0.3s;
}

button:hover, .btn:hover {
  background: var(--cor-destaque);
  transform: scale(1.05);
}

/* =========================
   FORMULÁRIOS
========================= */
form {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input, select {
  width: 100%;
  padding: 0.8rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus, select:focus {
  border-color: var(--cor-primaria);
  outline: none;
  box-shadow: 0 0 5px rgba(139, 94, 60, 0.4);
}

label {
  font-weight: 600;
  color: var(--cor-primaria);
}

/* =========================
   LISTAS E CARDS
========================= */
ul {
  list-style: none;
  padding: 0;
}

ul li, .card {
  background: #fff;
  margin: 0.6rem 0;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  line-height: 1.4;
}

.card strong, ul li strong {
  color: var(--cor-primaria);
}

/* =========================
   FLASH MESSAGES
========================= */
.flashes {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.flash {
  padding: 0.8rem;
  margin-bottom: 0.6rem;
  border-radius: 6px;
  font-weight: bold;
}

.flash.success { background: var(--cor-sucesso); color: #155724; }
.flash.danger  { background: var(--cor-perigo); color: #721c24; }
.flash.warning { background: var(--cor-aviso); color: #856404; }
.flash.info    { background: var(--cor-info); color: #0c5460; }

/* =========================
   TÍTULOS
========================= */
h1, h2, h3 {
  color: var(--cor-primaria);
  margin-bottom: 1rem;
}

/* =========================
   LINKS
========================= */
a {
  text-decoration: none;
  color: #0066cc;
}
a:hover {
  text-decoration: underline;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  margin: 0.2rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: 0.2s;
}

.btn-secundario {
  background: #eee;
  color: #333;
  border: 1px solid #ccc;
}
.btn-secundario:hover {
  background: #ddd;
}


/* =========================
   NOTIFICAÇÕES
========================= */
ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 0.7rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  background: #fafafa;
  border: 1px solid #e2e2e2;
  position: relative;
}

/* Notificação não lida */
li.nao-lida {
  background: #fff8e1;
  border-left: 5px solid #ff9800;
}

/* Badge "Novo" */
li.nao-lida::before {
  content: "Novo";
  background: #ff9800;
  color: #fff;
  font-size: 0.7rem;
  font-weight: bold;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  position: absolute;
  top: 8px;
  right: 10px;
}

/* Links dentro da notificação */
li a {
  font-size: 0.8rem;
  margin-left: 1rem;
  color: #0077cc;
}
li a:hover {
  text-decoration: underline;
}

/* =========================
   DASHBOARD / GRID
========================= */
.dashboard {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1rem;
}

@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
  }
}

/* =========================
   RESPONSIVIDADE
========================= */
@media (max-width: 600px) {
  .container {
    margin: 1rem;
    padding: 1rem;
  }

  form {
    padding: 1rem;
  }

  input, select, button {
    font-size: 0.9rem;
  }

  .nav {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav a {
    margin: 0.3rem 0;
  }
}

/* =========================
   HOME CARDS
========================= */
.cards-home {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.card-home {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 2rem;
  width: 280px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card-home:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

.card-home h2 {
  color: var(--cor-primaria);
  margin-bottom: 1rem;
}

.card-home p {
  margin-bottom: 1.5rem;
  color: #555;
}

.card-home .btn {
  display: inline-block;
  margin: 0.4rem;
  min-width: 100px;
  text-align: center;
}

/* Botão secundário */
.btn-secundario {
  background: var(--cor-secundaria);
  color: var(--cor-primaria);
  border: 1px solid var(--cor-primaria);
}

.btn-secundario:hover {
  background: var(--cor-destaque);
  color: #fff;
  border-color: var(--cor-destaque);
}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/base.html`:
```html
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Salão{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  </head>
  <body>
    <header>
      <div class="nav">
        <a href="{{ url_for('index') }}">Início</a>
        
        {% if user %}
          <span>
            Olá, {{ user.nome }} 
            ({{ user.perfil|capitalize }}
            {% if user.perfil == 'profissional' %}
              – {{ user.profissional.especialidades }}
            {% endif %})
          </span>

          <!-- Atalhos diferentes por perfil -->
          {% if user.perfil == 'cliente' %}
            <a href="{{ url_for('minhas_reservas') }}">Minhas Reservas</a>
          {% elif user.perfil == 'profissional' %}
            <a href="{{ url_for('dashboard_profissional') }}">Meus Agendamentos</a>
          {% elif user.perfil == 'admin' %}
            <a href="{{ url_for('dashboard_admin') }}">Painel Geral</a>
          {% endif %}

          <a href="{{ url_for('notificacoes') }}">Notificações</a>
          <a href="{{ url_for('logout') }}">Sair</a>
        {% endif %}
      </div>
    </header>

    <main>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <ul class="flashes">
          {% for category, message in messages %}
            <li class="flash {{ category }}">{{ message|safe }}</li>
          {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}

      {% block content %}{% endblock %}
    </main>
  </body>
</html>

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/dashboard_admin.html`:
```html
{% extends "base.html" %}
{% block title %}Painel Administrador{% endblock %}
{% block content %}
  <div class="container">
    <h2>Bem-vindo(a), {{ user.nome }}!</h2>
    <p>Você está logado como <strong>Administrador</strong>.</p>

    <h3>Profissionais cadastrados</h3>
    <ul>
      {% for p in profissionais %}
        <li>{{ p.user.nome }} – Especialidade(s): {{ p.especialidades }}</li>
      {% else %}
        <li>Nenhum profissional cadastrado.</li>
      {% endfor %}
    </ul>

    <h3>Clientes cadastrados</h3>
    <ul>
      {% for c in clientes %}
        <li>{{ c.user.nome }} – Contato: {{ c.contato if c.contato else 'Não informado' }}</li>
      {% else %}
        <li>Nenhum cliente cadastrado.</li>
      {% endfor %}
    </ul>

    <h3>Serviços cadastrados</h3>
    <ul>
      {% for s in servicos %}
        <li>{{ s.nome }} ({{ s.duracao_min }} min) – Profissional: {{ s.profissional.user.nome }}</li>
      {% else %}
        <li>Nenhum serviço cadastrado.</li>
      {% endfor %}
    </ul>

    <p>
      <a href="{{ url_for('register_servico') }}" class="btn">Cadastrar novo serviço</a>
    </p>

    <h3>Todos os Agendamentos</h3>
    <ul>
      {% for ag in agendamentos %}
        <li>
          {{ ag.data_hora.strftime('%d/%m/%Y %H:%M') }} – 
          Serviço: {{ ag.servico.nome }} | 
          Cliente: {{ ag.cliente.user.nome }} | 
          Profissional: {{ ag.profissional.user.nome }} 
          ({{ ag.status }})
        </li>
      {% else %}
        <li>Nenhum agendamento encontrado.</li>
      {% endfor %}
    </ul>
  </div>
{% endblock %}

```
 
---

#### Conteúdo do arquivo `Reservas-Onlines/templates/dashboard_cliente.html`:
```html
{% extends "base.html" %}
{% block title %}Painel Cliente{% endblock %}
{% block content %}
  <div class="container">
    <h2>Bem-vindo(a), {{ user.nome }}!</h2>
    <p>Você está logado como <strong>Cliente</strong>.</p>

    <a href="{{ url_for('reservar') }}" class="btn">Fazer minha reserva</a>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/dashboard_profissional.html`:
```html
{% extends "base.html" %}
{% block title %}Painel Profissional{% endblock %}
{% block content %}
  <div class="container">
    <h2>Bem-vindo(a), {{ user.nome }}!</h2>
    <p>Você está logado como <strong>Profissional</strong>.</p>
    <p><strong>Especialidade(s):</strong> {{ user.profissional.especialidades }}</p>

    <h3>Seus agendamentos</h3>
    <ul>
      {% for ag in agendamentos %}
        <li>
          {{ ag.data_hora.strftime('%d/%m/%Y %H:%M') }} – 
          {{ ag.servico.nome }} 
          (Cliente: {{ ag.cliente.user.nome }})
        </li>
      {% else %}
        <li>Você ainda não possui agendamentos.</li>
      {% endfor %}
    </ul>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/index.html`:
```html
{% extends "base.html" %}
{% block title %}Início{% endblock %}
{% block content %}
  <div class="container">
    <h1>Bem-vindo ao Sistema de Agendamento do Salão</h1>
    <p>Escolha como deseja acessar:</p>

    <div class="cards-home">
      <!-- Cliente -->
      <div class="card-home">
        <h2>Cliente</h2>
        <p>Agende seus serviços de forma rápida e fácil.</p>
        <a href="{{ url_for('login') }}" class="btn">Login</a>
        <a href="{{ url_for('register_cliente') }}" class="btn btn-secundario">Cadastro</a>
      </div>

      <!-- Profissional -->
      <div class="card-home">
        <h2>Profissional</h2>
        <p>Gerencie seus agendamentos e serviços oferecidos.</p>
        <a href="{{ url_for('login') }}" class="btn">Login</a>
        <a href="{{ url_for('register_profissional') }}" class="btn btn-secundario">Cadastro</a>
      </div>

      <!-- Administrador -->
      <div class="card-home">
        <h2>Administrador</h2>
        <p>Acesse o painel de controle do sistema.</p>
        <a href="{{ url_for('login') }}" class="btn">Login</a>
        <a href="{{ url_for('register_admin') }}" class="btn btn-secundario">Cadastro</a>
      </div>
    </div>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/login.html`:
```html
{% extends "base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
  <div class="container">
    <h2>Login</h2>
    <form method="post" action="{{ url_for('login') }}">
      <input type="email" name="email" placeholder="Email" required>
      <input type="password" name="senha" placeholder="Senha" required>
      <button type="submit">Entrar</button>
    </form>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/minhas_reservas.html`:
```html
{% extends "base.html" %}
{% block title %}Minhas Reservas{% endblock %}
{% block content %}
  <div class="container">
    <h2>Minhas Reservas</h2>

    {% if agendamentos %}
      <ul>
      {% for a in agendamentos %}
        <li>
          {{ a.servico.nome }} com {{ a.profissional.user.nome }} —
          {{ a.data_hora.strftime('%Y-%m-%d %H:%M') }} —
          <strong>{{ a.status }}</strong>

          {% if a.status != 'cancelado' %}
            <a href="{{ url_for('cancelar_agendamento', ag_id=a.id) }}">Cancelar</a>
          {% endif %}
        </li>
      {% endfor %}
      </ul>
    {% else %}
      <p>Você não possui reservas.</p>
    {% endif %}
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/notificacoes.html`:
```html
{% extends "base.html" %}
{% block title %}Notificações{% endblock %}
{% block content %}
  <div class="container">
    <h2>Notificações</h2>

    {% if notificacoes %}
      <div style="margin-bottom:1rem;">
        <a href="?filtro=nao_lidas" class="btn btn-secundario">Somente não lidas</a>
        <a href="?filtro=todas" class="btn btn-secundario">Todas</a>
      </div>

      <ul>
      {% for n in notificacoes %}
        <li {% if not n.lida %}class="nao-lida"{% endif %}>
          {{ n.criado_em.strftime('%d/%m/%Y %H:%M') }} — {{ n.mensagem }}
          {% if not n.lida %}
            <a href="{{ url_for('marcar_lida', notif_id=n.id) }}">Marcar como lida</a>
          {% endif %}
        </li>
      {% endfor %}
      </ul>
    {% else %}
      <p>Sem notificações.</p>
    {% endif %}
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/register_admin.html`:
```html
{% extends "base.html" %}
{% block title %}Cadastro Administrador{% endblock %}
{% block content %}
  <div class="container">
    <h2>Cadastro de Administrador</h2>
    <form method="post" action="{{ url_for('register_admin') }}">
      <input type="text" name="nome" placeholder="Nome" required>
      <input type="email" name="email" placeholder="Email" required>
      <input type="password" name="senha" placeholder="Senha" required>
      <button type="submit">Cadastrar</button>
    </form>
    <p>Já tem conta? <a href="{{ url_for('login') }}">Fazer login</a></p>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/register_cliente.html`:
```html
{% extends "base.html" %}
{% block title %}Cadastro Cliente{% endblock %}
{% block content %}
  <div class="container">
    <h2>Cadastro de Cliente</h2>
    <form method="post" action="{{ url_for('register_cliente') }}">
      <input type="text" name="nome" placeholder="Nome" required>
      <input type="email" name="email" placeholder="Email" required>
      <input type="password" name="senha" placeholder="Senha" required>
      <button type="submit">Cadastrar</button>
    </form>
    <p>Já tem conta? <a href="{{ url_for('login') }}">Fazer login</a></p>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/register_profissional.html`:
```html
{% extends "base.html" %}
{% block title %}Cadastro Profissional{% endblock %}
{% block content %}
  <div class="container">
    <h2>Cadastro de Profissional</h2>
    <form method="post" action="{{ url_for('register_profissional') }}">
      <input type="text" name="nome" placeholder="Nome" required>
      <input type="email" name="email" placeholder="Email" required>
      <input type="password" name="senha" placeholder="Senha" required>
      <input type="text" name="especialidades" placeholder="Especialidades (separadas por vírgula)" required>
      <button type="submit">Cadastrar</button>
    </form>
    <p>Já tem conta? <a href="{{ url_for('login') }}">Fazer login</a></p>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/register_servico.html`:
```html
{% extends "base.html" %}
{% block title %}Cadastro de Serviço{% endblock %}
{% block content %}
  <div class="container">
    <h2>Cadastro de Serviço</h2>
    <form method="post" action="{{ url_for('register_servico') }}">
      <input type="text" name="nome" placeholder="Nome do serviço" required>
      <input type="number" name="duracao" placeholder="Duração (min)" required>
      <input type="number" step="0.01" name="preco" placeholder="Preço (R$)" required>
      
      <label>Profissional</label>
      <select name="profissional_id" required>
        {% for p in profissionais %}
          <option value="{{ p.id }}">{{ p.user.nome }} — {{ p.especialidades }}</option>
        {% endfor %}
      </select>

      <button type="submit">Cadastrar Serviço</button>
    </form>
  </div>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/templates/reservar.html`:
```html
{% extends "base.html" %}
{% block title %}Reservar{% endblock %}
{% block content %}
  <div class="container">
    <h2>Fazer Reserva</h2>

    {% if profissionais %}
      <form method="post" action="{{ url_for('reservar') }}">
        
        <label>Profissional</label>
        <select name="profissional_id" id="profissional_id" required>
          <option value="">-- selecione --</option>
          {% for p in profissionais %}
            <option value="{{ p.id }}">{{ p.user.nome }} — {{ p.especialidades }}</option>
          {% endfor %}
        </select>

        <label>Serviço</label>
        <select name="servico_id" id="servico_id" required>
          <option value="">-- selecione um profissional primeiro --</option>
        </select>

        <label>Data</label>
        <input type="date" name="data" id="data" required>

        <label>Hora</label>
        <input type="time" name="hora" id="hora" required>

        <div id="horarios_ocupados" style="margin-top:1rem; color: #b33;">
          <!-- Horários ocupados aparecem aqui -->
        </div>

        <button type="submit">Enviar pedido de reserva</button>
      </form>
    {% else %}
      <p>Não há profissionais disponíveis no momento para reserva.</p>
    {% endif %}
  </div>

  <script>
    // quando escolher o profissional, carregar serviços
    document.getElementById("profissional_id").addEventListener("change", carregarServicos);

    function carregarServicos() {
      let profId = document.getElementById("profissional_id").value;
      let servicoSelect = document.getElementById("servico_id");

      if (!profId) {
        servicoSelect.innerHTML = "<option value=''>-- selecione um profissional primeiro --</option>";
        return;
      }

      fetch(`/api/servicos_por_profissional?profissional_id=${profId}`)
        .then(resp => resp.json())
        .then(dados => {
          servicoSelect.innerHTML = "";
          if (dados.length > 0) {
            dados.forEach(s => {
              let opt = document.createElement("option");
              opt.value = s.id;
              opt.textContent = `${s.nome} (${s.duracao} min)`;
              servicoSelect.appendChild(opt);
            });
          } else {
            servicoSelect.innerHTML = "<option value=''>-- este profissional não tem serviços cadastrados --</option>";
          }
        })
        .catch(err => {
          servicoSelect.innerHTML = "<option value=''>Erro ao carregar serviços</option>";
        });
    }

    // horários ocupados continuam iguais
    document.getElementById("data").addEventListener("change", carregarHorarios);
    document.getElementById("profissional_id").addEventListener("change", carregarHorarios);

    function carregarHorarios() {
      let profId = document.getElementById("profissional_id").value;
      let data = document.getElementById("data").value;
      let box = document.getElementById("horarios_ocupados");

      if (!profId || !data) {
        box.innerHTML = "";
        return;
      }

      fetch(`/api/horarios_ocupados?profissional_id=${profId}&data=${data}`)
        .then(resp => resp.json())
        .then(dados => {
          if (dados.length > 0) {
            box.innerHTML = "<strong>Horários já reservados:</strong> " + dados.join(", ");
          } else {
            box.innerHTML = "<em>Todos os horários estão livres nesta data.</em>";
          }
        })
        .catch(err => {
          box.innerHTML = "<em>Erro ao carregar horários.</em>";
        });
    }
  </script>
{% endblock %}

```

---

#### Conteúdo do arquivo `Reservas-Onlines/app.py`:
```py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Cliente, Profissional, Servico, Agendamento, Notificacao
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from dateutil import parser

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon_reservas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'troque_essa_chave_para_producao'
    db.init_app(app)
    return app

app = create_app()

# -------------------------
# Helpers
# -------------------------
def current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    return User.query.get(uid)

def exige_login(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user():
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper

def checar_conflito(profissional_id, inicio: datetime, duracao_min: int):
    """Retorna True se há conflito (ou seja, horário ocupado)."""
    fim = inicio + timedelta(minutes=duracao_min)
    ags = Agendamento.query.filter_by(profissional_id=profissional_id).filter(
        Agendamento.status != 'cancelado'
    ).all()
    for a in ags:
        a_inicio = a.data_hora
        a_dur = a.servico.duracao_min if a.servico and a.servico.duracao_min else 30
        a_fim = a_inicio + timedelta(minutes=a_dur)
        if not (fim <= a_inicio or inicio >= a_fim):
            return True
    return False

# -------------------------
# Rotas públicas
# -------------------------
@app.route('/')
def index():
    user = current_user()
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        entrada = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=entrada).first()

        if not user:
            flash("Usuário não encontrado. <a href='/register_cliente'>Não tenho conta, devo me cadastrar?</a>", "danger")
            return redirect(url_for('login'))

        if not check_password_hash(user.senha_hash, senha):
            flash("Senha incorreta. Tente novamente.", "danger")
            return redirect(url_for('login'))

        session['user_id'] = user.id
        flash(f"Bem-vindo(a), {user.nome}!", "success")

        if user.perfil == 'admin':
            return redirect(url_for('dashboard_admin'))
        elif user.perfil == 'profissional':
            return redirect(url_for('dashboard_profissional'))
        else:
            return redirect(url_for('dashboard_cliente'))

    return render_template('login.html')

# -------------------------
# Cadastro Cliente
# -------------------------
@app.route('/register_cliente', methods=['GET', 'POST'])
def register_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado. Faça login.", "warning")
            return redirect(url_for('login'))

        senha_hash = generate_password_hash(senha)
        u = User(nome=nome, email=email, senha_hash=senha_hash, perfil='cliente')
        db.session.add(u)
        db.session.commit()

        c = Cliente(user=u)
        db.session.add(c)
        db.session.commit()

        flash("Cadastro de cliente realizado com sucesso! Agora faça login.", "success")
        return redirect(url_for('login'))

    return render_template('register_cliente.html')

# -------------------------
# Cadastro Profissional
# -------------------------
@app.route('/register_profissional', methods=['GET', 'POST'])
def register_profissional():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        especialidades = request.form['especialidades']

        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado. Faça login.", "warning")
            return redirect(url_for('login'))

        senha_hash = generate_password_hash(senha)
        u = User(nome=nome, email=email, senha_hash=senha_hash, perfil='profissional')
        db.session.add(u)
        db.session.commit()

        p = Profissional(especialidades=especialidades, user=u)
        db.session.add(p)
        db.session.commit()

        flash("Cadastro de profissional realizado com sucesso! Agora faça login.", "success")
        return redirect(url_for('login'))

    return render_template('register_profissional.html')

@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado. Faça login.", "warning")
            return redirect(url_for('login'))

        senha_hash = generate_password_hash(senha)
        u = User(nome=nome, email=email, senha_hash=senha_hash, perfil='admin')
        db.session.add(u)
        db.session.commit()

        flash("Cadastro de administrador realizado com sucesso! Agora faça login.", "success")
        return redirect(url_for('login'))

    return render_template('register_admin.html')

# -------------------------
# Cadastro de Serviço (apenas Admin)
# -------------------------
@app.route('/register_servico', methods=['GET', 'POST'])
@exige_login
def register_servico():
    u = current_user()
    if u.perfil != 'admin':
        flash("Apenas administradores podem cadastrar serviços.", "danger")
        return redirect(url_for('index'))

    profissionais = Profissional.query.all()

    if request.method == 'POST':
        nome = request.form['nome']
        duracao = int(request.form['duracao'])
        preco = float(request.form['preco'])
        profissional_id = int(request.form['profissional_id'])

        servico = Servico(nome=nome, duracao_min=duracao, preco=preco, profissional_id=profissional_id)
        db.session.add(servico)
        db.session.commit()

        flash("Serviço cadastrado com sucesso!", "success")
        return redirect(url_for('dashboard_admin'))

    return render_template('register_servico.html', profissionais=profissionais)


@app.route('/logout')
def logout():
    session.clear()
    flash("Deslogado com sucesso.", "info")
    return redirect(url_for('index'))

# -------------------------
# Dashboards
# -------------------------
@app.route('/dashboard/cliente')
@exige_login
def dashboard_cliente():
    u = current_user()
    if u.perfil != 'cliente':
        return redirect(url_for('index'))
    servicos = Servico.query.all()
    return render_template('dashboard_cliente.html', user=u, servicos=servicos)

@app.route('/dashboard/profissional')
@exige_login
def dashboard_profissional():
    u = current_user()
    if u.perfil != 'profissional':
        return redirect(url_for('index'))
    prof = u.profissional
    ags = Agendamento.query.filter_by(profissional_id=prof.id).order_by(Agendamento.data_hora.desc()).all()
    return render_template('dashboard_profissional.html', user=u, agendamentos=ags)

@app.route('/dashboard/admin')
@exige_login
def dashboard_admin():
    u = current_user()
    if u.perfil != 'admin':
        return redirect(url_for('index'))
    
    profissionais = Profissional.query.all()
    clientes = Cliente.query.all()
    servicos = Servico.query.all()
    ags = Agendamento.query.order_by(Agendamento.data_hora.desc()).all()
    
    return render_template(
        'dashboard_admin.html',
        user=u,
        profissionais=profissionais,
        clientes=clientes,
        servicos=servicos,
        agendamentos=ags
    )

@app.route('/reservar', methods=['GET', 'POST'])
@exige_login
def reservar():
    u = current_user()
    if u.perfil != 'cliente':
        flash("Apenas clientes podem criar reservas.", "warning")
        return redirect(url_for('index'))

    profissionais = Profissional.query.all()

    if not profissionais:
        flash("Não há profissionais disponíveis no momento para reserva.", "info")
        return redirect(url_for('dashboard_cliente'))

    if request.method == 'POST':
        servico_id = int(request.form['servico_id'])
        profissional_id = int(request.form['profissional_id'])
        data = request.form['data']
        hora = request.form['hora']

        if not data or not hora:
            flash("Data e hora são obrigatórias.", "danger")
            return redirect(url_for('reservar'))

        try:
            dt = parser.parse(f"{data} {hora}")
        except Exception:
            flash("Formato de data/hora inválido.", "danger")
            return redirect(url_for('reservar'))

        agora = datetime.now()
        if dt < agora:
            flash("Não é possível agendar para datas passadas.", "danger")
            return redirect(url_for('reservar'))

        servico = Servico.query.get(servico_id)
        if not servico:
            flash("Serviço inválido.", "danger")
            return redirect(url_for('reservar'))

        if checar_conflito(profissional_id, dt, servico.duracao_min):
            flash("Horário indisponível para esse profissional. Escolha outro.", "warning")
            return redirect(url_for('reservar'))

        # Criar agendamento
        ag = Agendamento(
            cliente_id=u.cliente.id,
            profissional_id=profissional_id,
            servico_id=servico_id,
            data_hora=dt,
            status='pendente'
        )
        db.session.add(ag)
        db.session.commit()

        profissional = Profissional.query.get(profissional_id)
        if profissional:
            reserva_mensagem = f"Novo agendamento Pendente de {u.nome} para {servico.nome} em {dt.strftime('%d/%m/%Y %H:%M')}."
            notif_prof = Notificacao(
                user_id = profissional.user.id,
                mensagem = reserva_mensagem
            )
            db.session.add(notif_prof)
        
        db.session.commit()

        flash("Reserva criada com sucesso e enviada para confirmação.", "success")
        return redirect(url_for('minhas_reservas'))

    return render_template('reservar.html', user=u, profissionais=profissionais)


@app.route('/api/servicos_por_profissional')
@exige_login
def servicos_por_profissional():
    prof_id = request.args.get('profissional_id', type=int)
    if not prof_id:
        return []
    servicos = Servico.query.filter_by(profissional_id=prof_id).all()
    return [{"id": s.id, "nome": s.nome, "duracao": s.duracao_min} for s in servicos]
    return ocupados

# -------------------------
# Minhas reservas (cliente)
# -------------------------
@app.route('/minhas-reservas')
@exige_login
def minhas_reservas():
    u = current_user()
    if u.perfil != 'cliente':
        return redirect(url_for('index'))

    ags = Agendamento.query.filter_by(cliente_id=u.cliente.id).order_by(Agendamento.data_hora.desc()).all()

    return render_template('minhas_reservas.html', user=u, agendamentos=ags)

# -------------------------
# Notificações
# -------------------------
@app.route('/notificacoes')
@exige_login
def notificacoes():
    u = current_user()
    filtro = request.args.get("filtro", "todas")

    query = Notificacao.query.filter_by(user_id=u.id).order_by(Notificacao.criado_em.desc())
    if filtro == "nao_lidas":
        query = query.filter_by(lida=False)

    notifs = query.all()
    return render_template('notificacoes.html', user=u, notificacoes=notifs)


@app.route('/notificacao/ler/<int:notif_id>')
@exige_login
def marcar_lida(notif_id):
    u = current_user()
    notif = Notificacao.query.get_or_404(notif_id)
    if notif.user_id != u.id:
        flash("Ação não permitida.", "danger")
        return redirect(url_for('notificacoes'))

    notif.lida = True
    db.session.commit()
    return redirect(url_for('notificacoes'))



# -------------------------
# Ações de confirma/cancel
# -------------------------
@app.route('/agendamento/confirmar/<int:ag_id>')
@exige_login
def confirmar_agendamento(ag_id):
    u = current_user()
    ag = Agendamento.query.get_or_404(ag_id)
    if not (u.perfil == 'admin' or (u.perfil == 'profissional' and u.profissional.id == ag.profissional_id)):
        flash("Ação não permitida.", "danger")
        return redirect(url_for('index'))
    ag.status = 'confirmado'

    mensagem_confirmacao = f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} em {ag.data_hora.strftime ('%d/%m/%Y %H:%M')} foi confirmado!"
    nova_notif = Notificacao(
        user_id = ag.cliente.user.id,
        mensagem = mensagem_confirmacao
    )
    
    ag.status = 'confirmado'

    mensagem_confirmacao = f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} em {ag.data_hora.strftime ('%d/%m/%Y %H:%M')} foi confirmado!"
    nova_notif = Notificacao(
        user_id = ag.cliente.user.id,
        mensagem = mensagem_confirmacao
    )
    
    try:
        db.session.add(nova_notif)
        db.session.commit()
        flash("Agendamento confirmado.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"ERRO AO CRIAR NOTIFICAÇÃO DE CONFIRMAÇÃO: {e}")
        flash("Agendamento confirmado, mas houve um erro ao enviar a notificação.", "warning")
        
    return redirect(request.referrer or url_for('index'))

@app.route('/agendamento/cancelar/<int:ag_id>')
@exige_login
def cancelar_agendamento(ag_id):
    u = current_user()
    ag = Agendamento.query.get_or_404(ag_id)
    if not (u.perfil == 'admin' or (u.perfil == 'profissional' and u.profissional.id == ag.profissional_id) or (u.perfil == 'cliente' and u.cliente.id == ag.cliente_id)):
        flash("Ação não permitida.", "danger")
        return redirect(url_for('index'))
    ag.status = 'cancelado'

    cancelamento_mensagem = f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} em {ag.data_hora.strftime('%d/%m/%Y %H:%M')} foi cancelado."
    nova_notif = Notificacao(
        user_id = ag.cliente.user.id,
        mensagem = cancelamento_mensagem
    )
    
    ag.status = 'cancelado'

    cancelamento_mensagem = f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} em {ag.data_hora.strftime('%d/%m/%Y %H:%M')} foi cancelado."
    nova_notif = Notificacao(
        user_id = ag.cliente.user.id,
        mensagem = cancelamento_mensagem
    )

    try:
        db.session.add(nova_notif)
        db.session.commit()
        flash("Agendamento cancelado.", "info")
    except Exception as e:
        db.session.rollback()
        print(f"ERRO AO CRIAR NOTIFICAÇÃO DE CANCELAMENTO: {e}")
        flash("Agendamento cancelado, mas houve um erro ao enviar a notificação.", "warning")

    return redirect(request.referrer or url_for('index'))

# -------------------------
# Fallback
# -------------------------
@app.route('/register')
def register_fallback():
    flash("Use as páginas corretas de cadastro: Cliente ou Profissional.", "info")
    return redirect(url_for('index'))



# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
```

---

#### Conteúdo do arquivo `Reservas-Onlines/db_create.py`:
```py
from app import create_app
from models import db

app = create_app()
app.app_context().push()

# Apagar todas as tabelas existentes
# db.drop_all()

# Criar novamente as tabelas
db.create_all()

db.session.commit()
print("Banco reinicializado e pronto para uso (sem dados pré-carregados).")


```

---

#### Conteúdo do arquivo `Reservas-Onlines/models.py`:
```py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'tb_usuarios'

    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_name', db.String(200), nullable=False)
    email = db.Column('usu_email', db.String(200), unique=True, nullable=False)
    senha_hash = db.Column('usu_senha', db.String(200), nullable=False)

    perfil = db.Column(
        'usu_tipo',
        db.Enum('cliente', 'profissional', 'admin', name='perfil_enum'),
        nullable=False,
        default='cliente'
    )

    cliente = db.relationship(
        'Cliente',
        uselist=False,
        back_populates='user',
        cascade='all, delete-orphan',
        foreign_keys='Cliente.user_id'
    )

    profissional = db.relationship(
        'Profissional',
        uselist=False,
        back_populates='user',
        cascade='all, delete-orphan',
        foreign_keys='Profissional.user_id'
    )

    notificacoes = db.relationship(
        'Notificacao',
        back_populates='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


class Cliente(db.Model):
    __tablename__ = 'tb_clientes'

    id = db.Column('cli_id', db.Integer, primary_key=True)
    user_id = db.Column('cli_usu_id', db.Integer, db.ForeignKey('tb_usuarios.usu_id'), unique=True)
    contato = db.Column('cli_contato', db.String(200))

    user = db.relationship('User', back_populates='cliente')
    agendamentos = db.relationship(
        'Agendamento',
        back_populates='cliente',
        cascade='all, delete-orphan'
    )


class Profissional(db.Model):
    __tablename__ = 'tb_profissionais'

    id = db.Column('pro_id', db.Integer, primary_key=True)
    user_id = db.Column('pro_usu_id', db.Integer, db.ForeignKey('tb_usuarios.usu_id'), unique=True)
    contato = db.Column('pro_contato', db.String(200))
    especialidades = db.Column('pro_especialidades', db.String(500))

    user = db.relationship('User', back_populates='profissional')
    servicos = db.relationship('Servico', back_populates='profissional', cascade='all, delete-orphan')
    agendamentos = db.relationship('Agendamento', back_populates='profissional', cascade='all, delete-orphan')


class Servico(db.Model):
    __tablename__ = 'tb_servicos'

    id = db.Column('ser_id', db.Integer, primary_key=True)
    nome = db.Column('ser_categoria', db.String(200), nullable=False)
    duracao_min = db.Column('ser_duracao', db.Integer, nullable=False, default=30)
    preco = db.Column('ser_preco', db.Float, nullable=True)
    profissional_id = db.Column('ser_pro_id', db.Integer, db.ForeignKey('tb_profissionais.pro_id'))

    profissional = db.relationship('Profissional', back_populates='servicos')


class Agendamento(db.Model):
    __tablename__ = 'tb_agendamentos'

    id = db.Column('age_id', db.Integer, primary_key=True)
    cliente_id = db.Column('age_cli_id', db.Integer, db.ForeignKey('tb_clientes.cli_id'))
    profissional_id = db.Column('age_pro_id', db.Integer, db.ForeignKey('tb_profissionais.pro_id'))
    servico_id = db.Column('age_ser_id', db.Integer, db.ForeignKey('tb_servicos.ser_id'))

    data_hora = db.Column('age_data_hora', db.DateTime, nullable=False)
    status = db.Column(
        'age_status',
        db.Enum('pendente', 'confirmado', 'cancelado', name='status_enum'),
        default='pendente',
        nullable=False
    )
    criado_em = db.Column('age_criacao', db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', back_populates='agendamentos')
    profissional = db.relationship('Profissional', back_populates='agendamentos')
    servico = db.relationship('Servico')


class Notificacao(db.Model):
    __tablename__ = 'tb_notificacoes'

    id = db.Column('not_id', db.Integer, primary_key=True)
    user_id = db.Column('not_usu_id', db.Integer, db.ForeignKey('tb_usuarios.usu_id'), nullable=False)
    mensagem = db.Column('not_mensagem', db.String(500), nullable=False)

    lida = db.Column('not_lida', db.Boolean, default=False)
    criado_em = db.Column('not_criado_em', db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='notificacoes')

```

---

#### Conteúdo do arquivo `Reservas-Onlines/requirements.txt`:
```txt
blinker==1.9.0
click==8.1.7
colorama==0.4.6
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
greenlet==3.2.4
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
six==1.17.0
SQLAlchemy==2.0.44
typing_extensions==4.15.0
Werkzeug==3.1.3

```

---