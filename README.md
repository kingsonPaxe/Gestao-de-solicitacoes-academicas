# Módulo de Gestão de Solicitações Acadêmicas

Sistema web em Flask para gestão de solicitações acadêmicas (alunos e administradores).

## Stack
- Python 3.13, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Jinja2, Werkzeug
- SQLite (dev) / MySQL (prod)
- HTML5 + CSS3 puro + JavaScript puro (sem frameworks front)

## Executando com uv

```bash
uv sync
cp .env.example .env
uv run python run.py
```

Acesse http://localhost:5000

### Credenciais de demonstração
- **Admin:** admin@imetro.ao / 123456
- **Alunos:** aluno1@imetro.ao ... aluno10@imetro.ao / 123456

Dados de demonstração são criados automaticamente no primeiro boot (10 alunos, todos os tipos de solicitação, 1 admin).

## Migrando de SQLite para MySQL

1. Crie o banco no MySQL:
   ```sql
   CREATE DATABASE solicitacoes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Edite `.env`:
   ```
   DATABASE_URL=mysql+pymysql://usuario:senha@host:3306/solicitacoes
   ```
3. Rode as migrações:
   ```bash
   uv run flask --app run.py db upgrade
   ```
   Ou, se preferir recriar do zero, apague `instance/app.db` e rode `uv run python run.py` novamente para o SQLAlchemy criar as tabelas + seed.

## Estrutura

```
app/
  ├── __init__.py         # factory
  ├── config.py
  ├── models/             # SQLAlchemy models
  ├── repositories/       # acesso a dados
  ├── services/           # regras de negócio
  ├── routes/             # blueprints (controllers)
  ├── forms/              # WTForms
  ├── utils/              # decorators, seed
  ├── static/             # css, js, uploads
  └── templates/          # Jinja2
```

Arquitetura em camadas: **routes → services → repositories → models**.
# Gestao-de-solicitacoes-academicas
