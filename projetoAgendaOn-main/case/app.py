from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
import json
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

reservas = []
USUARIOS_FILE = 'usuarios.json'

# Funções para carregar e salvar usuários
def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=2)

# Página inicial
@app.route('/')
def pagina_inicial():
    return render_template('pageStart.html')

# Login: pode usar nome ou email
@app.route('/login', methods=['POST'])
def login():
    usuarios = carregar_usuarios()
    entrada = request.form['usuario']
    senha = request.form['senha']

    for u in usuarios:
        if (entrada == u['nome'] or entrada == u['email']) and senha == u['senha']:
            session['usuario'] = u['nome']
            return redirect(url_for('painel_profissional'))

    flash("Usuário ou senha inválidos.", "message")  # Corrigido: categoria "message"
    return redirect(url_for('pagina_inicial') + "?aba=login")  # Corrigido: manter aba de login ativa

# Cadastro
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

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        data = request.form['data']
        hora = request.form['hora']
        tipo = request.form['tipo']

        if not nome or not email or not data or not hora or not tipo:
            erro = "Todos os campos são obrigatórios."
            return render_template('reservas.html', erro=erro)

        reservas.append({
            'usuario': session['usuario'],
            'nome': nome,
            'email': email,
            'data': data,
            'hora': hora,
            'tipo': tipo
        })

        return redirect(url_for('ver_reservas'))

    return render_template('reservas.html')

@app.route('/reservas')
def ver_reservas():
    if 'usuario' not in session:
        return redirect(url_for('pagina_inicial'))

    minhas_reservas = [r for r in reservas if r.get('usuario') == session['usuario']]
    return render_template('lista_reservas.html', reservas=minhas_reservas)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('pagina_inicial') + "?aba=login")


if __name__ == '__main__':
    app.run(debug=True)
