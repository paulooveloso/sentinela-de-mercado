from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class ProdutoPreco(Base):
    __tablename__ = "historico_precos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float, nullable=False)
    loja = Column(String)
    url = Column(String)
    data_coleta = Column(DateTime, default=datetime.utcnow)

    # Ajuda a ver o objeto formatado no terminal durante testes
    def __repr__(self):
        return f"<Produto(nome={self.nome}, preco={self.preco}, loja={self.loja})>"