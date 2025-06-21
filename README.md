# 🍽️ Daily Diet API - Desafio 02 | Rocketseat

Este projeto é uma solução para o **Desafio 02** do módulo **Desenvolvimento Avançado com Flask** da trilha da Rocketseat.

A aplicação é uma API para controle de refeições diárias, com funcionalidades para registrar, listar, editar e excluir refeições de um usuário, verificando se estão dentro ou fora da dieta.

---

## 🚀 Tecnologias Utilizadas

- Python 3.11+
- Flask
- Flask SQLAlchemy
- Flask Migrate
- SQLite (ou PostgreSQL, opcional)
- pytest (para testes)
- Flask Marshmallow (opcional, para serialização)

---

## ⚙️ Funcionalidades

- ✅ Criar uma nova refeição com:
  - Nome
  - Descrição
  - Data e hora
  - Indicador de se está dentro ou fora da dieta
- ✏️ Editar qualquer refeição
- ❌ Excluir refeições
- 📋 Listar todas as refeições de um usuário
- 🔍 Visualizar uma única refeição
- 💾 Persistência dos dados em banco de dados relacional

---

## 🧰 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/daily-diet-api.git
cd daily-diet-api
```

### 2. Crie um ambiente virtual e ative

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Rode a aplicação

```bash
flask run
```

---

## 📮 Rotas da API (exemplos)

| Método | Rota                | Descrição                          |
|--------|---------------------|------------------------------------|
| POST   | `/refeicoes`        | Criar nova refeição                |
| GET    | `/refeicoes`        | Listar todas as refeições          |
| GET    | `/refeicoes/<id>`   | Visualizar uma refeição específica |
| PUT    | `/refeicoes/<id>`   | Editar uma refeição                |
| DELETE | `/refeicoes/<id>`   | Deletar uma refeição               |

> A estrutura final pode variar conforme o design do projeto.

---

## 🧪 Testes

Execute os testes com:

```bash
pytest
```

---

## 📁 Estrutura Sugerida

```text
.
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── schemas/
│   └── __init__.py
├── migrations/
├── tests/
├── config.py
├── run.py
└── requirements.txt
```

---

## 💭 Aprendizados

Durante o desafio, foram praticados:

- Organização de projeto Flask em estrutura modular
- Criação de API RESTful
- Manipulação de banco de dados com SQLAlchemy
- Criação e execução de migrações com Flask-Migrate
- Validação e serialização de dados
- Desenvolvimento com testes automatizados

---

## 📌 Entrega

URL do projeto: [https://github.com/seu-usuario/daily-diet-api](https://github.com/seu-usuario/daily-diet-api)

---

## 🧑‍💻 Autor

Feito por Wellington Pedro (https://github.com/wprsousa) para o desafio da Rocketseat.
