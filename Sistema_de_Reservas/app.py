from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from models import db, User, Cliente, Profissional, Servico, Agendamento, Notificacao, Administrador
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from dateutil import parser
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)

    # Diretório base
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'banco_de_dados', 'salon_reservas.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'troque_essa_chave_para_producao'

    # Upload de fotos de profissionais
    upload_folder = os.path.join(basedir, 'static', 'uploads', 'profissionais')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder

    # -------------------------
    # Flask-Mail / Gmail
    # -------------------------
    # Configuração fixa para o e-mail do sistema
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'sistemareservas13@gmail.com'
    # senha de app do Google SEM espaços
    app.config['MAIL_PASSWORD'] = 'wrhnhuufyjaynhlb'
    app.config['MAIL_DEFAULT_SENDER'] = 'sistemareservas13@gmail.com'

    db.init_app(app)
    return app


app = create_app()
mail = Mail(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------------
# Envio de e-mail
# -------------------------
def enviar_email(destinatario, assunto, corpo_html, corpo_texto=None):
    """Envia um e-mail. Retorna True se sucesso, False caso contrário."""
    try:
        # Se MAIL_USERNAME ou MAIL_PASSWORD não estão configurados, apenas simula o envio
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            print(f"[EMAIL SIMULADO] Para: {destinatario}, Assunto: {assunto}")
            print(f"[EMAIL SIMULADO] Corpo: {corpo_texto or corpo_html}")
            return True

        msg = Message(
            subject=assunto,
            recipients=[destinatario],
            html=corpo_html,
            body=corpo_texto
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False


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


def exige_admin(func):
    from functools import wraps

    @wraps(func)
    def wrap(*args, **kwargs):
        u = current_user()
        if not u or u.perfil != 'admin' or not u.administrador or u.administrador.status != 'aprovado':
            flash("Apenas administradores podem realizar esta ação.", "danger")
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrap


# -------------------------
# Rotas públicas
# -------------------------
@app.route('/')
def index():
    user = current_user()
    profissionais_aprovados = Profissional.query.filter_by(status='aprovado').all()
    return render_template('index.html', user=user, profissionais=profissionais_aprovados)


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

        # Regras por perfil
        if user.perfil == 'cliente':
            if not user.is_ativo:
                flash("Seu cadastro de cliente está inativo. Contate o administrador.", "warning")
                return redirect(url_for('login'))

        elif user.perfil == 'profissional':
            if not user.profissional:
                flash("Conta de profissional inválida. Contate o administrador.", "danger")
                return redirect(url_for('login'))

            if user.profissional.status == 'pendente':
                flash("Seu cadastro de profissional ainda está em análise.", "warning")
                return redirect(url_for('login'))

            if user.profissional.status == 'reprovado':
                flash("Esse profissional foi reprovado. Contate o administrador para mais informações.", "danger")
                return redirect(url_for('login'))

            if not user.is_ativo:
                flash("Seu cadastro de profissional está inativo. Contate o administrador.", "danger")
                return redirect(url_for('login'))

        elif user.perfil == 'admin':
            if not user.administrador:
                flash("Conta de administrador inválida. Contate outro administrador.", "danger")
                return redirect(url_for('login'))

            if user.administrador.status == 'pendente':
                flash("Seu cadastro de administrador ainda está em análise.", "warning")
                return redirect(url_for('login'))

            if user.administrador.status == 'reprovado':
                flash("Esse administrador foi reprovado. Contate outro administrador.", "danger")
                return redirect(url_for('login'))

            if not user.is_ativo:
                flash("Seu cadastro de administrador está inativo. Contate outro administrador.", "danger")
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
# Login / Cadastro restritos (Admin / Profissional)
# -------------------------
@app.route('/login-restrito', methods=['GET', 'POST'])
def login_restrito():
    if request.method == 'POST':
        entrada = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=entrada).first()

        if not user or not check_password_hash(user.senha_hash, senha):
            flash("Credenciais inválidas.", "danger")
            return redirect(url_for('login_restrito'))

        # Só admin ou profissional
        if user.perfil not in ('admin', 'profissional'):
            flash("Esta área é apenas para administradores e profissionais.", "warning")
            return redirect(url_for('login'))

        if user.perfil == 'profissional':
            if not user.profissional:
                flash("Conta de profissional inválida. Contate o administrador.", "danger")
                return redirect(url_for('login_restrito'))
            if user.profissional.status == 'pendente':
                flash("Seu cadastro de profissional ainda está em análise.", "warning")
                return redirect(url_for('login_restrito'))
            if user.profissional.status == 'reprovado':
                flash("Esse profissional foi reprovado. Contate o administrador para mais informações.", "danger")
                return redirect(url_for('login_restrito'))
            if not user.is_ativo:
                flash("Seu cadastro de profissional está inativo. Contate o administrador.", "danger")
                return redirect(url_for('login_restrito'))

        elif user.perfil == 'admin':
            if not user.administrador:
                flash("Conta de administrador inválida. Contate outro administrador.", "danger")
                return redirect(url_for('login_restrito'))
            if user.administrador.status == 'pendente':
                flash("Seu cadastro de administrador ainda está em análise.", "warning")
                return redirect(url_for('login_restrito'))
            if user.administrador.status == 'reprovado':
                flash("Esse administrador foi reprovado. Contate outro administrador.", "danger")
                return redirect(url_for('login_restrito'))
            if not user.is_ativo:
                flash("Seu cadastro de administrador está inativo. Contate outro administrador.", "danger")
                return redirect(url_for('login_restrito'))

        session['user_id'] = user.id
        flash(f"Bem-vindo(a), {user.nome}!", "success")

        if user.perfil == 'admin':
            return redirect(url_for('dashboard_admin'))
        else:
            return redirect(url_for('dashboard_profissional'))

    return render_template('login_restrito.html')


@app.route('/cadastro_restrito', methods=['GET', 'POST'])
def cadastro_restrito():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo_user = request.form['tipo_user']
        especialidades = request.form.get('especialidades', '')

        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "warning")
            return redirect(url_for('login_restrito'))

        senha_hash = generate_password_hash(senha)

        if tipo_user == 'profissional':
            file = request.files.get('foto_perfil')
            foto_perfil = None
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                foto_perfil = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_perfil))

            u = User(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                perfil='profissional',
                is_ativo=False
            )
            db.session.add(u)
            db.session.commit()

            p = Profissional(
                especialidades=especialidades,
                user=u,
                status='pendente',
                foto_perfil=foto_perfil
            )
            db.session.add(p)
            db.session.commit()

            admins_aprovados = Administrador.query.filter_by(status='aprovado').all()
            for adm in admins_aprovados:
                msg = f"Novo profissional {u.nome} solicitou acesso."
                db.session.add(Notificacao(
                    user_id=adm.user_id,
                    mensagem=msg,
                    tipo='pedido_profissional',
                    alvo_id=u.id
                ))
            db.session.commit()

            flash("Cadastro de profissional enviado para aprovação.", "info")
            return redirect(url_for('login_restrito'))

        elif tipo_user == 'admin':
            u = User(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                perfil='admin',
                is_ativo=False
            )
            db.session.add(u)
            db.session.commit()

            admin_sub = Administrador(user_id=u.id, nivel_acesso="geral", status='pendente')
            db.session.add(admin_sub)
            db.session.commit()

            admins_aprovados = Administrador.query.filter_by(status='aprovado').all()
            for adm in admins_aprovados:
                msg = f"Novo administrador {u.nome} solicitou acesso."
                db.session.add(Notificacao(
                    user_id=adm.user_id,
                    mensagem=msg,
                    tipo='pedido_admin',
                    alvo_id=u.id
                ))
            db.session.commit()

            flash("Cadastro de administrador enviado para aprovação.", "info")
            return redirect(url_for('login_restrito'))

        else:
            flash("Tipo de usuário inválido.", "danger")
            return redirect(url_for('cadastro_restrito'))

    return render_template('cadastro_restrito.html')


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
        u = User(nome=nome, email=email, senha_hash=senha_hash, perfil='cliente', is_ativo=True)
        db.session.add(u)
        db.session.commit()

        c = Cliente(user=u)
        db.session.add(c)
        db.session.commit()

        flash("Cadastro de cliente realizado com sucesso! Agora faça login.", "success")
        return redirect(url_for('login'))

    return render_template('register_cliente.html')


