import os
from flask import Flask
from werkzeug.security import generate_password_hash
from sqlalchemy import text  # necessário para usar comandos SQL diretos
from models import db, User, Administrador


# ------------------------------------
# Caminho do banco de dados
# ------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'banco_de_dados', 'salon_reservas.db')

print(f"Usando banco em: {db_path}")

# Garante que a pasta existe
os.makedirs(os.path.dirname(db_path), exist_ok=True)


# ------------------------------------
# Configuração do app Flask
# ------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# ------------------------------------
# Criação e população do banco (sem apagar)
# ------------------------------------
with app.app_context():
    # NÃO apagar o arquivo existente: isso destruía todos os dados
    if not os.path.exists(db_path):
        print("Banco não existe ainda. Será criado.")
    else:
        print("Banco já existe. Tabelas serão verificadas/criadas se necessário.")

    # Cria tabelas se não existirem
    db.create_all()

    # Criar administradores padrão somente se não existirem
    print("Verificando/criando administradores padrão...")

    admins_info = [
        ("Ana Francisca de Araújo Pereira", "anafrancisca@gmail.com", "1234"),
        ("Estela Áurea da Nóbrega Calixto", "estelaaurea@gmail.com", "2345"),
        ("Maria de Jesus Santos Neta", "mariajesus@gmail.com", "3456"),
        ("Samara Fernanda Medeiros da Silva", "samarafernanda@gmail.com", "4567"),
        ("Sthefany Dantas Brito", "sthefdantas@gmail.com", "5678"),
    ]

    criados = 0
    for nome, email, senha in admins_info:
        # se já existe um usuário com esse email, pula
        if User.query.filter_by(email=email).first():
            continue

        user = User(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
            perfil='admin',
            is_ativo=True  # admins padrão já ativos
        )
        db.session.add(user)
        db.session.commit()  # precisa para gerar o user.id

        admin = Administrador(
            user_id=user.id,
            nivel_acesso='geral',
            status='aprovado'  # admins padrão já aprovados
        )
        db.session.add(admin)
        criados += 1

    db.session.commit()
    print(f"Administradores padrão verificados. Novos criados: {criados}\n")

    # ------------------------------------
    # Mostrar tabelas e conteúdo
    # ------------------------------------
    print("Tabelas existentes:")
    tabelas = db.session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table';")
    ).fetchall()
    for t in tabelas:
        print(" -", t[0])

    # Listar usuários
    print("\nUsuários cadastrados:")
    usuarios = User.query.all()
    if usuarios:
        for u in usuarios:
            print(
                f"ID: {u.id} | Nome: {u.nome} | Email: {u.email} | "
                f"Perfil: {u.perfil} | Ativo: {u.is_ativo}"
            )
    else:
        print("Nenhum usuário encontrado.")

    # Listar administradores
    print("\nAdministradores cadastrados:")
    admins = Administrador.query.all()
    if admins:
        for a in admins:
            print(
                f"Admin ID: {a.id} | Usuário ID: {a.user_id} | "
                f"Nível: {a.nivel_acesso} | Status: {a.status}"
            )
    else:
        print("Nenhum administrador encontrado.")

    print("\nBanco verificado. Tabelas criadas (se necessário) e admins padrão garantidos.")
