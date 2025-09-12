from app import create_app
from models import db, User, Cliente, Profissional, Servico
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

db.create_all()

# Criar admin se não existir
if not User.query.filter_by(email='admin@salon.com').first():
    admin = User(
        nome='Administrador',
        email='admin@salon.com',
        senha_hash=generate_password_hash('admin123'),
        perfil='admin'
    )
    db.session.add(admin)

# Criar alguns profissionais e serviços de exemplo
if not User.query.filter_by(email='ana@salon.com').first():
    user_p = User(nome='Ana Profissional', email='ana@salon.com', senha_hash=generate_password_hash('senha123'), perfil='profissional')
    prof = Profissional(contato='(11) 99999-0001', especialidades='Manicure,Pedicure', user=user_p)
    s1 = Servico(nome='Manicure', duracao_min=45, preco=30.0, profissional=prof)
    s2 = Servico(nome='Pedicure', duracao_min=45, preco=35.0, profissional=prof)
    db.session.add_all([user_p, prof, s1, s2])

if not User.query.filter_by(email='carlos@cliente.com').first():
    user_c = User(nome='Carlos Cliente', email='carlos@cliente.com', senha_hash=generate_password_hash('senha123'), perfil='cliente')
    cliente = Cliente(contato='(11) 98888-7777', user=user_c)
    db.session.add_all([user_c, cliente])

db.session.commit()
print("Banco inicializado com dados de exemplo.")
