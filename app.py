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
    """
    Retorna True se há conflito (ou seja, horário ocupado).
    Considera intervalo [inicio, fim)
    """
    fim = inicio + timedelta(minutes=duracao_min)
    ags = Agendamento.query.filter_by(profissional_id=profissional_id).filter(Agendamento.status != 'cancelado').all()
    for a in ags:
        a_inicio = a.data_hora
        a_dur = a.servico.duracao_min if a.servico and a.servico.duracao_min else 30
        a_fim = a_inicio + timedelta(minutes=a_dur)
        # checar overlap
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        perfil = request.form.get('perfil', 'cliente')
        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "warning")
            return redirect(url_for('register'))

        senha_hash = generate_password_hash(senha)
        u = User(nome=nome, email=email, senha_hash=senha_hash, perfil=perfil)
        db.session.add(u)
        db.session.commit()

        if perfil == 'cliente':
            c = Cliente(contato=request.form.get('contato'), user=u)
            db.session.add(c)
        elif perfil == 'profissional':
            p = Profissional(contato=request.form.get('contato'), especialidades=request.form.get('especialidades',''), user=u)
            db.session.add(p)
        db.session.commit()

        flash("Cadastro realizado. Faça login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        entrada = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=entrada).first()
        if not user or not check_password_hash(user.senha_hash, senha):
            flash("Usuário ou senha inválidos.", "danger")
            return redirect(url_for('login'))
        session['user_id'] = user.id
        if user.perfil == 'admin':
            return redirect(url_for('dashboard_admin'))
        elif user.perfil == 'profissional':
            return redirect(url_for('dashboard_profissional'))
        else:
            return redirect(url_for('dashboard_cliente'))
    return render_template('login.html')

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
    cliente = u.cliente
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
    ags = Agendamento.query.order_by(Agendamento.data_hora.desc()).all()
    return render_template('dashboard_admin.html', user=u, agendamentos=ags)

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

    servicos = Servico.query.all()
    profissionais = Profissional.query.all()

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
            flash("Não é possível agendar para datas/horários passados.", "danger")
            return redirect(url_for('reservar'))

        servico = Servico.query.get(servico_id)
        if not servico:
            flash("Serviço inválido.", "danger")
            return redirect(url_for('reservar'))

        if checar_conflito(profissional_id, dt, servico.duracao_min):
            flash("Horário indisponível para esse profissional. Escolha outro horário.", "warning")
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

        prof_user = Profissional.query.get(profissional_id).user
        notif_prof = Notificacao(user_id=prof_user.id, mensagem=f"Novo pedido de agendamento em {dt.strftime('%Y-%m-%d %H:%M')} para o serviço {servico.nome}.")
        notif_cliente = Notificacao(user_id=u.id, mensagem=f"Seu pedido de agendamento em {dt.strftime('%Y-%m-%d %H:%M')} foi criado e está pendente.")
        db.session.add_all([notif_prof, notif_cliente])
        db.session.commit()

        flash("Reserva criada com sucesso e enviada para confirmação.", "success")
        return redirect(url_for('minhas_reservas'))

    return render_template('reservar.html', user=u, servicos=servicos, profissionais=profissionais)

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
    notifs = Notificacao.query.filter_by(user_id=u.id).order_by(Notificacao.criado_em.desc()).all()
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
# Ações de confirma/cancel (admin ou profissional)
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
    notif = Notificacao(user_id=ag.cliente.user.id, mensagem=f"Seu agendamento em {ag.data_hora.strftime('%Y-%m-%d %H:%M')} foi confirmado.")
    db.session.add(notif)
    db.session.commit()
    flash("Agendamento confirmado.", "success")
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
    notif = Notificacao(user_id=ag.cliente.user.id, mensagem=f"Seu agendamento em {ag.data_hora.strftime('%Y-%m-%d %H:%M')} foi cancelado.")
    db.session.add(notif)
    db.session.commit()
    flash("Agendamento cancelado.", "info")
    return redirect(request.referrer or url_for('index'))

# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
