from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from datetime import datetime, date


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

USUARIOS_FILE = 'usuarios.json'
RESERVAS_FILE = 'reservas.json'

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

def carregar_reservas():
    if os.path.exists(RESERVAS_FILE):
        with open(RESERVAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_reservas(reservas):
    with open(RESERVAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reservas, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('pageStart.html')

@app.route('/login', methods=['POST'])
def login():
    usuarios = carregar_usuarios()
    entrada = request.form['usuario'].strip()
    senha = request.form['senha']

    for u in usuarios:
        if (entrada == u['nome'] or entrada == u['email']) and senha == u['senha']:
            session['usuario'] = u['nome']
            session['email'] = u['email']
            session['tipo'] = u.get('tipo', 'usuario')  # pode ser 'usuario' ou 'admin'
            if session['tipo'] == 'admin':
                return redirect(url_for('admin_painel'))
            return redirect(url_for('painel_profissional'))

    flash("Usuário ou senha inválidos.", "message")
    return redirect(url_for('index') + "?aba=login")

@app.route('/cadastro', methods=['POST'])
def cadastro():
    usuarios = carregar_usuarios()
    nome = request.form['nome'].strip()
    email = request.form['email'].strip()
    senha = request.form['senha']

    if any(u['nome'] == nome or u['email'] == email for u in usuarios):
        flash("Usuário ou email já cadastrado.", "message")
        return redirect(url_for('index') + "?aba=cadastro")

    # por padrão o cadastro é usuário normal
    usuarios.append({'nome': nome, 'email': email, 'senha': senha, 'tipo': 'usuario'})
    salvar_usuarios(usuarios)

    flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
    return redirect(url_for('index') + "?aba=login")

@app.route('/painel')
def painel_profissional():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    if session.get('tipo') == 'admin':
        return redirect(url_for('admin_painel'))
    return render_template('painel.html', usuario=session['usuario'])

@app.route('/admin')
def admin_painel():
    if 'usuario' not in session or session.get('tipo') != 'admin':
        return redirect(url_for('index'))
    reservas = carregar_reservas()
    pendentes = [r for r in reservas if r['status'] == 'pendente']
    return render_template('admin_painel.html', reservas=pendentes)

@app.route('/admin/confirmar/<int:indice>')
def admin_confirmar(indice):
    if 'usuario' not in session or session.get('tipo') != 'admin':
        return redirect(url_for('index'))
    reservas = carregar_reservas()
    if 0 <= indice < len(reservas):
        reservas[indice]['status'] = 'confirmado'
        salvar_reservas(reservas)
        flash("Reserva confirmada com sucesso!", "sucesso")
    return redirect(url_for('admin_painel'))

@app.route('/admin/cancelar/<int:indice>')
def admin_cancelar(indice):
    if 'usuario' not in session or session.get('tipo') != 'admin':
        return redirect(url_for('index'))
    reservas = carregar_reservas()
    if 0 <= indice < len(reservas):
        reservas[indice]['status'] = 'cancelado'
        salvar_reservas(reservas)
        flash("Reserva recusada/cancelada.", "message")
    return redirect(url_for('admin_painel'))

@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if 'usuario' not in session:
        return redirect(url_for('pagina_inicial'))
    
    erro = None
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        data_str = request.form.get('data')
        hora = request.form.get('hora')
        nome = request.form.get('nome')
        email = request.form.get('email')

        if not tipo or not data_str or not hora or not nome or not email:
            erro = "Todos os campos são obrigatórios."
        else:
            data_hora = datetime.strptime(f"{data_str} {hora}", "%Y-%m-%d %H:%M")
            if data_hora < datetime.now():
                erro = "Não é possível agendar para datas e horários passados."
            else:
                flash("Reserva realizada com sucesso!", "sucesso")
                return redirect(url_for('painel_profissional'))

    return render_template('reservas.html', erro=erro, date=date)

@app.route('/reservas')
def ver_reservas():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    reservas = carregar_reservas()
    usuario = session['usuario']
    # Mostrar só as reservas do usuário e status confirmados e pendentes
    minhas = [r for r in reservas if r['usuario'] == usuario and r['status'] in ['pendente', 'confirmado']]
    return render_template('lista_reservas.html', reservas=minhas)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
