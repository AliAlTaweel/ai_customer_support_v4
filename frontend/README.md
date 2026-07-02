# Luxe v4.0 - AI Customer Support Frontend

Next.js 14-based frontend for the Luxe v4.0 multi-tenant AI customer support platform. Provides a responsive dashboard for tenant management, integrations, and case management.

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Building for Production](#building-for-production)
- [Project Structure](#project-structure)
- [Features](#features)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

Luxe v4.0 Frontend is a modern Next.js application that provides:

- **Multi-tenant dashboard** for managing customer support operations
- **Responsive UI** built with shadcn/ui components and Tailwind CSS
- **Real-time API integration** with structured logging
- **Clerk authentication** for secure user management
- **Tenant management** - create, update, delete organizations
- **API key management** for programmatic access
- **Integration setup** for Shopify, WooCommerce, and Stripe
- **Case/ticket management** (Phase 2)

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Next.js | 14.2.35 |
| Language | TypeScript | Latest |
| Styling | Tailwind CSS | 3.x |
| Components | shadcn/ui | Latest |
| State Management | Zustand | Latest |
| HTTP Client | Axios | Latest |
| Authentication | Clerk | Latest |
| Notifications | React Hot Toast | Latest |

## 📦 Prerequisites

- **Node.js** 18+ or higher
- **npm** or **yarn** (Node package manager)
- **Git** (for version control)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone git@github.com:AliAlTaweel/ai_customer_support_v4.git
cd ai_customer_support_v4/frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Environment Variables

Create a `.env.local` file in the frontend directory:

```bash
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_key
CLERK_SECRET_KEY=sk_test_your_clerk_secret

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8002
```

## ⚙️ Configuration

### Clerk Setup (Optional)

1. Create a Clerk account at [clerk.com](https://clerk.com)
2. Create a new application
3. Copy the publishable key to `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
4. Copy the secret key to `CLERK_SECRET_KEY`

### API Configuration

Ensure the backend is running on the specified `NEXT_PUBLIC_API_URL`:

```bash
# Development
NEXT_PUBLIC_API_URL=http://localhost:8002
```

## 🏃 Running the Application

### Development Mode

```bash
npm run dev -- -p 3002
```

Visit http://localhost:3002 in your browser.

### Hot Reload

The application automatically reloads when you save changes.

### Production Build

```bash
npm run build
npm run start
```

## 🏗️ Building for Production

### 1. Build the Application

```bash
npm run build
```

This creates an optimized production build in `.next/`.

### 2. Run Production Server

```bash
npm run start
```

### 3. Environment Variables

Ensure all environment variables are set for production:

```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_your_production_key
CLERK_SECRET_KEY=sk_live_your_production_secret
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## 📁 Project Structure

```
frontend/
├── app/                           # Next.js app directory
│   ├── layout.tsx                # Root layout with Clerk provider
│   ├── page.tsx                  # Home/landing page
│   ├── globals.css               # Global styles and CSS variables
│   └── dashboard/                # Dashboard routes
│       ├── layout.tsx            # Dashboard layout with sidebar
│       ├── page.tsx              # Overview/metrics page
│       ├── settings/
│       │   └── page.tsx          # Tenant management
│       ├── integrations/
│       │   └── page.tsx          # Store integrations
│       └── cases/
│           └── page.tsx          # Case management (Phase 2)
├── components/
│   └── ui/                       # shadcn/ui components
│       ├── button.tsx            # Button component
│       ├── card.tsx              # Card component
│       ├── input.tsx             # Input component
│       ├── form.tsx              # Form components
│       ├── table.tsx             # Table component
│       ├── dialog.tsx            # Dialog component
│       ├── dropdown-menu.tsx     # Dropdown component
│       └── badge.tsx             # Badge component
├── lib/
│   ├── api.ts                    # Axios instance with interceptors
│   ├── logger.ts                 # Structured logging utilities
│   ├── store.ts                  # Zustand state management
│   └── utils.ts                  # Utility functions
├── package.json                  # Dependencies and scripts
├── tsconfig.json                 # TypeScript configuration
├── tailwind.config.js            # Tailwind CSS configuration
├── components.json               # shadcn/ui configuration
└── .env.local                    # Environment variables (local)
```

## ✨ Features

### Phase 1: Multi-Tenant Foundation ✅

- [x] Multi-tenant dashboard
- [x] User authentication with Clerk
- [x] Tenant management (CRUD)
- [x] API key generation
- [x] Store integrations setup
- [x] Responsive UI with shadcn/ui
- [x] Structured logging
- [x] Delete tenant functionality

### Phase 2: Case Management (Future)

- [ ] Support ticket/case management
- [ ] Ticket assignment and routing
- [ ] Automation workflows
- [ ] Analytics and reporting
- [ ] Knowledge base management

## 📝 Environment Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | String | - | Clerk public key (visible in frontend) |
| `CLERK_SECRET_KEY` | String | - | Clerk secret key (server-side only) |
| `NEXT_PUBLIC_API_URL` | String | `http://localhost:8002` | Backend API URL |

## 📚 API Integration

The frontend communicates with the backend API via `lib/api.ts`:

```typescript
import { tenantApi, apiKeyApi, integrationApi } from '@/lib/api'

// Create tenant
const response = await tenantApi.create({
  name: "My Shop",
  supportEmail: "support@shop.com",
  tone: "professional",
  systemPrompt: "Help text..."
})

// List tenants
const tenants = await tenantApi.list()

// Update tenant
await tenantApi.update(tenantId, { name: "New Name" })

// Delete tenant
await tenantApi.delete(tenantId)

// Generate API key
const apiKey = await apiKeyApi.generate(tenantId)
```

## 🔍 Debugging

### Browser DevTools

Open DevTools (F12) to see:
- Console logs from the frontend
- Network requests to the API
- Redux DevTools for state management

### Logger

The application includes a structured logger:

```typescript
import { logger } from '@/lib/logger'

logger.info('Info message')
logger.warn('Warning message')
logger.error('Error message')
logger.success('Success message')
logger.api('POST', '/api/endpoint', 200)
```

### API Interceptors

All API requests/responses are logged automatically:

```typescript
// Enable/disable in lib/api.ts
logger.api(method, url, status)
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port 3002
lsof -i :3002

# Kill the process
kill -9 <PID>

# Or use a different port
npm run dev -- -p 3003
```

### API Connection Error

Ensure the backend is running:

```bash
# Backend should be running on port 8002
curl http://localhost:8002/health
```

Check `NEXT_PUBLIC_API_URL` in `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8002
```

### Module Not Found

Clear cache and reinstall dependencies:

```bash
rm -rf node_modules .next
npm install
npm run dev
```

### Clerk Authentication Error

1. Verify `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` is set
2. Check Clerk dashboard for API key validity
3. Ensure Clerk app is running and accessible

## 🚀 Performance Optimization

- **Code Splitting**: Next.js automatically splits code by route
- **Image Optimization**: Use `next/image` for automatic optimization
- **Lazy Loading**: Components load on demand
- **CSS Optimization**: Tailwind purges unused styles

## 🔐 Security Best Practices

- ✅ Never commit `.env.local` (in .gitignore)
- ✅ Keep `NEXT_PUBLIC_*` variables public-safe only
- ✅ Use `CLERK_SECRET_KEY` server-side only
- ✅ Validate all API responses
- ✅ Use HTTPS in production

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Clerk Documentation](https://clerk.com/docs)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

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

**Built with ❤️ using Next.js, React, and shadcn/ui**