# -------------------------
# Cadastro Profissional – COM FOTO
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

        file = request.files.get('foto_perfil')
        foto_filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            foto_filename = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

        senha_hash = generate_password_hash(senha)
        u = User(nome=nome, email=email, senha_hash=senha_hash, perfil='profissional', is_ativo=False)
        db.session.add(u)
        db.session.commit()

        p = Profissional(especialidades=especialidades, user=u, status='pendente', foto_perfil=foto_filename)
        db.session.add(p)
        db.session.commit()

        admins_aprovados = Administrador.query.filter_by(status='aprovado').all()
        for adm in admins_aprovados:
            msg = f"Novo profissional {u.nome} solicitou acesso."
            db.session.add(Notificacao(
                user_id=adm.user_id,
                mensagem=msg,
                tipo='pedido_profissional',
                alvo_id=u.id
            ))
        db.session.commit()

        flash("Cadastro de profissional enviado para aprovação. Você será notificado quando for liberado.", "info")
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

        user_admin = User(nome=nome, email=email, senha_hash=senha_hash, perfil='admin', is_ativo=False)
        db.session.add(user_admin)
        db.session.commit()

        admin_sub = Administrador(user_id=user_admin.id, nivel_acesso="geral", status='pendente')
        db.session.add(admin_sub)
        db.session.commit()

        admins_aprovados = Administrador.query.filter_by(status='aprovado').all()
        for adm in admins_aprovados:
            msg = f"Novo administrador {user_admin.nome} solicitou acesso."
            db.session.add(Notificacao(
                user_id=adm.user_id,
                mensagem=msg,
                tipo='pedido_admin',
                alvo_id=user_admin.id
            ))
        db.session.commit()

        flash("Cadastro de administrador enviado para aprovação pelos administradores existentes.", "info")
        return redirect(url_for('login'))

    return render_template('register_admin.html')


