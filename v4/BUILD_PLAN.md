# AI Customer Support v4 - Wilmo-like SaaS Build Plan

**Vision:** Build a white-label AI-native helpdesk for e-commerce (like Wilmo.ai)  
**Current State:** Luxe AI chat system with multi-tenant foundation  
**Target:** Zendesk/Gorgias alternative powered by AI agents  

---

## Product Overview

### What We're Building
- **AI-Native Helpdesk** - Tickets resolved by AI autopilot (target 80%+)
- **E-commerce Focused** - Order tracking, returns, cancellations, complaints
- **Multi-Tenant SaaS** - Serve unlimited e-commerce brands
- **Integration Hub** - Connect to Shopify, WooCommerce, ERPs, shipping
- **Multilingual** - Support 40+ languages natively
- **Human Handoff** - Escalate intelligently when AI is uncertain

### Key Differentiators vs. Zendesk/Gorgias
- Built for AI first, not humans with AI bolted on
- No manual ticket work required
- Captures team expertise for training
- 24/7 support without scaling support staff
- Sub-60 second response times

### Target Market
- E-commerce stores (Shopify, WooCommerce)
- $500K-$10M annual revenue
- High support volume (50+ tickets/day)
- Current pain: rising support costs, slow response times

---

## Phased Roadmap

### Phase 1: Multi-Tenant SaaS Foundation (Weeks 1-3)
**Goal:** Create a scalable, brand-aware backend

#### Features
- [ ] Tenant configuration system
  - Brand name, logo, colors
  - Custom system prompts and tone
  - API keys and webhook URLs
  - Billing/subscription info
- [ ] Admin dashboard (internal)
  - Add/manage tenants
  - View metrics per tenant
  - Manage integrations
- [ ] Tenant-specific API authentication
  - API key generation
  - Webhook signing
- [ ] Basic onboarding flow
  - Tenant signup form
  - Stripe integration (payment)
  - Setup wizard

#### Database Changes
```prisma
model Tenant {
  id String @id @default(cuid())
  clerkOrgId String @unique
  name String
  logo String?
  colors Json? // { primary, secondary, accent }
  systemPrompt String @db.Text
  tone String // "professional", "friendly", "casual"
  supportEmail String
  webhookUrl String?
  apiKey String @unique
  status "active" | "trial" | "suspended"
  plan "starter" | "pro" | "enterprise"
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  // Relations
  integrations Integration[]
  cases Case[]
  users TenantUser[]
}

model TenantUser {
  id String @id @default(cuid())
  tenantId String
  userId String // Clerk user ID
  role "admin" | "agent" | "viewer"
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
}
```

#### API Endpoints (New)
```
POST   /api/v1/tenants              # Admin: Create tenant
GET    /api/v1/tenants/:id          # Get tenant config
PUT    /api/v1/tenants/:id          # Update tenant
GET    /api/v1/tenants/:id/metrics  # View tenant metrics

POST   /api/v1/auth/signup          # Customer signup
POST   /api/v1/auth/login           # Customer login (via Clerk)
POST   /api/v1/api-keys             # Generate API key
```

#### Frontend Changes
- New onboarding pages (signup, setup wizard)
- Admin tenant management dashboard
- Basic branding customization UI

#### Deliverables
✅ Can add new e-commerce tenant via signup flow  
✅ Each tenant has isolated data and custom configuration  
✅ Stripe integration for basic billing  

