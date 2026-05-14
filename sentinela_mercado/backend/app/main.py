from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from . import models, database


# Cria as tabelas no arquivo .db
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI(title="Sentinela de Mercado API")


# Schema Pydantic para receber dados via JSON
class ProdutoPrecoCreate(BaseModel):
    nome: str
    preco: float
    loja: str
    url: str


@app.get("/")
def read_root():
    return {"mensagem": "API Sentinela de Mercado operando na porta 8001!"}


# CREATE - Rota INTELIGENTE para receber preços
@app.post("/precos/")
def criar_registro_preco(dados: ProdutoPrecoCreate, db: Session = Depends(database.get_db)):
    nome = dados.nome
    preco = dados.preco
    loja = dados.loja
    url = dados.url

    # 1. Busca o último preço salvo deste mesmo produto
    ultimo_registro = db.query(models.ProdutoPreco)\
                        .filter(models.ProdutoPreco.nome == nome)\
                        .order_by(models.ProdutoPreco.data_coleta.desc())\
                        .first()

    alerta_queda = False
    mensagem = "Preço cadastrado com sucesso."

        # 2. Verifica se o preço caiu
    if ultimo_registro is not None:
        preco_anterior = float(ultimo_registro.preco) # type: ignore
        if preco < preco_anterior:
            alerta_queda = True
            mensagem = f"ALERTA: O preço caiu de R$ {preco_anterior} para R$ {preco}!"
        elif preco > preco_anterior:
            mensagem = f"O preço subiu (Era R$ {preco_anterior})."
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

    # 4. Retorna a resposta com o alerta
    return {
        "alerta_queda": alerta_queda,
        "mensagem_alerta": mensagem,
        "dados_salvos": novo_registro
    }


# READ - Rota para listar TODOS os preços
@app.get("/historico/")
def listar_precos(db: Session = Depends(database.get_db)):
    return db.query(models.ProdutoPreco).all()


# READ - Buscar apenas UM preço específico pelo ID
@app.get("/precos/{preco_id}")
def buscar_preco_por_id(preco_id: int, db: Session = Depends(database.get_db)):
    registro = db.query(models.ProdutoPreco).filter(models.ProdutoPreco.id == preco_id).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
    return registro


# UPDATE - Atualizar um registro existente
@app.put("/precos/{preco_id}")
def atualizar_preco(
    preco_id: int,
    novo_nome: Optional[str] = None,
    novo_preco: Optional[float] = None,
    db: Session = Depends(database.get_db)
):
    registro = db.query(models.ProdutoPreco).filter(models.ProdutoPreco.id == preco_id).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")

    if novo_nome:
        registro.nome = novo_nome
    if novo_preco:
        registro.preco = novo_preco

    db.commit()
    db.refresh(registro)

    return {"mensagem": "Registro atualizado com sucesso!", "dados_atualizados": registro}


# DELETE - Apagar um registro do banco
@app.delete("/precos/{preco_id}")
def deletar_preco(preco_id: int, db: Session = Depends(database.get_db)):
    registro = db.query(models.ProdutoPreco).filter(models.ProdutoPreco.id == preco_id).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")

    db.delete(registro)
    db.commit()

    return {"mensagem": f"O registro ID {preco_id} foi apagado do banco de dados."}