# -------------------------
# Cadastro de Serviço (profissional)
# -------------------------
@app.route('/register_servico', methods=['GET', 'POST'])
@exige_login
def register_servico():
    u = current_user()
    if u.perfil != 'profissional':
        flash("Apenas profissionais podem cadastrar serviços.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form['nome']
        duracao = int(request.form['duracao'])
        preco = float(request.form['preco'])
        profissional_id = u.profissional.id

        servico = Servico(nome=nome, duracao_min=duracao, preco=preco, profissional_id=profissional_id)
        db.session.add(servico)
        db.session.commit()

        flash("Serviço cadastrado com sucesso!", "success")
        return redirect(url_for('dashboard_profissional'))

    return render_template('register_servico.html', user=u)


# -------------------------
# Logout
# -------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Deslogado com sucesso.", "info")
    return redirect(url_for('index'))


# -------------------------
# Dashboards
# -------------------------
@app.route('/dashboard_cliente')
@exige_login
def dashboard_cliente():
    u = current_user()
    if u.perfil != 'cliente':
        return redirect(url_for('index'))

    agora = datetime.now()
    agendamentos = Agendamento.query.filter_by(cliente_id=u.cliente.id).order_by(Agendamento.data_hora.desc()).all()

    proximos = [a for a in agendamentos if a.data_hora > agora and a.status != 'cancelado']
    pendentes = [a for a in agendamentos if a.status == 'pendente']
    confirmados = [a for a in agendamentos if a.status == 'confirmado']

    proximo_agendamento = proximos[0] if proximos else None

    for ag in agendamentos:
        ag.pode_cancelar = (ag.data_hora > agora and ag.status != 'cancelado')

    servicos = Servico.query.all()
    return render_template(
        'dashboard_cliente.html',
        user=u,
        servicos=servicos,
        agendamentos=agendamentos,
        proximo_agendamento=proximo_agendamento,
        total_agendamentos=len(agendamentos),
        proximos=len(proximos),
        pendentes=len(pendentes),
        confirmados=len(confirmados),
        agora=agora
    )


@app.route('/dashboard_profissional')
@exige_login
def dashboard_profissional():
    u = current_user()
    if u.perfil != 'profissional':
        return redirect(url_for('index'))

    prof = u.profissional
    ags = Agendamento.query.filter_by(profissional_id=prof.id).order_by(Agendamento.data_hora.desc()).all()

    agora = datetime.now()
    hoje = datetime.now().date()
    agendamentos_hoje = [a for a in ags if a.data_hora.date() == hoje and a.status != 'cancelado']
    agendamentos_semana = [
        a for a in ags
        if a.data_hora.date() >= hoje and a.data_hora.date() <= hoje + timedelta(days=7)
        and a.status != 'cancelado'
    ]
    pendentes = [a for a in ags if a.status == 'pendente']
    confirmados = [a for a in ags if a.status == 'confirmado']
    proximos = [a for a in ags if a.data_hora > agora and a.status != 'cancelado'][:5]

    return render_template(
        'dashboard_profissional.html',
        user=u,
        agendamentos=ags,
        agendamentos_hoje=len(agendamentos_hoje),
        agendamentos_semana=len(agendamentos_semana),
        pendentes=len(pendentes),
        confirmados=len(confirmados),
        proximos=proximos,
        total_servicos=len(prof.servicos)
    )


@app.route('/dashboard_admin')
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
# Reservar (cliente)
# -------------------------
@app.route('/reservar', methods=['GET', 'POST'])
@exige_login
def reservar():
    u = current_user()
    if u.perfil != 'cliente':
        flash("Apenas clientes podem criar reservas.", "warning")
        return redirect(url_for('index'))

    profissionais = Profissional.query.filter_by(status='aprovado').all()
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
        if dt <= agora:
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
            reservamensagem = (
                f"Novo agendamento pendente de {u.nome} para {servico.nome} em "
                f"{dt.strftime('%d/%m/%Y %H:%M')}."
            )
            notifprof = Notificacao(
                user_id=profissional.user.id,
                mensagem=reservamensagem,
                tipo='reserva_pendente',
                alvo_id=ag.id
            )
            db.session.add(notifprof)
            db.session.commit()

        assunto = "Reserva Criada com Sucesso"
        corpohtml = f"""
        <html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #8B5E3C;">Reserva Criada com Sucesso!</h2>
        <p>Olá, <strong>{u.nome}</strong>!</p>
        <p>Sua reserva foi criada e está aguardando confirmação do profissional.</p>
        <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #8B5E3C; margin-top: 0;">Detalhes da Reserva</h3>
        <p><strong>Profissional:</strong> {profissional.user.nome}</p>
        <p><strong>Serviço:</strong> {servico.nome}</p>
        <p><strong>Data e Hora:</strong> {dt.strftime('%d/%m/%Y às %H:%M')}</p>
        <p><strong>Duração:</strong> {servico.duracao_min} minutos</p>
        <p><strong>Preço:</strong> R$ {servico.preco:.2f}</p>
        <p><strong>Status:</strong> Pendente de confirmação</p>
        </div>
        <p>Você receberá uma notificação quando o profissional confirmar ou cancelar sua reserva.</p>
        <p>Acesse o sistema para acompanhar seus agendamentos:
        <a href="{request.url_root}minhas-reservas">Minhas Reservas</a></p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="color: #666; font-size: 0.9em;">Este é um e-mail automático, por favor não responda.</p>
        <p style="color: #666; font-size: 0.9em;">Atenciosamente,<br>Equipe do Sistema de Reservas</p>
        </div></body></html>
        """
        enviar_email(u.email, assunto, corpohtml)

        flash("Reserva criada com sucesso! Um e-mail de confirmação foi enviado.", "success")
        return redirect(url_for('minhas_reservas'))

    return render_template('reservar.html', user=u, profissionais=profissionais)


# -------------------------
# APIs auxiliares (JS)
# -------------------------
@app.route('/api/servicos_por_profissional')
@exige_login
def servicos_por_profissional():
    prof_id = request.args.get('profissional_id', type=int)
    if not prof_id:
        return []
    servicos = Servico.query.filter_by(profissional_id=prof_id).all()
    return [{
        'id': s.id,
        'nome': s.nome,
        'duracao': s.duracao_min,
        'preco': s.preco or 0
    } for s in servicos]


@app.route('/api/horarios_ocupados')
@exige_login
def horarios_ocupados():
    prof_id = request.args.get('profissional_id', type=int)
    data = request.args.get('data', type=str)
    if not prof_id or not data:
        return []
    try:
        base = parser.parse(data).date()
    except Exception:
        return []
    ags = Agendamento.query.filter_by(profissional_id=prof_id).filter(Agendamento.status != 'cancelado').all()
    ocupados = [a.data_hora.strftime('%H:%M') for a in ags if a.data_hora.date() == base]
    return ocupados


# -------------------------
# Minhas Reservas (cliente)
# -------------------------
@app.route('/minhas-reservas')
@exige_login
def minhas_reservas():
    u = current_user()
    if u.perfil != 'cliente':
        return redirect(url_for('index'))
    agora = datetime.now()
    ags = Agendamento.query.filter_by(cliente_id=u.cliente.id).order_by(Agendamento.data_hora.desc()).all()
    for ag in ags:
        ag.pode_cancelar = (ag.data_hora > agora and ag.status != 'cancelado')
    return render_template('minhas_reservas.html', user=u, agendamentos=ags, agora=agora)


# -------------------------
# Notificações
# -------------------------
@app.route('/notificacoes')
@exige_login
def notificacoes():
    u = current_user()
    filtro = request.args.get('filtro', 'todas')
    query = Notificacao.query.filter_by(user_id=u.id).order_by(Notificacao.criado_em.desc())
    if filtro == 'naolidas':
        query = query.filter_by(lida=False)
    notifs = query.all()
    nao_lidas_count = sum(1 for n in notifs if not n.lida)
    return render_template('notificacoes.html', user=u, notificacoes=notifs, nao_lidas_count=nao_lidas_count)


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
    flash("Notificação marcada como lida.", "success")
    return redirect(url_for('notificacoes'))


@app.route('/notificacoes/marcar-todas-lidas')
@exige_login
def marcar_todas_lidas():
    u = current_user()
    notificacoes_naolidas = Notificacao.query.filter_by(user_id=u.id, lida=False).all()
    if notificacoes_naolidas:
        for notif in notificacoes_naolidas:
            notif.lida = True
        db.session.commit()
        flash(f"{len(notificacoes_naolidas)} notificações marcadas como lidas.", "success")
    else:
        flash("Não há notificações não lidas para marcar.", "info")
    return redirect(url_for('notificacoes'))


# -------------------------
# Aprovações / reprovações admin
# -------------------------
@app.route('/aprovar_admin/<int:user_id>')
@exige_login
@exige_admin
def aprovar_admin(user_id):
    utarget = User.query.get_or_404(user_id)
    if not utarget.administrador:
        flash("Usuário não é administrador.", "warning")
        return redirect(url_for('notificacoes'))

    utarget.is_ativo = True
    utarget.administrador.status = 'aprovado'
    db.session.add(Notificacao(user_id=utarget.id, mensagem="Seu cadastro de administrador foi aprovado."))
    db.session.commit()

    assunto = "Cadastro de Administrador Aprovado"
    corpohtml = f"""
    <html><body><h2>Parabéns, {utarget.nome}!</h2>
    <p>Seu cadastro como administrador foi <strong>aprovado</strong>.</p>
    <p>Agora você pode fazer login e acessar o painel administrativo.</p>
    <p>Acesse o sistema: <a href="{request.url_root}login">Fazer Login</a></p>
    <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p></body></html>
    """
    enviar_email(utarget.email, assunto, corpohtml)
    flash("Administrador aprovado e notificado por e-mail.", "success")
    return redirect(url_for('notificacoes'))


@app.route('/reprovar_admin/<int:user_id>')
@exige_login
@exige_admin
def reprovar_admin(user_id):
    utarget = User.query.get_or_404(user_id)
    if not utarget.administrador:
        flash("Usuário não é administrador.", "warning")
        return redirect(url_for('notificacoes'))

    utarget.is_ativo = False
    utarget.administrador.status = 'reprovado'
    db.session.add(Notificacao(user_id=utarget.id, mensagem="Seu cadastro de administrador foi reprovado."))
    db.session.commit()

    assunto = "Cadastro de Administrador Reprovado"
    corpohtml = f"""
    <html><body><h2>Olá, {utarget.nome}</h2>
    <p>Infelizmente, seu cadastro como administrador foi <strong>reprovado</strong>.</p>
    <p>Para mais informações, entre em contato com outros administradores do sistema.</p>
    <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p></body></html>
    """
    enviar_email(utarget.email, assunto, corpohtml)
    flash("Administrador reprovado e notificado por e-mail.", "info")
    return redirect(url_for('notificacoes'))


@app.route('/aprovar_profissional/<int:user_id>')
@exige_login
@exige_admin
def aprovar_profissional(user_id):
    utarget = User.query.get_or_404(user_id)
    if not utarget.profissional:
        flash("Usuário não é profissional.", "warning")
        return redirect(url_for('notificacoes'))

    utarget.is_ativo = True
    utarget.profissional.status = 'aprovado'
    db.session.add(Notificacao(user_id=utarget.id, mensagem="Seu cadastro de profissional foi aprovado."))
    db.session.commit()

    assunto = "Cadastro de Profissional Aprovado"
    corpohtml = f"""
    <html><body><h2>Parabéns, {utarget.nome}!</h2>
    <p>Seu cadastro como profissional foi <strong>aprovado</strong> pelo administrador.</p>
    <p>Agora você pode fazer login e começar a gerenciar seus serviços e agendamentos.</p>
    <p>Acesse o sistema: <a href="{request.url_root}login">Fazer Login</a></p>
    <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p></body></html>
    """
    enviar_email(utarget.email, assunto, corpohtml)
    flash("Profissional aprovado e notificado por e-mail.", "success")
    return redirect(url_for('notificacoes'))


@app.route('/reprovar_profissional/<int:user_id>')
@exige_login
@exige_admin
def reprovar_profissional(user_id):
    utarget = User.query.get_or_404(user_id)
    if not utarget.profissional:
        flash("Usuário não é profissional.", "warning")
        return redirect(url_for('notificacoes'))

    utarget.is_ativo = False
    utarget.profissional.status = 'reprovado'
    db.session.add(Notificacao(user_id=utarget.id, mensagem="Seu cadastro de profissional foi reprovado."))
    db.session.commit()

    assunto = "Cadastro de Profissional Reprovado"
    corpohtml = f"""
    <html><body><h2>Olá, {utarget.nome}</h2>
    <p>Infelizmente, seu cadastro como profissional foi <strong>reprovado</strong> pelo administrador.</p>
    <p>Para mais informações, entre em contato com a administração do sistema.</p>
    <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p></body></html>
    """
    enviar_email(utarget.email, assunto, corpohtml)
    flash("Profissional reprovado e notificado por e-mail.", "info")
    return redirect(url_for('notificacoes'))


@app.route('/reconsiderar_profissional/<int:user_id>')
@exige_login
@exige_admin
def reconsiderar_profissional(user_id):
    utarget = User.query.get_or_404(user_id)
    if not utarget.profissional:
        flash("Usuário não é profissional.", "warning")
        return redirect(url_for('painel_usuarios'))

    utarget.profissional.status = 'pendente'
    utarget.is_ativo = False
    db.session.add(Notificacao(
        user_id=utarget.id,
        mensagem="Seu cadastro de profissional foi reconsiderado e está novamente em análise."
    ))
    db.session.commit()
    flash("Profissional movido para pendente.", "info")
    return redirect(url_for('painel_usuarios'))


@app.route('/reconsiderar_admin/<int:user_id>')
@exige_login
@exige_admin
def reconsiderar_admin(user_id):
    utarget = User.query.get_or_404(user_id)
    if not utarget.administrador:
        flash("Usuário não é administrador.", "warning")
        return redirect(url_for('painel_usuarios'))

    utarget.administrador.status = 'pendente'
    utarget.is_ativo = False
    db.session.add(Notificacao(
        user_id=utarget.id,
        mensagem="Seu cadastro de administrador foi reconsiderado e está novamente em análise."
    ))
    db.session.commit()
    flash("Administrador movido para pendente.", "info")
    return redirect(url_for('painel_usuarios'))


# -------------------------
# Painel de Usuários (ADMIN)
# -------------------------
@app.route('/admin/usuarios')
@exige_login
@exige_admin
def painel_usuarios():
    u = current_user()
    usuarios = User.query.all()
    return render_template('painel_usuarios.html', user=u, usuarios=usuarios)


@app.route('/admin/usuarios/criar', methods=['GET', 'POST'])
@exige_login
@exige_admin
def criar_usuario():
    u = current_user()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        perfil = request.form['perfil']
        especialidades = request.form.get('especialidades', '')

        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "warning")
            return redirect(url_for('criar_usuario'))

        senha_hash = generate_password_hash(senha)
        novo_user = User(nome=nome, email=email, senha_hash=senha_hash, perfil=perfil, is_ativo=True)
        db.session.add(novo_user)
        db.session.commit()

        if perfil == 'cliente':
            c = Cliente(user=novo_user)
            db.session.add(c)
        elif perfil == 'profissional':
            p = Profissional(user=novo_user, especialidades=especialidades, status='aprovado')
            db.session.add(p)
        elif perfil == 'admin':
            adm = Administrador(user_id=novo_user.id, nivel_acesso="geral", status='aprovado')
            db.session.add(adm)
        db.session.commit()

        flash(f"Usuário {nome} criado com sucesso!", "success")
        return redirect(url_for('painel_usuarios'))

    return render_template('criar_usuario.html', user=u)


