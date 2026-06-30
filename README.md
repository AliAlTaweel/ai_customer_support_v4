# AI Customer Support Platform (v4)

A Wilmo-like AI-native helpdesk for e-commerce businesses. Let AI handle 80%+ of support tickets while maintaining human control and oversight.

## 🎯 Vision

Build a white-label helpdesk where AI agents can understand the business context and take real actions:
- Process refunds in Shopify
- Generate return labels
- Check order status with real-time tracking
- Handle multilingual support across 40+ languages
- Learn from corrections and improve over time

## 📋 Phase 1: Multi-Tenant SaaS Foundation

**Goal:** Create a scalable, brand-aware backend for e-commerce support.

### ✅ Completed

- **Multi-tenant architecture** - Isolated data per customer
- **Tenant configuration** - Brand name, logo, custom prompts, tones
- **Authentication** - Clerk integration for user management
- **API Keys** - Secure authentication for external integrations
- **Integration framework** - Shopify, WooCommerce, Stripe ready
- **Admin Dashboard** - Manage tenants, settings, API keys
- **Stripe integration** - Payment processing (ready for Phase 2 billing)

### 📦 Tech Stack

**Backend:**
- FastAPI (Python)
- PostgreSQL (Prisma ORM)
- Clerk (Authentication)
- Stripe (Payments)

**Frontend:**
- Next.js 14 (TypeScript)
- Tailwind CSS
- Zustand (State management)
- Clerk Auth

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 13+
- Clerk account (free)
- Stripe account (free)

### 1. Clone and Setup

```bash
cd ai_customer_support_v4

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Environment Setup

Copy environment variables:
```bash
cp ../.env.example ../.env
```

Edit `.env` with your credentials:
```
DATABASE_URL="postgresql://user:password@localhost:5432/ai_customer_support"
CLERK_SECRET_KEY="sk_test_..."
CLERK_PUBLISHABLE_KEY="pk_test_..."
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_PUBLISHABLE_KEY="pk_test_..."
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

### 3. Database Setup

```bash
# Initialize Prisma
cd backend
npx prisma db push

# Create tables
prisma generate
```

### 4. Run Development Servers

**Backend (Terminal 1):**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

Visit http://localhost:3000

## 📚 API Documentation

### Tenants
```
POST   /api/v1/tenants              Create tenant
GET    /api/v1/tenants/:id          Get tenant
PUT    /api/v1/tenants/:id          Update tenant
GET    /api/v1/tenants/:id/metrics  Get metrics
GET    /api/v1/tenants              List tenants
```

### Authentication
```
POST   /api/v1/auth/signup          Create account
POST   /api/v1/auth/login           Login (Clerk)
GET    /api/v1/auth/me              Current user
POST   /api/v1/auth/tenant-users/:id Add user to tenant
```

### API Keys
```
POST   /api/v1/api-keys/:tenant_id  Generate key
GET    /api/v1/api-keys/:tenant_id  Get current key
```

### Integrations
```
POST   /api/v1/integrations/:tenant_id              Connect
GET    /api/v1/integrations/:tenant_id              List
GET    /api/v1/integrations/:tenant_id/:id          Get
DELETE /api/v1/integrations/:tenant_id/:id          Disconnect
POST   /api/v1/integrations/:tenant_id/:id/sync     Manual sync
```

## 🏗️ Project Structure

```
ai_customer_support_v4/
├── backend/
│   ├── main.py              FastAPI app entry
│   ├── config.py            Configuration
│   ├── db.py                Database connection
│   ├── auth.py              Authentication helpers
│   ├── schemas.py           Pydantic models
│   ├── routers/
│   │   ├── tenants.py       Tenant endpoints
│   │   ├── auth.py          Auth endpoints
│   │   ├── api_keys.py      API key endpoints
│   │   └── integrations.py  Integration endpoints
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx       Root layout
│   │   ├── page.tsx         Home page
│   │   └── dashboard/
│   │       ├── layout.tsx   Dashboard layout
│   │       ├── page.tsx     Overview
│   │       ├── settings/    Tenant management
│   │       ├── cases/       Cases (Phase 2)
│   │       └── integrations/ Integrations
│   ├── lib/
│   │   ├── api.ts          API client
│   │   └── store.ts        Zustand store
│   └── package.json
├── prisma/
│   └── schema.prisma        Database schema
└── README.md
```

## 🔐 Security Notes

- All sensitive data (API keys, tokens) stored encrypted
- Clerk handles user authentication securely
- Tenant data completely isolated (multi-tenant guards)
- API keys validated server-side
- CORS restricted to frontend origin

## 📈 Next Steps (Phase 2)

- [ ] Case/Ticket management system
- [ ] Dashboard with case filters
- [ ] Internal notes and tagging
- [ ] Agent assignment and routing
- [ ] SLA tracking

See `BUILD_PLAN.md` for full roadmap.

## 📞 Support

For issues or questions:
1. Check the BUILD_PLAN.md for detailed specifications
2. Review Clerk docs: https://clerk.com
3. Review Stripe docs: https://stripe.com/docs

## 📄 License

Proprietary - All rights reserved
