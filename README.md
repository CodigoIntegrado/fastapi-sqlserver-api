# 🚀 API REST com FastAPI + SQL Server

Projeto desenvolvido para o canal **Código Integrado**.

Neste tutorial construímos uma API REST do zero utilizando **Python, FastAPI, SQL Server, Pydantic e pyodbc**.

## 📚 Tecnologias utilizadas

- Python
- FastAPI
- SQL Server
- pyodbc
- Pydantic
- Uvicorn
- Swagger / OpenAPI
- Postman

## 📁 Estrutura do projeto

```text
fastapi-sqlserver-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routes/
│       ├── __init__.py
│       └── produtos.py
│
├── sql/
│   └── 01_criar_banco.sql
│
├── postman/
│   └── CodigoIntegrado_API.postman_collection.json
│
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md