import os
from flask import Flask
from werkzeug.security import generate_password_hash
from sqlalchemy import text  #necessário para usar comandos SQL diretos
from models import db, User, Administrador

# ------------------------------------
# Caminho do banco de dados
# ------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'banco_de_dados', 'salon_reservas.db')

print(f"Verificando banco em: {db_path}")

# ------------------------------------
# Configuração do app Flask
# ------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ------------------------------------
# Criação e população do banco
# ------------------------------------
with app.app_context():
    print("Limpando tabelas existentes...")
    if os.path.exists(db_path):
        os.remove(db_path)

    db.create_all()

    # Criar administradores padrão
    print("Criando administradores padrão...")

    admins_info = [
        ("Ana Francisca de Araújo Pereira", "anafrancisca@gmail.com", "1234"),
        ("Estela Áurea da Nóbrega Calixto", "estelaaurea@gmail.com", "2345"),
        ("Maria de Jesus Santos Neta", "mariajesus@gmail.com", "3456"),
        ("Samara Fernanda Medeiros da Silva", "samarafernanda@gmail.com", "4567"),
        ("Sthefany Dantas Brito", "sthefdantas@gmail.com", "5678"),
    ]

    for nome, email, senha in admins_info:
        user = User(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
            perfil='admin'
        )
        db.session.add(user)
        db.session.commit()  #precisa para gerar o usu_id

        admin = Administrador(
            user_id=user.id,  # usa o atributo mapeado (usu_id)
            nivel_acesso='geral'
        )
        db.session.add(admin)

    db.session.commit()
    print("Administradores padrão criados com sucesso!\n")

    # ------------------------------------
    # Mostrar tabelas e conteúdo
    # ------------------------------------
    print("Tabelas existentes:")
    tabelas = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    for t in tabelas:
        print(" -", t[0])

    # Listar usuários
    print("\nUsuários cadastrados:")
    usuarios = User.query.all()
    if usuarios:
        for u in usuarios:
            print(f"ID: {u.id} | Nome: {u.nome} | Email: {u.email} | Perfil: {u.perfil}")
    else:
        print("Nenhum usuário encontrado.")

    # Listar administradores
    print("\nAdministradores cadastrados:")
    admins = Administrador.query.all()
    if admins:
        for a in admins:
            print(f"Admin ID: {a.id} | Usuário ID: {a.user_id} | Nível: {a.nivel_acesso}")
    else:
        print("Nenhum administrador encontrado.")

    print("\nBanco reinicializado e populado com administradores padrão.")