@app.route('/admin/usuarios/editar/<int:user_id>', methods=['GET', 'POST'])
@exige_login
@exige_admin
def editar_usuario(user_id):
    u = current_user()
    utarget = User.query.get_or_404(user_id)

    adminspadraoemails = [
        "anafrancisca@gmail.com",
        "estelaaurea@gmail.com",
        "mariajesus@gmail.com",
        "samarafernanda@gmail.com",
        "sthefdantas@gmail.com",
    ]
    if utarget.email in adminspadraoemails:
        flash("Não é possível editar administradores padrão.", "warning")
        return redirect(url_for('painel_usuarios'))

    if request.method == 'POST':
        utarget.nome = request.form['nome']
        novoemail = request.form['email']

        if novoemail != utarget.email:
            if User.query.filter_by(email=novoemail).first():
                flash("Email já cadastrado para outro usuário.", "warning")
                return redirect(url_for('editar_usuario', user_id=user_id))
            utarget.email = novoemail

        utarget.is_ativo = bool(request.form.get('is_ativo') == 'on')

        if utarget.perfil == 'profissional' and utarget.profissional:
            utarget.profissional.especialidades = request.form.get('especialidades', '')

        if request.form.get('senha'):
            utarget.senha_hash = generate_password_hash(request.form['senha'])

        db.session.commit()
        flash(f"Usuário {utarget.nome} atualizado com sucesso!", "success")
        return redirect(url_for('painel_usuarios'))

    return render_template('editar_usuario.html', user=u, usuario_editado=utarget)


