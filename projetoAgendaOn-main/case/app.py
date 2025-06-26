from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

usuarios = {}
reservas = []  # Lista temporária de reservas

@app.route('/')
def pagina_inicial():
    return render_template('pageStart.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = get_flashed_messages()
    erro = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('painel_profissional'))
        else:
            erro = "Usuário ou senha inválidos."
    return render_template('login.html', erro=erro, sucesso=mensagem[0] if mensagem else "")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    erro = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in usuarios:
            erro = "Usuário já cadastrado."
        else:
            usuarios[usuario] = senha
            flash("Cadastro realizado com sucesso! Faça login.")
            return redirect(url_for('login'))
    return render_template('cadastro.html', erro=erro)

@app.route('/painel')
def painel_profissional():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('painel.html', usuario=session['usuario'])

@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if 'usuario' not in session:
        return redirect(url_for('login'))

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
        return redirect(url_for('login'))

    minhas_reservas = [r for r in reservas if r.get('usuario') == session['usuario']]
    return render_template('lista_reservas.html', reservas=minhas_reservas)

if __name__ == '__main__':
    app.run(debug=True)
