from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Nome do arquivo do banco de dados que será criado automaticamente
SQLALCHEMY_DATABASE_URL = "sqlite:///./precos_mercado.db"

# Criando o motor de conexão (Corrigido para create_engine)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criando a sessão que o backend usará para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que usaremos para criar nossas tabelas (Models)
Base = declarative_base()

# Função auxiliar para abrir/fechar a conexão automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()