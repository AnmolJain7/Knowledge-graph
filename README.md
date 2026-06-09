# Knowledge Graph Demo

This project is a `FastAPI` backend that combines standard user CRUD APIs with a conversational workflow powered by `LangGraph`. It stores user records and chat workflow state in `PostgreSQL`, and it can optionally use `Groq` to improve intent detection for chat requests.

## Features

- Create, read, update, list, and delete users through REST APIs
- Chat-based user operations through a single `/chat/` endpoint
- Multi-turn workflow state persisted by `thread_id`
- Guided user creation flow using `LangGraph`
- Optional LLM-based intent classification with Groq
- Fallback keyword-based intent detection when Groq is not configured

## Tech Stack

- `FastAPI`
- `SQLAlchemy`
- `PostgreSQL`
- `Pydantic`
- `LangGraph`
- `Groq API` (optional)

## Project Structure

```text
knowledge_graph_demo/
├── backend/
│   ├── app/
│   │   ├── api/v1/              # REST and chat routes
│   │   ├── core/                # Config and database setup
│   │   ├── langgraph/           # Workflow state, graph, and nodes
│   │   ├── models/              # SQLAlchemy models
│   │   ├── repositories/        # Database access layer
│   │   ├── schemas/             # Request/response schemas
│   │   └── services/            # Business logic
│   ├── .env.example
│   ├── requirements.txt
│   └── test_graph.py
└── README.md
```

## How It Works

### 1. User APIs

The `/users` routes provide direct CRUD operations:

- `POST /users` creates a user
- `GET /users` lists all users
- `GET /users/{user_id}` fetches one user
- `PUT /users/{user_id}` updates a user
- `DELETE /users/{user_id}` deletes a user

### 2. Chat Workflow

The `/chat/` endpoint accepts natural language and handles these intents:

- `create_user`
- `get_user`
- `list_users`
- `update_user`
- `delete_user`

When a request comes in:

1. The app loads workflow state using `thread_id`
2. It updates any pending step such as name, age, or phone number
3. It detects the intent using Groq if configured, otherwise local rules
4. It executes the matching workflow
5. It saves the updated workflow state back to PostgreSQL

For `create_user`, the app uses a `LangGraph` flow to ask for missing fields one by one:

- Name
- Age
- Gender
- Address
- Phone number

## Prerequisites

- `Python 3.12+`
- `PostgreSQL`
- Optional: `Groq API key`

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

Create `backend/.env` from `backend/.env.example`.

Example:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=knowledge_graph_demo

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

### 4. Create the database

Create a PostgreSQL database matching `DB_NAME`.

The tables are created automatically on app startup from:

- `users`
- `workflow_states`

### 5. Run the application

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## API Examples

### Create a user

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aman",
    "age": 25,
    "gender": "male",
    "address": "Delhi",
    "phone_number": "9876543210"
  }'
```

### List users

```bash
curl "http://127.0.0.1:8000/users"
```

### Chat: start create user workflow

```bash
curl -X POST "http://127.0.0.1:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "create a new user"
  }'
```

### Chat: continue same thread

Use the returned `thread_id` in follow-up requests:

```bash
curl -X POST "http://127.0.0.1:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "returned-thread-id",
    "message": "Aman"
  }'
```

## Sample Chat Prompts

- `create a new user`
- `show all users`
- `get user 1`
- `delete user 2`
- `update user 3 age to 30`

## Notes

- If `GROQ_API_KEY` is not set, the app still works using keyword matching.
- Workflow state is stored as JSON in the `workflow_states` table.
- Phone number uniqueness is enforced before user creation.
- The app currently creates tables directly on startup and does not yet use migration flow in runtime.

## Useful Files

- [backend/app/main.py](/Users/amanjain/Documents/knowledge_graph_demo/backend/app/main.py:1)
- [backend/app/api/v1/chat_routes.py](/Users/amanjain/Documents/knowledge_graph_demo/backend/app/api/v1/chat_routes.py:1)
- [backend/app/api/v1/user_routes.py](/Users/amanjain/Documents/knowledge_graph_demo/backend/app/api/v1/user_routes.py:1)
- [backend/app/services/intent_service.py](/Users/amanjain/Documents/knowledge_graph_demo/backend/app/services/intent_service.py:1)
- [backend/app/langgraph/graphs/create_user_graph.py](/Users/amanjain/Documents/knowledge_graph_demo/backend/app/langgraph/graphs/create_user_graph.py:1)

## Future Improvements

- Add Alembic migrations for schema management
- Add tests for API routes and chat workflows
- Improve intent extraction for more natural update commands
- Add Docker support for local development

