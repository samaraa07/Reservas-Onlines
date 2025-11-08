from app import create_app
from models import db

app = create_app()
app.app_context().push()

# Apagar todas as tabelas existentes
# db.drop_all()

# Criar novamente as tabelas
db.create_all()

db.session.commit()
print("Banco reinicializado e pronto para uso (sem dados pré-carregados).")

