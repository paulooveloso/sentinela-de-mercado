
# 📑 Relatório Técnico: Backend - Sentinela de Mercado (v1.0)

## 🎯 Objetivo do Módulo
Desenvolver a infraestrutura central do projeto, responsável por persistir o histórico de preços e processar a inteligência de comparação para detecção de promoções.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.9+
- **Framework Web:** FastAPI (Alta performance e documentação automática).
- **Banco de Dados:** SQLite (Armazenamento local em arquivo `.db`).
- **ORM:** SQLAlchemy (Mapeamento de banco de dados para classes Python).
- **Servidor:** Uvicorn.

---

## 🏗️ Estrutura de Pastas Implementada
```text
sentinela_mercado/
└── backend/
    ├── app/
    │   ├── main.py       # Cérebro da API e Rotas
    │   ├── models.py     # Definição das Tabelas do Banco
    │   ├── database.py   # Configuração e Conexão SQLite
    │   └── __init__.py
    ├── venv/             # Ambiente Virtual Isolado
    └── requirements.txt  # Dependências do Sistema
```

---

## ⚙️ Funcionalidades Concluídas

### 1. Persistência de Dados Automatizada
O sistema cria automaticamente um banco de dados chamado `precos_mercado.db`. A tabela principal (`historico_precos`) armazena:
- Nome do Produto
- Valor (Float)
- Nome da Loja
- URL de Origem
- Timestamp (Data e hora exata da coleta)

### 2. Lógica de "Sentinela" (Diferencial do Projeto)
A rota de cadastro (`POST /precos/`) não apenas salva o dado, mas executa uma análise em tempo real:
- Busca o registro anterior do mesmo produto.
- Compara o preço novo com o antigo.
- **Gera um Alerta:** Retorna um campo booleano `alerta_queda: true` e uma mensagem formatada caso o preço atual seja menor que o anterior.

### 3. Documentação Viva (Swagger)
A API já conta com uma interface gráfica para testes rodando em `http://127.0.0.1:8001/docs`, permitindo que qualquer integrante teste as rotas sem precisar de ferramentas externas.

---

## 🤝 Guia de Integração para a Equipe

Para que o projeto flua, os outros integrantes devem interagir com o Backend da seguinte forma:

1.  **Integrante 1 (Scraper):** Deve enviar um `POST` para `/precos/` contendo o JSON com os dados coletados.
2.  **Integrante 3 (Dashboard):** Deve consumir a rota `GET /historico/` para obter a lista completa de preços e gerar os gráficos de variação.
3.  **Integrante 4 (Bot Telegram):** Deve monitorar o retorno da rota de cadastro. Se `alerta_queda` for `true`, o Bot dispara a notificação para os usuários.



---

## 🚀 Próximos Passos
- Implementar filtros de busca por nome ou loja na rota de histórico.
- Criar uma rota para deletar registros antigos (limpeza de banco).
- Preparar o deploy (subir a API para que os colegas acessem pela internet, não apenas local).

