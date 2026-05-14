# 📑 Relatório Técnico: Backend - Sentinela de Mercado (v1.0)

## 🎯 Objetivo do Módulo
Desenvolver a infraestrutura central do projeto, responsável por persistir o histórico de preços e processar a inteligência de comparação para detecção de promoções.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.9+
- **Framework Web:** FastAPI (Alta performance e documentação automática)
- **Banco de Dados:** SQLite (Armazenamento local em arquivo `.db`)
- **ORM:** SQLAlchemy (Mapeamento de banco de dados para classes Python)
- **Servidor:** Uvicorn
- **Validação:** Pydantic v2

---

## 🏗️ Estrutura de Pastas Implementada
```text
sentinela_mercado/
└── backend/
    ├── app/
    │   ├── main.py       # Cérebro da API e Rotas
    │   ├── models.py     # Definição das Tabelas do Banco
    │   ├── database.py   # Configuração e Conexão SQLite
    │   ├── schemas.py    # Schemas de validação Pydantic
    │   ├── crud.py       # Operações de banco de dados
    │   └── __init__.py
    ├── venv/             # Ambiente Virtual Isolado
    ├── precos_mercado.db # Banco de dados local (não versionado)
    └── requirements.txt  # Dependências do Sistema
```

---

## ▶️ Como Rodar Localmente

```bash
cd sentinela_mercado/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

Acesse a documentação interativa em: **http://127.0.0.1:8001/docs**

---

## ⚙️ Funcionalidades Concluídas

### 1. CRUD Completo
A API implementa todas as operações básicas:

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/precos/` | Cadastra novo preço com análise inteligente |
| `GET` | `/historico/` | Lista todos os preços registrados |
| `GET` | `/precos/{id}` | Busca um registro específico por ID |
| `PUT` | `/precos/{id}` | Atualiza nome ou preço de um registro |
| `DELETE` | `/precos/{id}` | Remove um registro do banco |

### 2. Persistência de Dados Automatizada
O sistema cria automaticamente o banco `precos_mercado.db`. A tabela principal armazena:
- Nome do Produto
- Valor (Float)
- Nome da Loja
- URL de Origem
- Timestamp (Data e hora exata da coleta)

### 3. Lógica de "Sentinela" (Diferencial do Projeto)
A rota `POST /precos/` não apenas salva o dado, mas executa uma análise em tempo real:
- Busca o registro anterior do mesmo produto
- Compara o preço novo com o antigo
- Retorna `alerta_queda: true` e mensagem formatada se o preço caiu
- Informa também se o preço subiu ou se manteve igual

### 4. Validação de Dados com Pydantic
Os dados recebidos pela API são validados automaticamente via schema Pydantic antes de chegar ao banco, evitando dados malformados ou incompletos.

### 5. Documentação Viva (Swagger)
Interface gráfica para testes disponível em `http://127.0.0.1:8001/docs` — permite testar todas as rotas sem ferramentas externas.

---

## 🤝 Guia de Integração para a Equipe

1. **Integrante 1 (Scraper):** Enviar `POST /precos/` com JSON contendo `nome`, `preco`, `loja` e `url`
2. **Integrante 3 (Dashboard):** Consumir `GET /historico/` para obter lista completa de preços e gerar gráficos
3. **Integrante 4 (Bot Telegram):** Monitorar o retorno do `POST /precos/` — se `alerta_queda: true`, disparar notificação

### Exemplo de Payload (POST /precos/)
```json
{
  "nome": "iPhone 15 Pro",
  "preco": 7499.99,
  "loja": "Americanas",
  "url": "https://americanas.com.br/produto/123"
}
```

### Exemplo de Resposta
```json
{
  "alerta_queda": true,
  "mensagem_alerta": "ALERTA: O preço caiu de R$ 7999.99 para R$ 7499.99!",
  "dados_salvos": { ... }
}
```

