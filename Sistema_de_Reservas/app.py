from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
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

    # Configuração do Flask-Mail
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

    db.init_app(app)
    return app


app = create_app()
mail = Mail(app)


# -------------------------
# Helper para envio de e-mail
# -------------------------
def enviar_email(destinatario, assunto, corpo_html, corpo_texto=None):
    """Envia um e-mail. Retorna True se sucesso, False caso contrário."""
    try:
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            # Se não configurado, apenas loga (para desenvolvimento)
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

        # Regras de ativação/aprovação por perfil
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

        # Só admin ou profissional podem entrar aqui
        if user.perfil not in ('admin', 'profissional'):
            flash("Esta área é apenas para administradores e profissionais.", "warning")
            return redirect(url_for('login'))

        # Regras específicas para profissional
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

        # Regras específicas para admin
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

        # Se passou por tudo, loga
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
        foto_perfil = request.form.get('foto_perfil', '')  # <-- NOVO

        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "warning")
            return redirect(url_for('login_restrito'))

        senha_hash = generate_password_hash(senha)

        if tipo_user == 'profissional':
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
                foto_perfil=foto_perfil   # <-- NOVO
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
# Cadastro Profissional (pendente)
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
        u = User(nome=nome, email=email, senha_hash=senha_hash, perfil='profissional', is_ativo=False)
        db.session.add(u)
        db.session.commit()

        p = Profissional(especialidades=especialidades, user=u, status='pendente')
        db.session.add(p)
        db.session.commit()

        # Notificar admins aprovados sobre novo profissional
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
# Cadastro Administrador (pendente)
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

        # Notificar admins aprovados sobre novo administrador
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
# Cadastro de Serviço (apenas para Profissionais)
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
        profissional_id = u.profissional.id  # Usa o ID do profissional logado

        servico = Servico(nome=nome, duracao_min=duracao, preco=preco, profissional_id=profissional_id)
        db.session.add(servico)
        db.session.commit()

        flash("Serviço cadastrado com sucesso!", "success")
        return redirect(url_for('dashboard_profissional'))

    return render_template('register_servico.html', user=u)  # Passando a variável user


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
    
    # Buscar agendamentos do cliente
    agendamentos = Agendamento.query.filter_by(cliente_id=u.cliente.id).order_by(Agendamento.data_hora.desc()).all()
    
    # Estatísticas
    agora = datetime.now()
    proximos = [a for a in agendamentos if a.data_hora > agora and a.status != 'cancelado']
    passados = [a for a in agendamentos if a.data_hora <= agora or a.status == 'cancelado']
    pendentes = [a for a in agendamentos if a.status == 'pendente']
    confirmados = [a for a in agendamentos if a.status == 'confirmado']
    
    # Próximo agendamento
    proximo_agendamento = proximos[0] if proximos else None
    
    # Adicionar flag para verificar se pode cancelar (agendamentos futuros)
    for ag in agendamentos:
        ag.pode_cancelar = ag.data_hora > agora and ag.status != 'cancelado'
    
    servicos = Servico.query.all()
    return render_template('dashboard_cliente.html', 
                         user=u, 
                         servicos=servicos,
                         agendamentos=agendamentos,
                         proximo_agendamento=proximo_agendamento,
                         total_agendamentos=len(agendamentos),
                         proximos=len(proximos),
                         pendentes=len(pendentes),
                         confirmados=len(confirmados),
                         agora=agora)


