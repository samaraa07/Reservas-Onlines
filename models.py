from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# A tabela tb_usuarios é a base para o modelo User
class User(db.Model):
    __tablename__ = 'tb_usuarios' 
    id = db.Column('usu_id', db.Integer, primary_key=True) 
    nome = db.Column('usu_name', db.String(200), nullable=False)
    email = db.Column('usu_email', db.String(200), unique=True, nullable=False)
    senha_hash = db.Column('usu_senha', db.String(200), nullable=False)
    
    perfil = db.Column('usu_tipo', db.Enum('cliente', 'profissional', 'admin', name='perfil_enum'), nullable=False, default='cliente')

    
    cliente = db.relationship('Cliente', uselist=False, back_populates='user', cascade='all,delete-orphan', foreign_keys='Cliente.user_id')
    profissional = db.relationship('Profissional', uselist=False, back_populates='user', cascade='all,delete-orphan', foreign_keys='Profissional.user_id')
    
    notificacoes = db.relationship('Notificacao', backref='usuario', lazy='dynamic', primaryjoin="User.id == Notificacao.user_id")

# CLASSE CLIENTE
class Cliente(db.Model):
    __tablename__ = 'tb_clientes'
    id = db.Column('cli_id', db.Integer, primary_key=True)
    user_id = db.Column('cli_usu_id', db.Integer, db.ForeignKey('tb_usuarios.usu_id'), unique=True)
    contato = db.Column('cli_contato', db.String(200))
    
    user = db.relationship('User', back_populates='cliente')
    agendamentos = db.relationship('Agendamento', back_populates='cliente', cascade='all,delete-orphan')

# CLASSE PROFISSIONAL
class Profissional(db.Model):
    __tablename__ = 'tb_profissionais'
    id = db.Column('pro_id', db.Integer, primary_key=True)

    user_id = db.Column('pro_usu_id', db.Integer, db.ForeignKey('tb_usuarios.usu_id'), unique=True)
    contato = db.Column('pro_contato', db.String(200)) 
    
    especialidades = db.Column('pro_especialidades', db.String(500)) 
    
    user = db.relationship('User', back_populates='profissional')
    servicos = db.relationship('Servico', back_populates='profissional', cascade='all,delete-orphan')
    agendamentos = db.relationship('Agendamento', back_populates='profissional', cascade='all,delete-orphan')

# CLASSE SERVICO
class Servico(db.Model):
    __tablename__ = 'tb_servicos'
    id = db.Column('ser_id', db.Integer, primary_key=True)
    nome = db.Column('ser_categoria', db.String(200), nullable=False)
    
    duracao_min = db.Column('ser_duracao', db.Integer, nullable=False, default=30)
    preco = db.Column('ser_preco', db.Float, nullable=True)
    profissional_id = db.Column('ser_pro_id', db.Integer, db.ForeignKey('tb_profissionais.pro_id'), nullable=True)
    
    profissional = db.relationship('Profissional', back_populates='servicos')

# CLASSE AGENDAMENTO
class Agendamento(db.Model):
    __tablename__ = 'tb_agendamentos'
    id = db.Column('age_id', db.Integer, primary_key=True)
    cliente_id = db.Column('age_cli_id', db.Integer, db.ForeignKey('tb_clientes.cli_id'))
    profissional_id = db.Column('age_pro_id', db.Integer, db.ForeignKey('tb_profissionais.pro_id'))
    servico_id = db.Column('age_ser_id', db.Integer, db.ForeignKey('tb_servicos.ser_id'))
    data_hora = db.Column('age_data_hora', db.DateTime, nullable=False)
    status = db.Column('age_status', db.Enum('pendente', 'confirmado', 'cancelado', name='status_enum'), default='pendente', nullable=False)
    criado_em = db.Column('age_criacao', db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', back_populates='agendamentos')
    profissional = db.relationship('Profissional', back_populates='agendamentos')
    servico = db.relationship('Servico')

# CLASSE NOTIFICACAO (Ajustes para a notificação funcionar)
class Notificacao(db.Model):
    __tablename__ = 'tb_notificacoes'
    id = db.Column('not_id', db.Integer, primary_key=True)
    user_id = db.Column('not_usu_id', db.Integer, db.ForeignKey('tb_usuarios.usu_id'), nullable=False) 
    mensagem = db.Column('not_mensagem', db.String(500), nullable=False) 
    
    lida = db.Column('not_lida', db.Boolean, default=False)
    criado_em = db.Column('not_criado_em', db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='notificacoes')