@app.route('/admin/usuarios/excluir/<int:user_id>', methods=['POST'])
@exige_login
@exige_admin
def excluir_usuario(user_id):
    utarget = User.query.get_or_404(user_id)
    adminspadraoemails = [
        "anafrancisca@gmail.com",
        "estelaaurea@gmail.com",
        "mariajesus@gmail.com",
        "samarafernanda@gmail.com",
        "sthefdantas@gmail.com",
    ]
    if utarget.email in adminspadraoemails:
        flash("Não é possível excluir administradores padrão.", "warning")
        return redirect(url_for('painel_usuarios'))

    nomeusuario = utarget.nome
    db.session.delete(utarget)
    db.session.commit()
    flash(f"Usuário {nomeusuario} excluído com sucesso!", "success")
    return redirect(url_for('painel_usuarios'))


@app.route('/admin/usuarios/limpar', methods=['POST'])
@exige_login
@exige_admin
def limpar_usuarios():
    adminspadraoemails = [
        "anafrancisca@gmail.com",
        "estelaaurea@gmail.com",
        "mariajesus@gmail.com",
        "samarafernanda@gmail.com",
        "sthefdantas@gmail.com",
    ]
    usuarios_para_apagar = User.query.filter(~User.email.in_(adminspadraoemails)).all()
    for u in usuarios_para_apagar:
        db.session.delete(u)
    db.session.commit()
    flash("Todos os usuários exceto os administradores padrão foram removidos.", "info")
    return redirect(url_for('painel_usuarios'))