@app.route('/dashboard/profissional')
@exige_login
def dashboard_profissional():
    u = current_user()
    if u.perfil != 'profissional':
        return redirect(url_for('index'))
    prof = u.profissional
    ags = Agendamento.query.filter_by(profissional_id=prof.id).order_by(Agendamento.data_hora.desc()).all()
    
    # Estatísticas
    agora = datetime.now()
    hoje = datetime.now().date()
    
    agendamentos_hoje = [a for a in ags if a.data_hora.date() == hoje and a.status != 'cancelado']
    agendamentos_semana = [a for a in ags if a.data_hora.date() >= hoje and a.data_hora.date() <= (hoje + timedelta(days=7)) and a.status != 'cancelado']
    pendentes = [a for a in ags if a.status == 'pendente']
    confirmados = [a for a in ags if a.status == 'confirmado']
    
    # Próximos agendamentos
    proximos = [a for a in ags if a.data_hora > agora and a.status != 'cancelado'][:5]
    
    return render_template('dashboard_profissional.html', 
                         user=u, 
                         agendamentos=ags,
                         agendamentos_hoje=len(agendamentos_hoje),
                         agendamentos_semana=len(agendamentos_semana),
                         pendentes=len(pendentes),
                         confirmados=len(confirmados),
                         proximos=proximos,
                         total_servicos=len(prof.servicos))


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

    # Apenas profissionais aprovados podem receber reservas
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

        # Enviar e-mail de confirmação para o cliente
        assunto = "Reserva Criada com Sucesso"
        corpo_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #8B5E3C;">Reserva Criada com Sucesso!</h2>
                <p>Olá, <strong>{u.nome}</strong>!</p>
                <p>Sua reserva foi criada e está aguardando confirmação do profissional.</p>
                
                <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #8B5E3C; margin-top: 0;">Detalhes da Reserva:</h3>
                    <p><strong>Profissional:</strong> {profissional.user.nome}</p>
                    <p><strong>Serviço:</strong> {servico.nome}</p>
                    <p><strong>Data e Hora:</strong> {dt.strftime('%d/%m/%Y às %H:%M')}</p>
                    <p><strong>Duração:</strong> {servico.duracao_min} minutos</p>
                    {f'<p><strong>Preço:</strong> R$ {servico.preco:.2f}</p>' if servico.preco else ''}
                    <p><strong>Status:</strong> Pendente de confirmação</p>
                </div>
                
                <p>Você receberá uma notificação quando o profissional confirmar ou cancelar sua reserva.</p>
                <p>Acesse o sistema para acompanhar seus agendamentos: <a href="{request.url_root}minhas-reservas">Minhas Reservas</a></p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="color: #666; font-size: 0.9em;">Este é um e-mail automático, por favor não responda.</p>
                <p style="color: #666; font-size: 0.9em;">Atenciosamente,<br>Equipe do Sistema de Reservas</p>
            </div>
        </body>
        </html>
        """
        enviar_email(u.email, assunto, corpo_html)

        flash("Reserva criada com sucesso! Um e-mail de confirmação foi enviado.", "success")
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
    return [{"id": s.id, "nome": s.nome, "duracao": s.duracao_min, "preco": s.preco or 0} for s in servicos]


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
    ocupados = []
    for a in ags:
        if a.data_hora.date() == base:
            ocupados.append(a.data_hora.strftime('%H:%M'))
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

    agora = datetime.now()
    ags = Agendamento.query.filter_by(cliente_id=u.cliente.id).order_by(Agendamento.data_hora.desc()).all()
    
    # Adicionar flag para verificar se pode cancelar (agendamentos futuros)
    for ag in ags:
        ag.pode_cancelar = ag.data_hora > agora and ag.status != 'cancelado'
    
    return render_template('minhas_reservas.html', user=u, agendamentos=ags, agora=agora)


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
    
    # Contar notificações não lidas para o botão "marcar todas"
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
    notificacoes_nao_lidas = Notificacao.query.filter_by(user_id=u.id, lida=False).all()
    
    if notificacoes_nao_lidas:
        for notif in notificacoes_nao_lidas:
            notif.lida = True
        db.session.commit()
        flash(f"{len(notificacoes_nao_lidas)} notificação(ões) marcada(s) como lida(s).", "success")
    else:
        flash("Não há notificações não lidas para marcar.", "info")
    
    return redirect(url_for('notificacoes'))


# -------------------------
# Aprovação/Reprovação de cadastros (somente admin)
# -------------------------
@app.route('/aprovar_admin/<int:user_id>')
@exige_login
@exige_admin
def aprovar_admin(user_id):
    u_target = User.query.get_or_404(user_id)
    if not u_target.administrador:
        flash("Usuário não é administrador.", "warning")
        return redirect(url_for('notificacoes'))

    u_target.is_ativo = True
    u_target.administrador.status = 'aprovado'
    db.session.add(Notificacao(user_id=u_target.id, mensagem="Seu cadastro de administrador foi aprovado."))
    db.session.commit()
    
    # Enviar e-mail de aprovação
    assunto = "Cadastro de Administrador Aprovado"
    corpo_html = f"""
    <html>
    <body>
        <h2>Parabéns, {u_target.nome}!</h2>
        <p>Seu cadastro como administrador foi <strong>aprovado</strong>.</p>
        <p>Agora você pode fazer login e acessar o painel administrativo.</p>
        <p>Acesse o sistema: <a href="{request.url_root}login">Fazer Login</a></p>
        <br>
        <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p>
    </body>
    </html>
    """
    enviar_email(u_target.email, assunto, corpo_html)
    
    flash("Administrador aprovado e notificado por e-mail.", "success")
    return redirect(url_for('notificacoes'))


@app.route('/reprovar_admin/<int:user_id>')
@exige_login
@exige_admin
def reprovar_admin(user_id):
    u_target = User.query.get_or_404(user_id)
    if not u_target.administrador:
        flash("Usuário não é administrador.", "warning")
        return redirect(url_for('notificacoes'))

    u_target.is_ativo = False
    u_target.administrador.status = 'reprovado'
    db.session.add(Notificacao(user_id=u_target.id, mensagem="Seu cadastro de administrador foi reprovado."))
    db.session.commit()
    
    # Enviar e-mail de reprovação
    assunto = "Cadastro de Administrador Reprovado"
    corpo_html = f"""
    <html>
    <body>
        <h2>Olá, {u_target.nome}</h2>
        <p>Infelizmente, seu cadastro como administrador foi <strong>reprovado</strong>.</p>
        <p>Para mais informações, entre em contato com outros administradores do sistema.</p>
        <br>
        <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p>
    </body>
    </html>
    """
    enviar_email(u_target.email, assunto, corpo_html)
    
    flash("Administrador reprovado e notificado por e-mail.", "info")
    return redirect(url_for('notificacoes'))


@app.route('/aprovar_profissional/<int:user_id>')
@exige_login
@exige_admin
def aprovar_profissional(user_id):
    u_target = User.query.get_or_404(user_id)
    if not u_target.profissional:
        flash("Usuário não é profissional.", "warning")
        return redirect(url_for('notificacoes'))

    u_target.is_ativo = True
    u_target.profissional.status = 'aprovado'
    db.session.add(Notificacao(user_id=u_target.id, mensagem="Seu cadastro de profissional foi aprovado."))
    db.session.commit()
    
    # Enviar e-mail de aprovação
    assunto = "Cadastro de Profissional Aprovado"
    corpo_html = f"""
    <html>
    <body>
        <h2>Parabéns, {u_target.nome}!</h2>
        <p>Seu cadastro como profissional foi <strong>aprovado</strong> pelo administrador.</p>
        <p>Agora você pode fazer login e começar a gerenciar seus serviços e agendamentos.</p>
        <p>Acesse o sistema: <a href="{request.url_root}login">Fazer Login</a></p>
        <br>
        <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p>
    </body>
    </html>
    """
    enviar_email(u_target.email, assunto, corpo_html)
    
    flash("Profissional aprovado e notificado por e-mail.", "success")
    return redirect(url_for('notificacoes'))


@app.route('/reprovar_profissional/<int:user_id>')
@exige_login
@exige_admin
def reprovar_profissional(user_id):
    u_target = User.query.get_or_404(user_id)
    if not u_target.profissional:
        flash("Usuário não é profissional.", "warning")
        return redirect(url_for('notificacoes'))

    u_target.is_ativo = False
    u_target.profissional.status = 'reprovado'
    db.session.add(Notificacao(user_id=u_target.id, mensagem="Seu cadastro de profissional foi reprovado."))
    db.session.commit()
    
    # Enviar e-mail de reprovação
    assunto = "Cadastro de Profissional Reprovado"
    corpo_html = f"""
    <html>
    <body>
        <h2>Olá, {u_target.nome}</h2>
        <p>Infelizmente, seu cadastro como profissional foi <strong>reprovado</strong> pelo administrador.</p>
        <p>Para mais informações, entre em contato com a administração do sistema.</p>
        <br>
        <p>Atenciosamente,<br>Equipe do Sistema de Reservas</p>
    </body>
    </html>
    """
    enviar_email(u_target.email, assunto, corpo_html)
    
    flash("Profissional reprovado e notificado por e-mail.", "info")
    return redirect(url_for('notificacoes'))

@app.route('/reconsiderar_profissional/<int:user_id>')
@exige_login
@exige_admin
def reconsiderar_profissional(user_id):
    u_target = User.query.get_or_404(user_id)
    if not u_target.profissional:
        flash("Usuário não é profissional.", "warning")
        return redirect(url_for('painel_usuarios'))

    u_target.profissional.status = 'pendente'
    u_target.is_ativo = False
    db.session.add(Notificacao(
        user_id=u_target.id,
        mensagem="Seu cadastro de profissional foi reconsiderado e está novamente em análise."
    ))
    db.session.commit()
    flash("Profissional movido para pendente.", "info")
    return redirect(url_for('painel_usuarios'))


@app.route('/reconsiderar_admin/<int:user_id>')
@exige_login
@exige_admin
def reconsiderar_admin(user_id):
    u_target = User.query.get_or_404(user_id)
    if not u_target.administrador:
        flash("Usuário não é administrador.", "warning")
        return redirect(url_for('painel_usuarios'))

    u_target.administrador.status = 'pendente'
    u_target.is_ativo = False
    db.session.add(Notificacao(
        user_id=u_target.id,
        mensagem="Seu cadastro de administrador foi reconsiderado e está novamente em análise."
    ))
    db.session.commit()
    flash("Administrador movido para pendente.", "info")
    return redirect(url_for('painel_usuarios'))


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

    # Atualizar status para confirmado
    ag.status = 'confirmado'

    # Criar notificação para o cliente
    mensagem_confirmacao = (
        f"✅ Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} "
        f"em {ag.data_hora.strftime('%d/%m/%Y às %H:%M')} foi CONFIRMADO e está marcado!"
    )
    nova_notif = Notificacao(user_id=ag.cliente.user.id, mensagem=mensagem_confirmacao)

    try:
        db.session.add(nova_notif)
        db.session.commit()
        
        # Enviar e-mail de confirmação para o cliente
        assunto = "Agendamento Confirmado - Reserva Marcada"
        corpo_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #28a745;">✅ Agendamento Confirmado!</h2>
                <p>Olá, <strong>{ag.cliente.user.nome}</strong>!</p>
                <p style="font-size: 1.1em; color: #28a745; font-weight: bold;">
                    Seu agendamento foi <strong>CONFIRMADO</strong> pelo profissional e está marcado!
                </p>
                
                <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #155724; margin-top: 0;">📅 Detalhes do Agendamento Confirmado:</h3>
                    <p><strong>Profissional:</strong> {ag.profissional.user.nome}</p>
                    <p><strong>Serviço:</strong> {ag.servico.nome}</p>
                    <p><strong>Data e Hora:</strong> {ag.data_hora.strftime('%d/%m/%Y às %H:%M')}</p>
                    <p><strong>Duração:</strong> {ag.servico.duracao_min} minutos</p>
                    {f'<p><strong>Preço:</strong> R$ {ag.servico.preco:.2f}</p>' if ag.servico.preco else ''}
                    <p style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #c3e6cb;">
                        <strong style="color: #155724;">Status: ✅ CONFIRMADO E MARCADO</strong>
                    </p>
                </div>
                
                <p>Seu agendamento está confirmado e marcado. Lembre-se de comparecer no horário agendado!</p>
                <p>Acesse o sistema para ver todos os seus agendamentos: <a href="{request.url_root}minhas-reservas" style="color: #8B5E3C;">Minhas Reservas</a></p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="color: #666; font-size: 0.9em;">Este é um e-mail automático, por favor não responda.</p>
                <p style="color: #666; font-size: 0.9em;">Atenciosamente,<br>Equipe do Sistema de Reservas</p>
            </div>
        </body>
        </html>
        """
        enviar_email(ag.cliente.user.email, assunto, corpo_html)
        
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

    cancelamento_mensagem = (
        f"Seu agendamento de {ag.servico.nome} com {ag.profissional.user.nome} "
        f"em {ag.data_hora.strftime('%d/%m/%Y %H:%M')} foi cancelado."
    )
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
# Limpar usuários (exceto admins padrão)
# -------------------------
@app.route('/admin/usuarios/limpar', methods=['POST'])
@exige_login
@exige_admin
def limpar_usuarios():
    admins_padrao_emails = [
        "anafrancisca@gmail.com",
        "estelaaurea@gmail.com",
        "mariajesus@gmail.com",
        "samarafernanda@gmail.com",
        "sthefdantas@gmail.com",
    ]

    usuarios_para_apagar = User.query.filter(
        ~User.email.in_(admins_padrao_emails)
    ).all()

    for u in usuarios_para_apagar:
        db.session.delete(u)

    db.session.commit()

    flash("Todos os usuários (exceto os administradores padrão) foram removidos.", "info")
    return redirect(url_for('painel_usuarios'))