#### Success Metrics
- Add 2-3 test tenants
- Verify data isolation (tenant A can't see tenant B data)
- Verify custom prompts are used per tenant

---

### Phase 2: Ticket/Case Management System (Weeks 4-7)
**Goal:** Replace ad-hoc chat with proper helpdesk ticketing

#### Features
- [ ] Case/Ticket model
  - Unique ID (CASE-00001)
  - Status workflow: open → in-progress → resolved → closed
  - Priority: low, medium, high, urgent
  - Tags/categories (order-tracking, return-request, complaint, etc.)
  - Assigned agent
  - Customer info
  - Conversation history
- [ ] Support team dashboard
  - View all open cases (table view)
  - Filter by status, priority, tag, assignee
  - Sort by date, priority, age
  - Quick actions (assign, close, tag, note)
- [ ] Case detail page
  - Full conversation thread
  - Customer profile sidebar
  - Case metadata (status, priority, tags, assignee)
  - Add internal notes (visible to team only)
  - Add case tags
  - Manual escalation button
- [ ] Case assignment logic
  - Auto-assign to available agent
  - Round-robin routing
  - Skill-based routing (agents can specialize)
  - Manual assignment by admin
- [ ] SLA tracking
  - First response time
  - Resolution time
  - Breach notifications

#### Database Changes
```prisma
model Case {
  id String @id @default(cuid()) // CASE-00001 format
  tenantId String
  customerId String // From Shopify/WooCommerce
  subject String
  description String @db.Text
  status "open" | "in-progress" | "resolved" | "closed" @default("open")
  priority "low" | "medium" | "high" | "urgent" @default("medium")
  source "chat" | "email" | "web-form" @default("chat")
  
  assignedToId String? // TenantUser
  resolvedByAI Boolean @default(false)
  confidenceScore Float? // 0-1 (how confident is AI)
  
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  resolvedAt DateTime?
  
  messages Message[]
  tags CaseTag[]
  notes InternalNote[]
  
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  assignedTo TenantUser? @relation(fields: [assignedToId], references: [id])
}

model Message {
  id String @id @default(cuid())
  caseId String
  role "customer" | "agent" | "ai" // who sent it
  content String @db.Text
  isInternal Boolean @default(false) // only team sees
  createdAt DateTime @default(now())
  
  case Case @relation(fields: [caseId], references: [id], onDelete: Cascade)
}

model InternalNote {
  id String @id @default(cuid())
  caseId String
  agentId String
  content String @db.Text
  createdAt DateTime @default(now())
  
  case Case @relation(fields: [caseId], references: [id], onDelete: Cascade)
  agent TenantUser @relation(fields: [agentId], references: [id])
}

model CaseTag {
  id String @id @default(cuid())
  caseId String
  tag String // "order-tracking", "return-request", etc.
  
  case Case @relation(fields: [caseId], references: [id], onDelete: Cascade)
}
```

#### API Endpoints (New)
```
POST   /api/v1/cases                          # Create case (from chat/email)
GET    /api/v1/cases                          # List cases (with filters)
GET    /api/v1/cases/:caseId                  # Get case detail
PUT    /api/v1/cases/:caseId                  # Update case (status, priority, assignee)
POST   /api/v1/cases/:caseId/messages         # Add message to case
POST   /api/v1/cases/:caseId/notes            # Add internal note
POST   /api/v1/cases/:caseId/tags             # Add tags
POST   /api/v1/cases/:caseId/escalate         # Escalate to human

GET    /api/v1/dashboard                      # Agent dashboard (open cases, stats)
GET    /api/v1/dashboard/metrics              # SLA metrics, resolution time, etc.
```

#### Frontend Changes
- New "Cases" section (main nav)
- Cases dashboard (table of all cases)
- Case detail view
- Agent assignment UI
- Quick actions (close, tag, assign)
- Search/filter sidebar

#### Backend Changes
- Move `app/luxe/tools/chat_history.py` logic → cases system
- Extend `NativeAgentService` to create cases from conversations
- Add case assignment logic
- Add SLA tracking

#### Deliverables
✅ Support team can see all customer cases in one place  
✅ Cases track conversation history  
✅ Agents can assign, tag, and manage tickets  
✅ Dashboard shows open/resolved/closed counts  

#### Success Metrics
- Can create case from chat and view it
- Agents can filter by status, priority
- SLA metrics calculated correctly
- Case detail loads in <500ms

---

### Phase 3: E-commerce Integrations (Weeks 8-11)
**Goal:** Connect to real customer data (Shopify, WooCommerce)

#### Phase 3a: Core Integrations (Must-Have)

##### Shopify
- [ ] OAuth setup (get store access)
  - User authorizes Wilmo in Shopify app
  - Store access token stored in `TenantIntegration` table
- [ ] Real-time data sync
  - Orders API (list, get, update status, refund, cancel)
  - Products API (search, get details)
  - Customers API (get info, email, order history)
- [ ] Webhook listeners
  - Order created
  - Order updated
  - Customer created
  - Fulfillment updated
- [ ] Chat context enrichment
  - When customer types, fetch their recent orders
  - Show order status, tracking, payment status
  - Show 5 most recent orders in chat sidebar

##### WooCommerce
- [ ] REST API integration (simpler than Shopify)
  - API key/secret setup
  - Same endpoints as Shopify (orders, products, customers)
- [ ] Webhook setup
- [ ] Chat context enrichment (same as Shopify)

#### Phase 3b: Nice-to-Have Integrations
- Stripe (payment verification, failed payments)
- Shippo/EasyPost (real-time tracking)
- Klaviyo (customer segments)

#### Database Changes
```prisma
model Integration {
  id String @id @default(cuid())
  tenantId String
  type "shopify" | "woocommerce" | "stripe" | "shippo" | "klaviyo"
  status "connected" | "error" | "disconnected"
  
  // Shopify
  shopifyStoreName String? // mystore.myshopify.com
  shopifyAccessToken String? @db.Text
  
  // WooCommerce
  wooCommerceUrl String? // https://mysite.com
  wooCommerceKey String? @db.Text
  wooCommerceSecret String? @db.Text
  
  // Stripe
  stripeApiKey String? @db.Text
  
  lastSyncedAt DateTime?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
}

model Order {
  id String @id @default(cuid())
  tenantId String
  externalId String // shopify order ID
  customerId String // external customer ID
  
  orderNumber String // e.g., "#1001"
  status "pending" | "processing" | "shipped" | "delivered" | "cancelled" | "refunded"
  total Float
  currency String
  
  customerEmail String
  customerName String
  shippingAddress Json
  billingAddress Json
  
  lineItems Json // [{sku, name, quantity, price}]
  
  syncedAt DateTime @default(now())
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  
  @@unique([tenantId, externalId])
}

model Product {
  id String @id @default(cuid())
  tenantId String
  externalId String
  
  name String
  sku String
  description String? @db.Text
  price Float
  imageUrl String?
  
  syncedAt DateTime @default(now())
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  
  @@unique([tenantId, externalId])
}
```

#### API Endpoints (New)
```
POST   /api/v1/integrations                   # Connect new integration
GET    /api/v1/integrations                   # List connected integrations
DELETE /api/v1/integrations/:integrationId    # Disconnect integration
POST   /api/v1/integrations/:integrationId/sync  # Manual sync

GET    /api/v1/orders/:orderId                # Get order from external system
GET    /api/v1/orders?customerId=X            # Get customer orders
GET    /api/v1/products?search=X              # Search products
```

#### Frontend Changes
- New "Integrations" settings page
  - Connect Shopify/WooCommerce buttons
  - List connected integrations
  - Disconnect option
- Chat sidebar enhancement
  - Show customer's last 5 orders
  - Show order status, tracking, payment
  - Quick action: "Check order status", "Initiate refund"

#### Backend Changes
- New `app/luxe/services/shopify_service.py`
- New `app/luxe/services/woocommerce_service.py`
- Update `NativeAgentService` to include order context
- Add order/product tools (refactored)

#### Deliverables
✅ Can connect Shopify store (OAuth flow)  
✅ Can connect WooCommerce store (API key)  
✅ Real-time order data fetched and displayed  
✅ Chat shows customer order history + status  
✅ AI can see order context for better responses  

#### Success Metrics
- OAuth flow completes
- Customer orders displayed in chat
- Shopify/WooCommerce webhooks received
- Order data synced <60 seconds

---

### Phase 4: Autopilot & Smart Routing (Weeks 12-16)
**Goal:** AI decides which tickets to resolve vs. escalate

#### Features
- [ ] Confidence scoring
  - AI rates confidence 0-1 on every response
  - <70% = escalate to human
  - 70-90% = resolve with note to agent
  - >90% = auto-resolve, notify customer
- [ ] Auto-resolution logic
  - If AI is confident, close case automatically
  - Send resolution to customer
  - Log in case history
- [ ] Intelligent escalation
  - If AI unsure, create case for agent
  - Include AI's reasoning + attempted solution
  - Pre-assign to agent based on skill/availability
- [ ] Learning from feedback
  - Agent reviews AI resolution
  - "This was good" / "This was wrong"
  - Use feedback to improve future responses
- [ ] Case analytics
  - Track which case types AI handles well
  - Identify weak areas (refunds, complex returns)
  - Show improvement over time

#### Database Changes
```prisma
model CaseResolution {
  id String @id @default(cuid())
  caseId String
  
  resolvedByAI Boolean
  confidenceScore Float // 0-1
  aiResponse String @db.Text
  
  agentReview "correct" | "incorrect" | "partial" | "escalated"?
  agentFeedback String? @db.Text
  
  createdAt DateTime @default(now())
  case Case @relation(fields: [caseId], references: [id], onDelete: Cascade)
}

model AutopilotMetrics {
  id String @id @default(cuid())
  tenantId String
  
  totalCases Int
  aiResolvedCases Int
  escalatedCases Int
  correctResolutions Int // agentReview = "correct"
  
  autopilotRate Float // aiResolvedCases / totalCases
  accuracy Float // correctResolutions / aiResolvedCases
  
  date DateTime @default(now())
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
}
```

#### Algorithm Pseudocode
```python
def process_customer_message(tenant, customer, message):
  # Step 1: Get context
  order_context = fetch_customer_orders(customer)
  faq_context = search_faq(message)
  
  # Step 2: Generate AI response
  response = gemini.generate(
    system_prompt=tenant.systemPrompt,
    context={"orders": order_context, "faq": faq_context},
    user_message=message
  )
  
  # Step 3: Score confidence
  confidence = score_confidence(response, message_type)
  
  # Step 4: Decide action
  if confidence > 0.9:
    # Auto-resolve
    case.status = "resolved"
    case.resolvedByAI = True
    send_customer_email(customer, response)
    log_resolution(case, response, confidence)
  
  elif confidence > 0.7:
    # Create case, resolve with note
    case = create_case(customer, message, response)
    case.status = "resolved"
    case.resolvedByAI = True
    add_note(case, "AI-resolved with confidence {confidence}")
    send_customer_email(customer, response)
  
  else:
    # Escalate to human
    case = create_case(customer, message, response)
    case.status = "open"
    agent = assign_agent(case, tenant)
    add_note(case, "AI escalated. Confidence: {confidence}. Attempted: {response}")
    
  return case
```

#### API Endpoints (New)
```
GET    /api/v1/autopilot/metrics              # Autopilot rate, accuracy, trends
GET    /api/v1/autopilot/feedback             # Cases needing agent review
POST   /api/v1/autopilot/feedback/:caseId     # Agent marks AI as correct/wrong
GET    /api/v1/autopilot/weak-areas           # Categories AI struggles with
```

#### Frontend Changes
- Dashboard enhancement
  - "Autopilot Rate: 82%" metric
  - Chart: autopilot rate over time
  - List of "AI-resolved" cases
  - Feedback widget for agents ("Mark this resolution as correct/wrong")
- Case detail enhancement
  - Show "Resolved by AI" badge
  - Show confidence score
  - Allow agent to mark correct/incorrect

#### Backend Changes
- Update `NativeAgentService` to return confidence score
- Add `score_confidence()` function
- Add autopilot logic to case creation
- Track metrics in database

#### Deliverables
✅ AI returns confidence score with every response  
✅ High-confidence cases auto-resolve  
✅ Low-confidence cases escalate to agent  
✅ Autopilot rate calculated and shown  
✅ Agent can mark AI as correct/wrong for learning  

#### Success Metrics
- Autopilot rate >70% on simple queries
- Accuracy (agent feedback) >80%
- Escalation rate <30%
- Time-to-resolution <2 minutes

---

### Phase 5: Multichannel Support (Weeks 17-20)
**Goal:** Support beyond chat (email, web forms)

#### Phase 5a: Email Integration (Priority)
- [ ] Inbound email handling
  - Parse customer emails to support address
  - Create case from email thread
  - Extract customer email/name
- [ ] Case-to-email conversion
  - Send AI response via email
  - Include reply-to case address
- [ ] Email threading
  - Group replies into same case
  - Show full conversation in case
  - Detect "Re:" chains

#### Phase 5b: Web Form Integration
- [ ] Embeddable form builder
  - Customer can customize form fields
  - Auto-fill customer info if logged in
  - Multi-step forms
- [ ] Form submission → Case creation
  - Auto-populate case from form data
  - Map form fields to case metadata
- [ ] Form placement
  - Embed on customer website
  - Link from help center

#### Database Changes
```prisma
model ContactForm {
  id String @id @default(cuid())
  tenantId String
  
  name String
  fields Json // [{name, type, required, placeholder}]
  submitButtonText String
  successMessage String
  theme Json // colors, logo, etc
  
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  submissions ContactFormSubmission[]
}

model ContactFormSubmission {
  id String @id @default(cuid())
  formId String
  
  submitterEmail String
  submitterName String
  data Json // {field1: value1, field2: value2, ...}
  
  caseId String
  createdAt DateTime @default(now())
  
  form ContactForm @relation(fields: [formId], references: [id], onDelete: Cascade)
  case Case @relation(fields: [caseId], references: [id], onDelete: Cascade)
}

model EmailThread {
  id String @id @default(cuid())
  tenantId String
  caseId String
  
  messageId String @unique // email message ID
  inReplyTo String? // email in-reply-to
  
  subject String
  from String
  to String
  body String @db.Text
  receivedAt DateTime
  
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  case Case @relation(fields: [caseId], references: [id], onDelete: Cascade)
}
```

#### API Endpoints (New)
```
POST   /api/v1/contact-forms                  # Create form
GET    /api/v1/contact-forms/:formId          # Get form (embed on website)
POST   /api/v1/contact-forms/:formId/submit   # Submit form
GET    /api/v1/contact-forms/submissions      # List submissions

POST   /webhooks/email                        # Inbound email handler
```

#### Frontend Changes
- New "Channels" settings page
  - Email configuration (IMAP/SMTP)
  - Form builder (drag-drop)
  - Embed code generator
- Contact form preview
  - Live preview of form
  - Test submission

#### Backend Changes
- Email listener service (poll inbound email)
- Email parsing service (extract customer, body, attachments)
- Form submission handler
- Email reply service (send responses via email)

#### Deliverables
✅ Can receive support emails and create cases  
✅ Can respond via email (case replies show in customer email)  
✅ Can create custom contact forms  
✅ Form submissions create cases  
✅ Email threads grouped in case  

#### Success Metrics
- Email received and case created <1 minute
- Email reply shows in customer inbox
- Form submission → case creation works
- <1 second email validation

---

### Phase 6: Analytics & Self-Serve Dashboard (Weeks 21-23)
**Goal:** Show customers their ROI

#### Features
- [ ] Public metrics dashboard (customer-facing)
  - Autopilot rate (% tickets handled by AI)
  - Average resolution time
  - Cost savings (estimated hours saved × hourly rate)
  - Customer satisfaction (CSAT from cases)
  - Uptime %
- [ ] Trends & charts
  - Autopilot rate over time (line chart)
  - Cases by category (pie chart)
  - Response time trend
  - Top issues (bar chart)
- [ ] Performance by category
  - Which case types does AI handle best?
  - Order tracking: 95% autopilot
  - Returns: 80% autopilot
  - Custom inquiries: 50% autopilot
- [ ] SLA monitoring
  - First response time (target: <1 minute)
  - Resolution time (target: <24 hours)
  - SLA breaches highlighted
- [ ] Export reports
  - CSV export of metrics
  - Monthly summary email

#### Database Changes
```prisma
model CaseMetrics {
  id String @id @default(cuid())
  tenantId String
  
  // Counts
  totalCases Int
  openCases Int
  resolvedCases Int
  escalatedCases Int
  
  // Autopilot
  aiResolvedCases Int
  autopilotRate Float // 0-1
  accuracy Float // 0-1
  
  // Time
  avgResolutionTime Float // minutes
  avgFirstResponseTime Float // minutes
  
  // SLA
  slaBreaches Int
  slaMeetRate Float // 0-1
  
  // Satisfaction
  averageCsat Float // 1-5
  
  // Costs
  estimatedHoursSaved Float
  costSavings Float // USD
  
  date DateTime @default(now())
  month Int // 1-12
  year Int
  
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
}
```

#### API Endpoints (New)
```
GET    /api/v1/dashboard/metrics              # Current metrics
GET    /api/v1/dashboard/metrics/history?range=30d  # Historical data
GET    /api/v1/dashboard/by-category          # Metrics by case type
GET    /api/v1/dashboard/export?format=csv    # Export metrics
```

#### Frontend Changes
- New public "Dashboard" (available to all tenant users)
  - KPI cards (autopilot rate, avg resolution time, cost savings)
  - Trend chart (autopilot rate over 30 days)
  - Category breakdown (pie chart)
  - SLA status
  - Export button (CSV)

#### Backend Changes
- Daily metrics aggregation job (calculate metrics per tenant)
- Metrics calculation service
- Cost estimation formula

#### Deliverables
✅ Dashboard shows autopilot rate, resolution time, cost savings  
✅ Metrics tracked daily  
✅ Historical data available  
✅ Can export CSV  

#### Success Metrics
- Dashboard loads in <500ms
- Metrics calculated accurately
- CSV export generates <5 seconds

---

### Phase 7: Multilingual & Advanced Features (Weeks 24-27)
**Goal:** Go global, add depth

#### Phase 7a: Multilingual Support (Weeks 24-25)

- [ ] Language detection
  - Detect customer language from message
  - Store language preference per customer
- [ ] Prompt translation
  - Translate system prompt to customer's language
  - Use Claude for natural translations
- [ ] Response translation
  - AI responds in customer's language
  - Fallback: translate English response
- [ ] Support for 15+ languages
  - All major languages (EN, ES, FR, DE, IT, PT, RU, ZH, JA, KO, etc.)
  - Store language setting per tenant
  - Let tenant choose "auto-detect" or "fixed language"

#### Phase 7b: Knowledge Base (Weeks 25-26)

- [ ] Customer can upload FAQ/documentation
  - CSV, PDF, markdown, or paste text
  - Parse and chunk documents
- [ ] RAG search
  - Embed documents using GeminiEmbeddings
  - Store embeddings in Supabase pgvector
  - Search during case processing
- [ ] AI learns from docs
  - System prompt includes relevant docs
  - AI can reference customer's docs in responses
  - "According to your knowledge base: ..."

#### Phase 7c: Advanced Analytics (Weeks 26-27)

- [ ] A/B testing prompts
  - Test two system prompts
  - Compare autopilot rate, accuracy
  - Auto-switch to better prompt
- [ ] Performance by time-of-day
  - Which hours get most tickets?
  - When is AI most accurate?
- [ ] Customer segment analytics
  - VIP customers vs regular
  - New customers vs repeat
  - By product category

#### Database Changes
```prisma
model CustomerKnowledgeBase {
  id String @id @default(cuid())
  tenantId String
  
  name String
  sourceType "csv" | "pdf" | "markdown" | "text"
  uploadedAt DateTime
  
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  documents KBDocument[]
}

model KBDocument {
  id String @id @default(cuid())
  knowledgeBaseId String
  
  title String
  content String @db.Text
  embedding Vector(768) // GeminiEmbeddings
  
  createdAt DateTime @default(now())
  kb CustomerKnowledgeBase @relation(fields: [knowledgeBaseId], references: [id], onDelete: Cascade)
}

model PromptVariant {
  id String @id @default(cuid())
  tenantId String
  
  name String
  prompt String @db.Text
  isActive Boolean @default(false)
  
  autopilotRate Float?
  accuracy Float?
  
  createdAt DateTime @default(now())
  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)
}
```

#### API Endpoints (New)
```
POST   /api/v1/knowledge-base/upload          # Upload FAQ/docs
GET    /api/v1/knowledge-base                 # List documents
DELETE /api/v1/knowledge-base/:docId          # Delete document

POST   /api/v1/prompts/variants               # Create prompt variant
POST   /api/v1/prompts/variants/:id/activate  # Switch to variant
GET    /api/v1/prompts/compare                # Compare A/B test results

GET    /api/v1/analytics/by-language          # Metrics per language
GET    /api/v1/analytics/by-segment           # Metrics per customer segment
```

#### Frontend Changes
- New "Knowledge Base" section
  - Upload documents
  - List/preview documents
  - Delete option
- Prompt management
  - Create/edit system prompts
  - Create variants for A/B testing
  - View A/B test results
- Analytics enhancements
  - Filter by language
  - Filter by customer segment
  - Drilldown by category

#### Backend Changes
- Language detection service
- Document embedding & storage
- RAG search service
- A/B testing logic
- Prompt variant selection

#### Deliverables
✅ Multilingual support (40+ languages)  
✅ Can upload FAQ documents  
✅ AI includes relevant docs in responses  
✅ A/B testing for prompts  
✅ Analytics by language & segment  

#### Success Metrics
- Language detection >95% accurate
- Document search returns relevant results
- Multilingual responses are natural
- A/B test detects improvement in <500 cases

---

## Technical Architecture

### System Design
```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend (Next.js)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Chat UI    │  │  Dashboard   │  │   Settings   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Backend API (Python/FastAPI)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Chat Endpoint│  │Case Endpoint │  │Integration   │       │
│  │              │  │  (Tickets)   │  │ Endpoints    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ NativeAgent  │  │   FastTrack  │  │   Autopilot  │       │
│  │  (LLM)       │  │   (Fast Path)│  │   (Logic)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│         Integrations & External Services                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Shopify API │  │  WooCommerce │  │  Google LLM  │       │
│  │              │  │     API      │  │  (Gemini)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Database (Supabase PostgreSQL)              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tenants  │  Cases  │  Messages  │  Integrations   │   │
│  │  Orders   │  Products│ Metrics  │  KB Documents    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### New Services to Create
- `TenantConfigService` - Brand customization
- `CaseManagementService` - Ticket lifecycle
- `IntegrationService` - Shopify/WooCommerce abstraction
- `AutopilotService` - AI decision logic
- `AnalyticsService` - Metrics calculation
- `EmailService` - Inbound/outbound email
- `KnowledgeBaseService` - RAG search
- `MultilingualService` - Language detection & translation

### Key Changes to Existing Services
- `NativeAgentService` - Add confidence scoring, tenant context
- `FastTrackService` - Extend for autopilot routing
- `ChatInterface.tsx` - Switch from direct chat to case-based
- `main.py` - Add new routers for cases, integrations, analytics

---

## Development Priorities

### MVP Path (Weeks 1-11, "v4 Alpha")
**Ship something usable to first customer:**

1. Phase 1: Multi-Tenant Foundation
2. Phase 2: Ticket Management
3. Phase 3a: Shopify integration only

**Minimal frontend:** Basic case dashboard + settings

### Post-MVP (Weeks 12-27, "v4 Beta")
1. Phase 4: Autopilot
2. Phase 5a: Email
3. Phase 6: Analytics

### Polish & Scale (Weeks 27+)
1. Phase 3b, 5b, 7

---

## Resource Estimate

| Phase | Duration | Dev Time | QA Time | Total |
|-------|----------|----------|---------|-------|
| 1: Foundation | 3 weeks | 60h | 20h | 80h |
| 2: Cases | 4 weeks | 80h | 20h | 100h |
| 3a: Integrations | 4 weeks | 80h | 20h | 100h |
| 4: Autopilot | 5 weeks | 100h | 30h | 130h |
| 5a: Email | 2 weeks | 40h | 10h | 50h |
| 6: Analytics | 3 weeks | 60h | 15h | 75h |
| 7: Multilingual | 4 weeks | 80h | 20h | 100h |
| **Total** | **27 weeks** | **500h** | **135h** | **635h** |

**Team:** 1-2 full-stack engineers

---

## Success Metrics & KPIs

### Product Metrics
- **Autopilot Rate** - Target: 80%+ by Week 16
- **Accuracy** - Target: 90%+ agent feedback
- **CSAT** - Target: 4.5/5 stars
- **Time-to-Resolution** - Target: <2 hours
- **SLA Compliance** - Target: 95%

### Business Metrics
- **Time to Launch** - Alpha by Week 11
- **Customer Acquisition** - 3+ paying customers by Week 16
- **MRR** - $5K+ by Week 27
- **Churn** - <5%
- **NPS** - >50

### Technical Metrics
- **API Response Time** - <500ms (p95)
- **Uptime** - 99.5%
- **Error Rate** - <0.1%
- **Database Latency** - <50ms (p95)

---

## Risk Mitigation

### Technical Risks
- **Risk:** Shopify/WooCommerce API rate limits
  - **Mitigation:** Implement queue/batch processing, caching
  
- **Risk:** LLM hallucinations affecting autopilot
  - **Mitigation:** Confidence scoring, extensive testing, human feedback loop
  
- **Risk:** Data isolation bugs (tenant A sees tenant B data)
  - **Mitigation:** Automated tests, tenant-scoped queries everywhere, code review

- **Risk:** Email deliverability (emails go to spam)
  - **Mitigation:** Use SendGrid/AWS SES, DKIM/SPF setup, gradual warmup

### Product Risks
- **Risk:** Market wants different features
  - **Mitigation:** Early customer interviews (Phase 1), beta testing, pivot quickly

- **Risk:** Pricing model doesn't work
  - **Mitigation:** Flexible pricing (per-seat, per-ticket, per-AI-resolution), gather feedback

### Business Risks
- **Risk:** Competitor launches similar product
  - **Mitigation:** Move fast, differentiate on UX, build moat (integrations, KB learning)

---

## Go-to-Market Strategy

### Phase 1-2 (MVP Launch)
- Target: E-commerce stores with $500K-$5M ARR
- Channels: ProductHunt, e-commerce communities, direct outreach
- Messaging: "Zendesk without the support team"
- Pricing: Free trial → $500/month (Pro) → custom (Enterprise)

### Phase 3-4 (Traction)
- Expand to $5M-$50M ARR stores
- Add more integrations based on feedback
- Improve autopilot accuracy
- Testimonials: "92% of tickets handled by AI"

### Phase 5+ (Scale)
- Enterprise features (SLA guarantees, custom workflows)
- Multilingual expansion
- Partnership integrations (Shopify App Store, etc.)
- IPO potential ($100M+ ARR)

---

## Checklist for Each Phase

### Phase 1
- [ ] Tenant model + migration
- [ ] Clerk multi-org setup
- [ ] Stripe payment integration
- [ ] Onboarding flow complete
- [ ] Data isolation verified
- [ ] Deployed to staging

### Phase 2
- [ ] Case model + migration
- [ ] Dashboard backend + frontend
- [ ] Assignment + escalation logic
- [ ] SLA tracking working
- [ ] Chat → Case conversion
- [ ] Agent workflows tested

### Phase 3a
- [ ] Shopify OAuth setup
- [ ] API integration working
- [ ] Webhooks receiving data
- [ ] Order context in chat
- [ ] Real data loaded from store

### Phase 4
- [ ] Confidence scoring algorithm
- [ ] Auto-resolve logic
- [ ] Escalation rules
- [ ] Feedback collection
- [ ] Autopilot metrics calculated

### Phase 5a
- [ ] Email parsing service
- [ ] Case creation from email
- [ ] Email replies sending
- [ ] Threading working

### Phase 6
- [ ] Metrics aggregation daily
- [ ] Dashboard displaying data
- [ ] Charts rendering
- [ ] Export working

### Phase 7a
- [ ] Language detection
- [ ] Prompt translation
- [ ] Response translation
- [ ] 15+ languages tested

---

## Timeline Summary

```
Week  1-3   : Phase 1 - Foundation ✓
Week  4-7   : Phase 2 - Cases ✓
Week  8-11  : Phase 3 - Integrations ✓
            >>> ALPHA LAUNCH (First Customer)
Week 12-16  : Phase 4 - Autopilot ✓
Week 17-20  : Phase 5 - Multichannel ✓
            >>> BETA LAUNCH (3+ Customers)
Week 21-23  : Phase 6 - Analytics ✓
Week 24-27  : Phase 7 - Multilingual ✓
            >>> GA LAUNCH (Public)
```

---

## Conclusion

This is a 27-week build to launch a Wilmo-like AI customer support SaaS. Start with MVP (Phase 1-3a), get paying customers, then build out autopilot and multichannel.

**Next Steps:**
1. Validate market demand (customer interviews)
2. Finalize pricing model
3. Start Phase 1 (Week 1)