# -------------------------
# Agendamento: confirmar / cancelar
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
    mensagemconfirmacao = (
        f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} em "
        f"{ag.data_hora.strftime('%d/%m/%Y às %H:%M')} foi CONFIRMADO e está marcado!"
    )
    novanotif = Notificacao(user_id=ag.cliente.user.id, mensagem=mensagemconfirmacao)
    try:
        db.session.add(novanotif)
        db.session.commit()

        assunto = "Agendamento Confirmado - Reserva Marcada"
        corpohtml = f"""
        <html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #28a745;">Agendamento Confirmado!</h2>
        <p>Olá, <strong>{ag.cliente.user.nome}</strong>!</p>
        <p style="font-size: 1.1em; color: #28a745; font-weight: bold;">
        Seu agendamento foi <strong>CONFIRMADO</strong> pelo profissional e está marcado!</p>
        <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #155724; margin-top: 0;">Detalhes do Agendamento Confirmado</h3>
        <p><strong>Profissional:</strong> {ag.profissional.user.nome}</p>
        <p><strong>Serviço:</strong> {ag.servico.nome}</p>
        <p><strong>Data e Hora:</strong> {ag.data_hora.strftime('%d/%m/%Y às %H:%M')}</p>
        <p><strong>Duração:</strong> {ag.servico.duracao_min} minutos</p>
        <p><strong>Preço:</strong> R$ {ag.servico.preco:.2f}</p>
        <p style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #c3e6cb;">
        <strong style="color: #155724;">Status: CONFIRMADO E MARCADO</strong></p>
        </div>
        <p>Seu agendamento está confirmado e marcado. Lembre-se de comparecer no horário agendado!</p>
        <p>Acesse o sistema para ver todos os seus agendamentos:
        <a href="{request.url_root}minhas-reservas" style="color: #8B5E3C;">Minhas Reservas</a></p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="color: #666; font-size: 0.9em;">Este é um e-mail automático, por favor não responda.</p>
        <p style="color: #666; font-size: 0.9em;">Atenciosamente,<br>Equipe do Sistema de Reservas</p>
        </div></body></html>
        """
        enviar_email(ag.cliente.user.email, assunto, corpohtml)
        flash("Agendamento confirmado e cliente notificado por e-mail.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"ERRO AO CONFIRMAR AGENDAMENTO: {e}")
        flash("Agendamento confirmado, mas houve um erro ao enviar a notificação/e-mail.", "warning")

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
    cancelamentomensagem = (
        f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} "
        f"em {ag.data_hora.strftime('%d/%m/%Y %H:%M')} foi cancelado."
    )
    novanotif = Notificacao(user_id=ag.cliente.user.id, mensagem=cancelamentomensagem)
    try:
        db.session.add(novanotif)
        db.session.commit()
        flash("Agendamento cancelado.", "info")
    except Exception as e:
        db.session.rollback()
        print(f"ERRO AO CRIAR NOTIFICAO DE CANCELAMENTO: {e}")
        flash("Agendamento cancelado, mas houve um erro ao enviar a notificação.", "warning")

    return redirect(request.referrer or url_for('index'))


# -------------------------
# Fallback de register errado (opcional)
# -------------------------
@app.route('/register')
def register_fallback():
    flash("Use as páginas corretas de cadastro: Cliente, Profissional ou Administrador.", "info")
    return redirect(url_for('index'))


# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