# -------------------------
# CRUD de Usuários (somente administradores)
# -------------------------
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
    u_target = User.query.get_or_404(user_id)
    
    # Proteger admins padrão
    admins_padrao_emails = [
        "anafrancisca@gmail.com",
        "estelaaurea@gmail.com",
        "mariajesus@gmail.com",
        "samarafernanda@gmail.com",
        "sthefdantas@gmail.com",
    ]
    if u_target.email in admins_padrao_emails:
        flash("Não é possível editar administradores padrão.", "warning")
        return redirect(url_for('painel_usuarios'))
    
    if request.method == 'POST':
        u_target.nome = request.form['nome']
        novo_email = request.form['email']
        
        # Verificar se o email já existe em outro usuário
        if novo_email != u_target.email:
            if User.query.filter_by(email=novo_email).first():
                flash("Email já cadastrado para outro usuário.", "warning")
                return redirect(url_for('editar_usuario', user_id=user_id))
            u_target.email = novo_email
        
        # Atualizar senha se fornecida
        if request.form.get('senha'):
            u_target.senha_hash = generate_password_hash(request.form['senha'])
        
        # Atualizar campos específicos do perfil
        if u_target.perfil == 'profissional' and u_target.profissional:
            u_target.profissional.especialidades = request.form.get('especialidades', '')
        
        # Atualizar status de ativação
        u_target.is_ativo = request.form.get('is_ativo') == 'on'
        
        db.session.commit()
        flash(f"Usuário {u_target.nome} atualizado com sucesso!", "success")
        return redirect(url_for('painel_usuarios'))
    
    return render_template('editar_usuario.html', user=u, usuario_editado=u_target)


@app.route('/admin/usuarios/excluir/<int:user_id>', methods=['POST'])
@exige_login
@exige_admin
def excluir_usuario(user_id):
    u_target = User.query.get_or_404(user_id)
    
    # Proteger admins padrão
    admins_padrao_emails = [
        "anafrancisca@gmail.com",
        "estelaaurea@gmail.com",
        "mariajesus@gmail.com",
        "samarafernanda@gmail.com",
        "sthefdantas@gmail.com",
    ]
    if u_target.email in admins_padrao_emails:
        flash("Não é possível excluir administradores padrão.", "warning")
        return redirect(url_for('painel_usuarios'))
    
    nome_usuario = u_target.nome
    db.session.delete(u_target)
    db.session.commit()
    
    flash(f"Usuário {nome_usuario} excluído com sucesso!", "success")
    return redirect(url_for('painel_usuarios'))


# -------------------------
# Fallback
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