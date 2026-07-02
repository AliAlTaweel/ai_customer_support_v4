# Luxe v4.0 - AI Customer Support Backend

FastAPI-based backend for the Luxe v4.0 multi-tenant AI customer support platform. Provides REST API endpoints for tenant management, authentication, API keys, and integrations.

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

Luxe v4.0 Backend is a FastAPI application that powers the multi-tenant SaaS platform for AI-driven customer support. It manages:

- **Multi-tenant architecture** with isolated data per organization
- **Tenant management** (CRUD operations)
- **API key generation** for programmatic access
- **Store integrations** (Shopify, WooCommerce, Stripe)
- **Authentication** with optional Clerk integration
- **Structured logging** for monitoring and debugging

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | FastAPI | 0.109.0 |
| Database ORM | SQLAlchemy | 2.0.27 |
| Database | SQLite | 3.x |
| Authentication | Clerk SDK | Optional |
| Validation | Pydantic | 2.0+ |
| Server | Uvicorn | Latest |
| Python | 3.12 | Recommended |

## 📦 Prerequisites

- **Python 3.12** or higher
- **pip** (Python package manager)
- **Git** (for version control)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone git@github.com:AliAlTaweel/ai_customer_support_v4.git
cd ai_customer_support_v4/backend
```

### 2. Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Database (SQLite for development)
DATABASE_URL=sqlite:///./ai_customer_support.db

# Clerk Authentication (test keys)
CLERK_SECRET_KEY=sk_test_your_clerk_secret_key
CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_publishable_key

# Stripe (optional)
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8002

# Frontend
FRONTEND_URL=http://localhost:3002
```

### Database Setup

The database is automatically initialized on first run. SQLite creates `ai_customer_support.db` in the backend directory.

## 🏃 Running the Server

### Development Mode (with auto-reload)

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

### Production Mode

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --workers 4
```

### Access the Server

- **API**: http://localhost:8002
- **Auto-docs**: http://localhost:8002/docs (Swagger UI)
- **ReDoc**: http://localhost:8002/redoc

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Pydantic configuration settings
├── db.py                  # SQLAlchemy database setup
├── logger.py              # Structured logging configuration
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic request/response schemas
├── auth.py                # Authentication utilities
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── routers/              # API route handlers
    ├── tenants.py        # Tenant CRUD endpoints
    ├── auth.py           # Authentication endpoints
    ├── api_keys.py       # API key management
    └── integrations.py   # Store integration endpoints
```

## 🔌 API Endpoints

### Tenant Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/tenants` | Create new tenant |
| `GET` | `/api/v1/tenants` | List all tenants |
| `GET` | `/api/v1/tenants/{id}` | Get tenant details |
| `PUT` | `/api/v1/tenants/{id}` | Update tenant |
| `DELETE` | `/api/v1/tenants/{id}` | Delete tenant |
| `GET` | `/api/v1/tenants/{id}/metrics` | Get tenant metrics |

### API Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/api-keys/{tenant_id}` | Generate new API key |
| `GET` | `/api/v1/api-keys/{tenant_id}` | Get API key |

### Integrations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/integrations/{tenant_id}` | Create integration |
| `GET` | `/api/v1/integrations/{tenant_id}` | List integrations |
| `GET` | `/api/v1/integrations/{tenant_id}/{id}` | Get integration |
| `DELETE` | `/api/v1/integrations/{tenant_id}/{id}` | Delete integration |
| `POST` | `/api/v1/integrations/{tenant_id}/{id}/sync` | Sync integration data |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/signup` | Sign up new user |
| `POST` | `/api/v1/auth/login` | User login |
| `GET` | `/api/v1/auth/me` | Get current user |

## 📝 Example Requests

### Create Tenant

```bash
curl -X POST http://localhost:8002/api/v1/tenants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Shop",
    "supportEmail": "support@shop.com",
    "tone": "professional",
    "systemPrompt": "You are a helpful customer support assistant"
  }'
```

### List Tenants

```bash
curl http://localhost:8002/api/v1/tenants
```

### Generate API Key

```bash
curl -X POST http://localhost:8002/api/v1/api-keys/tenant-id-here
```

### Delete Tenant

```bash
curl -X DELETE http://localhost:8002/api/v1/tenants/tenant-id-here
```

## 🔐 Environment Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | String | `sqlite:///./ai_customer_support.db` | Database connection URL |
| `CLERK_SECRET_KEY` | String | `sk_test_placeholder` | Clerk API secret key |
| `CLERK_PUBLISHABLE_KEY` | String | `pk_test_placeholder` | Clerk publishable key |
| `STRIPE_SECRET_KEY` | String | Empty | Stripe API secret key |
| `STRIPE_PUBLISHABLE_KEY` | String | Empty | Stripe publishable key |
| `API_HOST` | String | `0.0.0.0` | Server host address |
| `API_PORT` | Integer | `8002` | Server port |
| `FRONTEND_URL` | String | `http://localhost:3002` | Frontend URL for CORS |
| `DEBUG` | Boolean | `false` | Debug mode |
| `APP_NAME` | String | `Luxe v4.0 - AI Helpdesk` | Application name |

## 🪵 Logging

Logs are written to:

- **Console**: Real-time application logs
- **File**: `logs/app.log` - Persistent log file

Log levels:
- `INFO` - General information
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `DEBUG` - Debug information

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8002
lsof -i :8002

# Kill the process
kill -9 <PID>
```

### Database Lock Error

SQLite doesn't handle concurrent writes well. For production, use PostgreSQL:

```bash
DATABASE_URL=postgresql://user:password@localhost/luxe
```

### Import Errors

Ensure you're in the virtual environment:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### CORS Errors

Check `FRONTEND_URL` in `.env` matches your frontend URL:

```bash
# For local development
FRONTEND_URL=http://localhost:3002
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Clerk Documentation](https://clerk.com/docs)

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 📄 License

This project is proprietary software. All rights reserved.

## 📧 Support

For issues and questions, please contact the development team.

---

**Built with ❤️ using FastAPI**
