# Luxe v4.0 - AI Customer Support Platform

A modern, multi-tenant SaaS platform for AI-driven customer support automation. Luxe enables ecommerce businesses to automate 80%+ of their support tickets using advanced AI while maintaining human oversight through a Copilot mode.

![Luxe v4.0](https://img.shields.io/badge/Luxe-v4.0-blue)
![Phase 1](https://img.shields.io/badge/Phase-1%20Complete-green)
![License](https://img.shields.io/badge/License-Proprietary-red)

## 📚 Quick Links

- **[Backend Documentation](./backend/README.md)** - FastAPI server setup and API reference
- **[Frontend Documentation](./frontend/README.md)** - Next.js dashboard setup
- **[Integration Guide](./support/LUXE_INTEGRATION_GUIDE.md)** - How to integrate Luxe into your store

## 🎯 Project Overview

Luxe v4.0 is a complete multi-tenant AI customer support platform built with modern technologies:

### What It Does

- 🤖 **AI-Powered Support** - Automatically respond to customer inquiries using AI
- 🏪 **Multi-Store Management** - Support multiple Shopify/WooCommerce stores from one dashboard
- 📊 **Analytics & Metrics** - Track automation rates, response times, and resolution rates
- 🔌 **Easy Integration** - Connect stores in minutes with API keys
- 👥 **Copilot Mode** - Review and approve AI responses before sending
- 🛠️ **Customizable AI** - Set brand tone and custom instructions per store

## 🏗️ Architecture

```
Luxe v4.0
├── Frontend (Next.js 14 + React)
│   ├── Dashboard UI (Responsive)
│   ├── Tenant Management
│   ├── Integration Setup
│   └── Case Management (Phase 2)
│
├── Backend (FastAPI + Python)
│   ├── Multi-tenant API
│   ├── SQLAlchemy ORM
│   ├── SQLite Database
│   └── Store Integrations
│
└── Infrastructure
    ├── Clerk Authentication
    ├── CORS Middleware
    ├── Structured Logging
    └── Error Handling
```

## 🚀 Quick Start

### Option 1: Development Setup (5 minutes)

#### Prerequisites
- Node.js 18+
- Python 3.12+
- Git

#### Start Backend

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

Backend will be available at: **http://localhost:8002**

#### Start Frontend (in a new terminal)

```bash
cd frontend
npm install
npm run dev -- -p 3002
```

Frontend will be available at: **http://localhost:3002**

#### Access the Dashboard

1. Open http://localhost:3002 in your browser
2. Click "Sign In" or "Sign Up"
3. Create/manage tenants in the Settings tab

## 📁 Project Structure

```
ai_customer_support_v4/
├── backend/                    # FastAPI application
│   ├── main.py                # App entry point
│   ├── config.py              # Configuration
│   ├── db.py                  # Database setup
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── routers/               # API endpoints
│   ├── requirements.txt       # Python dependencies
│   ├── .gitignore
│   └── README.md              # Backend documentation
│
├── frontend/                   # Next.js application
│   ├── app/                   # App directory
│   ├── components/            # React components
│   ├── lib/                   # Utilities
│   ├── package.json          # npm dependencies
│   ├── tailwind.config.js    # Tailwind config
│   ├── .gitignore
│   └── README.md             # Frontend documentation
│
├── support/                    # Documentation
│   └── LUXE_INTEGRATION_GUIDE.md
│
├── .gitignore                 # Root git ignore
└── README.md                  # This file
```

## ⚙️ Configuration

### Environment Variables

Both services require `.env` files. See respective READMEs for details:

**Backend** (`backend/.env`)
```
DATABASE_URL=sqlite:///./ai_customer_support.db
CLERK_SECRET_KEY=sk_test_your_key
API_PORT=8002
```

**Frontend** (`frontend/.env.local`)
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_key
NEXT_PUBLIC_API_URL=http://localhost:8002
```

## 🔌 API Endpoints

### Core Endpoints

```
POST   /api/v1/tenants              # Create tenant
GET    /api/v1/tenants              # List tenants
GET    /api/v1/tenants/{id}         # Get tenant
PUT    /api/v1/tenants/{id}         # Update tenant
DELETE /api/v1/tenants/{id}         # Delete tenant

POST   /api/v1/api-keys/{id}        # Generate API key
GET    /api/v1/api-keys/{id}        # Get API key

POST   /api/v1/integrations/{id}    # Create integration
GET    /api/v1/integrations/{id}    # List integrations
```

Full API documentation: See [Backend README](./backend/README.md)

## 🎨 Tech Stack

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State**: Zustand
- **HTTP**: Axios
- **Auth**: Clerk

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (Dev) / PostgreSQL (Prod)
- **Validation**: Pydantic v2
- **Auth**: Clerk (Optional)
- **Logging**: Python logging

## 📊 Phase Progress

### ✅ Phase 1: Multi-Tenant Foundation (COMPLETE)

- [x] Multi-tenant architecture
- [x] Tenant CRUD operations
- [x] API key management
- [x] Store integrations setup
- [x] Clerk authentication
- [x] Responsive dashboard
- [x] shadcn/ui components
- [x] Structured logging
- [x] Error handling
- [x] Delete tenant functionality

### 🚧 Phase 2: Case Management (Planned)

- [ ] Support ticket system
- [ ] AI response generation
- [ ] Human review workflow
- [ ] Analytics dashboard
- [ ] Knowledge base management
- [ ] Custom automation rules

### 🎯 Phase 3: Advanced Features (Future)

- [ ] Multi-language support
- [ ] Advanced reporting
- [ ] API rate limiting
- [ ] Webhook system
- [ ] Custom integrations
- [ ] Team collaboration

## 🔐 Security

- ✅ No hardcoded credentials
- ✅ Environment-based secrets
- ✅ CORS properly configured
- ✅ Optional Clerk authentication
- ✅ API key-based access
- ✅ Structured logging for auditing

## 📖 Documentation

- **[Backend Setup Guide](./backend/README.md)** - API, models, configuration
- **[Frontend Setup Guide](./frontend/README.md)** - Components, state, building
- **[Integration Guide](./support/LUXE_INTEGRATION_GUIDE.md)** - How to use Luxe
- **[API Reference](./backend/README.md#-api-endpoints)** - All endpoints

## 🚀 Deployment

### Development
```bash
# Start backend
cd backend && python -m uvicorn main:app --reload --port 8002

# Start frontend (new terminal)
cd frontend && npm run dev -- -p 3002
```

### Production

See deployment guides in:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

Recommended platforms:
- **Backend**: Railway, Heroku, AWS, DigitalOcean
- **Frontend**: Vercel, Netlify, AWS, DigitalOcean
- **Database**: PostgreSQL on managed service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes with clear messages
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

**Problem**: Port already in use
```bash
# Find and kill process
lsof -i :8002
kill -9 <PID>
```

**Problem**: Module not found
```bash
# Reinstall dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**Problem**: API connection error
- Ensure backend is running on http://localhost:8002
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`

See detailed troubleshooting in respective README files.

## 📞 Support & Feedback

- **Issues**: Create an issue on GitHub
- **Questions**: Check the documentation first
- **Feedback**: Email the development team

## 📄 License

This project is proprietary software. All rights reserved.

---

## 🎉 Getting Help

- 📚 Read the [Integration Guide](./support/LUXE_INTEGRATION_GUIDE.md)
- 🔧 Check [Backend README](./backend/README.md) for API details
- 💻 Check [Frontend README](./frontend/README.md) for UI setup
- 🐛 Report bugs in GitHub Issues

---

**Luxe v4.0** - Making customer support smarter, not harder.

Built with ❤️ using FastAPI, Next.js, and React.
