from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessária para usar session e flash

usuarios = {}

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
            session['usuario'] = usuario  # Armazena o usuário na sessão
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
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('login'))  # Se não estiver logado, redireciona

    return render_template('painel.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
