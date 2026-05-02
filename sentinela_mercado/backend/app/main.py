from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database

# Cria as tabelas no arquivo .db
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Sentinela de Mercado API")

@app.get("/")
def read_root():
    return {"mensagem": "API Sentinela de Mercado operando na porta 8001!"}

# Rota INTELIGENTE para receber preços
@app.post("/precos/")
def criar_registro_preco(
    nome: str, 
    preco: float, 
    loja: str, 
    url: str, 
    db: Session = Depends(database.get_db)
):
    # 1. Busca o último preço salvo deste mesmo produto
    ultimo_registro = db.query(models.ProdutoPreco)\
                        .filter(models.ProdutoPreco.nome == nome)\
                        .order_by(models.ProdutoPreco.data_coleta.desc())\
                        .first()
    
    alerta_queda = False
    mensagem = "Preço cadastrado com sucesso."

    # 2. Verifica se o preço caiu
    if ultimo_registro:
        if preco < ultimo_registro.preco:
            alerta_queda = True
            mensagem = f"ALERTA: O preço caiu de R$ {ultimo_registro.preco} para R$ {preco}!"
        elif preco > ultimo_registro.preco:
            mensagem = f"O preço subiu (Era R$ {ultimo_registro.preco})."
        else:
            mensagem = "O preço se manteve igual."

    # 3. Salva o novo preço no banco
    novo_registro = models.ProdutoPreco(
        nome=nome, 
        preco=preco, 
        loja=loja, 
        url=url
    )
    db.add(novo_registro)
    db.commit()
    db.refresh(novo_registro)

    # 4. Retorna a resposta com o alerta para o Bot do Telegram ler
    return {
        "alerta_queda": alerta_queda,
        "mensagem_alerta": mensagem,
        "dados_salvos": novo_registro
    }

# Rota para o Dashboard
@app.get("/historico/")
def listar_precos(db: Session = Depends(database.get_db)):
    return db.query(models.ProdutoPreco).all()