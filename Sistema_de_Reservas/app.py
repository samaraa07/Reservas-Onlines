from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Cliente, Profissional, Servico, Agendamento, Notificacao, Administrador
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from dateutil import parser
import os


def create_app():
    app = Flask(__name__)

    # Define o diretório base do projeto
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Caminho do banco de dados dentro da pasta 'banco_de_dados'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'banco_de_dados', 'salon_reservas.db')}"

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


@app.route('/login', methods=['GET', 'POST'])
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


# -------------------------
# Cadastro Administrador
# -------------------------
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

        # Cria o usuário principal
        user_admin = User(nome=nome, email=email, senha_hash=senha_hash, perfil='admin')
        db.session.add(user_admin)
        db.session.commit()

        # Cria também o registro na tabela Administradores
        admin_sub = Administrador(user_id=user_admin.id, nivel_acesso="geral")
        db.session.add(admin_sub)
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


# -------------------------
# Reservas
# -------------------------
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
            reserva_mensagem = f"Novo agendamento pendente de {u.nome} para {servico.nome} em {dt.strftime('%d/%m/%Y %H:%M')}."
            notif_prof = Notificacao(user_id=profissional.user.id, mensagem=reserva_mensagem)
            db.session.add(notif_prof)

        db.session.commit()

        flash("Reserva criada com sucesso e enviada para confirmação.", "success")
        return redirect(url_for('minhas_reservas'))

    return render_template('reservar.html', user=u, profissionais=profissionais)


# -------------------------
# API auxiliar
# -------------------------
@app.route('/api/servicos_por_profissional')
@exige_login
def servicos_por_profissional():
    prof_id = request.args.get('profissional_id', type=int)
    if not prof_id:
        return []
    servicos = Servico.query.filter_by(profissional_id=prof_id).all()
    return [{"id": s.id, "nome": s.nome, "duracao": s.duracao_min} for s in servicos]


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
# Ações confirmar/cancelar agendamento
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

    mensagem_confirmacao = f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} em {ag.data_hora.strftime('%d/%m/%Y %H:%M')} foi confirmado!"
    nova_notif = Notificacao(user_id=ag.cliente.user.id, mensagem=mensagem_confirmacao)

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
    if not (
        u.perfil == 'admin'
        or (u.perfil == 'profissional' and u.profissional.id == ag.profissional_id)
        or (u.perfil == 'cliente' and u.cliente.id == ag.cliente_id)
    ):
        flash("Ação não permitida.", "danger")
        return redirect(url_for('index'))

    ag.status = 'cancelado'

    cancelamento_mensagem = f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} em {ag.data_hora.strftime('%d/%m/%Y %H:%M')} foi cancelado."
    nova_notif = Notificacao(user_id=ag.cliente.user.id, mensagem=cancelamento_mensagem)

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
# Painel de Usuários (somente administradores)
# -------------------------
@app.route('/admin/usuarios')
@exige_login
def painel_usuarios():
    u = current_user()
    if u.perfil != 'admin':
        flash("Apenas administradores podem acessar o painel de usuários.", "danger")
        return redirect(url_for('index'))

    usuarios = User.query.all()
    return render_template('painel_usuarios.html', user=u, usuarios=usuarios)

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
