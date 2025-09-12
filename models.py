from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    perfil = db.Column(db.Enum('cliente', 'profissional', 'admin', name='perfil_enum'), nullable=False, default='cliente')

    cliente = db.relationship('Cliente', uselist=False, back_populates='user', cascade='all,delete-orphan')
    profissional = db.relationship('Profissional', uselist=False, back_populates='user', cascade='all,delete-orphan')
    notificacoes = db.relationship('Notificacao', back_populates='user', cascade='all,delete-orphan')

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    contato = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user = db.relationship('User', back_populates='cliente')
    agendamentos = db.relationship('Agendamento', back_populates='cliente', cascade='all,delete-orphan')

class Profissional(db.Model):
    __tablename__ = 'profissionais'
    id = db.Column(db.Integer, primary_key=True)
    contato = db.Column(db.String(200))
    especialidades = db.Column(db.String(500))  # CSV de serviços / categorias
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user = db.relationship('User', back_populates='profissional')
    servicos = db.relationship('Servico', back_populates='profissional', cascade='all,delete-orphan')
    agendamentos = db.relationship('Agendamento', back_populates='profissional', cascade='all,delete-orphan')

class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    duracao_min = db.Column(db.Integer, nullable=False, default=30)  # duração em minutos
    preco = db.Column(db.Float, nullable=True)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=True)
    profissional = db.relationship('Profissional', back_populates='servicos')

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'))
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'))
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pendente', 'confirmado', 'cancelado', name='status_enum'), default='pendente', nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', back_populates='agendamentos')
    profissional = db.relationship('Profissional', back_populates='agendamentos')
    servico = db.relationship('Servico')

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mensagem = db.Column(db.String(1000))
    lida = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='notificacoes')
