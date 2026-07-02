# Luxe v4.0 Integration Guide

Complete guide to integrate Luxe v4.0 AI Assistant into your ecommerce store.

## Prerequisites

- Luxe v4.0 deployed and running
  - Backend: `http://localhost:8002`
  - Frontend: `http://localhost:3002`
- Ecommerce store (Shopify, WooCommerce, or custom)
  - Backend: `http://localhost:8003`
  - Frontend: `http://localhost:3003`

---

## Step 1: Deploy Luxe v4.0

### Start Backend Server
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

**Backend running at:** `http://localhost:8002`

### Start Frontend Server
```bash
cd frontend
npm install
npm run dev -- -p 3002
```

**Frontend running at:** `http://localhost:3002`

### Environment Configuration
Create or update `.env.local` in frontend:
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key
CLERK_SECRET_KEY=your_clerk_secret
NEXT_PUBLIC_API_URL=http://localhost:8002
```

---

## Step 2: Create a Tenant for Your Ecommerce Shop

1. Open Luxe dashboard: `http://localhost:3002/dashboard`
2. Go to **Settings** tab
3. Click **+ New Tenant** button
4. Fill in the form:
   - **Organization Name:** `ecommerce_shop` (or your store name)
   - **Support Email:** `your-email@shop.com`
   - **Brand Tone:** Choose appropriate tone (professional/friendly/casual)
   - **System Prompt:** Custom instructions for AI behavior (see below)

### Example System Prompt
```
You are a helpful and friendly customer service assistant for [Your Store Name]. 
Your role is to help customers with:
- Product information and recommendations
- Order tracking and status
- Returns and refunds
- Shipping and delivery questions
- General FAQs

Be concise, helpful, and always maintain a professional tone.
When you don't know something, ask for clarification or direct to human support.
```

5. Click **Create Tenant**

---

## Step 3: Connect Your Ecommerce Store

### For Shopify Stores
1. In dashboard, go to **Integrations** tab
2. Click **Connect Shopify**
3. Authenticate with your Shopify admin credentials
4. Grant permissions for:
   - Reading products
   - Reading orders
   - Reading customers
5. Luxe will sync your store data

### For WooCommerce Stores
1. In dashboard, go to **Integrations** tab
2. Click **Connect WooCommerce**
3. Enter your store URL and API credentials
4. Grant necessary permissions
5. Data sync will begin automatically

### For Custom ecommerce Platform
Use the REST API to connect:
```bash
curl -X POST http://localhost:8000/api/integrations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d {
    "type": "custom",
    "name": "ecommerce_shop",
    "config": {
      "products_endpoint": "https://your-store.com/api/products",
      "orders_endpoint": "https://your-store.com/api/orders"
    }
  }
```

---

## Step 4: Configure AI Assistant

### Set Up Knowledge Base
1. Go to **Settings**
2. Update **System Prompt** with specific info:
   - Store policies
   - Return/refund procedures
   - Shipping information
   - Common FAQs

### Upload FAQ/Knowledge Base (Optional)
You can upload a PDF or document with:
- Product specifications
- Common questions and answers
- Policies and procedures
- Troubleshooting guides

---

## Step 5: Get Your API Key

1. In **Settings**, find **API Key** section
2. Copy the API key (shown masked as `sk_test_...`)
3. Save this securely - you'll need it for:
   - Embedding chat widget in your store
   - Making API calls from your backend
   - Webhooks and integrations

### Generate New Key
If needed, click **Generate New Key** to create a fresh API key.

---

## Step 6: Embed Chat Widget in Your Store

### Option A: React Component (Next.js/React Store)

```tsx
// components/LuxeChatWidget.tsx
import { useState } from 'react'
import axios from 'axios'

export default function LuxeChatWidget() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(
        'http://localhost:8002/api/v1/chat',
        {
          tenant_id: 'YOUR_TENANT_ID',
          message: input,
          conversation_id: 'customer_123'
        },
        {
          headers: {
            'Authorization': `Bearer YOUR_API_KEY`,
            'Content-Type': 'application/json'
          }
        }
      )

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed bottom-4 right-4 w-96 h-96 bg-white rounded-lg shadow-lg p-4 flex flex-col">
      <h3 className="font-bold mb-4">Chat with AI Assistant</h3>
      
      <div className="flex-1 overflow-y-auto mb-4 space-y-2">
        {messages.map((msg, i) => (
          <div key={i} className={`p-2 rounded ${msg.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'}`}>
            {msg.content}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your question..."
          className="flex-1 p-2 border rounded"
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  )
}
```

### Option B: HTML/JavaScript (Any Store)

```html
<!-- Add to your store's footer or header -->
<div id="luxe-chat-widget"></div>

<script>
  const LUXE_API_KEY = 'YOUR_API_KEY'
  const LUXE_TENANT_ID = 'YOUR_TENANT_ID'
  const LUXE_API_URL = 'http://localhost:8002'

  async function sendMessage(message) {
    const response = await fetch(`${LUXE_API_URL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${LUXE_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        tenant_id: LUXE_TENANT_ID,
        message: message,
        conversation_id: `customer_${new Date().getTime()}`
      })
    })

    const data = await response.json()
    return data.response
  }

  // Initialize widget
  document.getElementById('luxe-chat-widget').innerHTML = `
    <div style="position: fixed; bottom: 20px; right: 20px; width: 400px; height: 500px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; flex-direction: column; z-index: 9999;">
      <div style="padding: 15px; background: #0284c7; color: white; font-weight: bold; border-radius: 8px 8px 0 0;">
        AI Assistant
      </div>
      <div id="chat-messages" style="flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px;"></div>
      <div style="padding: 15px; display: flex; gap: 10px; border-top: 1px solid #ccc;">
        <input id="chat-input" type="text" placeholder="Ask me anything..." style="flex: 1; padding: 8px; border: 1px solid #ccc; border-radius: 4px;" />
        <button id="send-btn" style="padding: 8px 15px; background: #0284c7; color: white; border: none; border-radius: 4px; cursor: pointer;">Send</button>
      </div>
    </div>
  `

  document.getElementById('send-btn').addEventListener('click', async () => {
    const input = document.getElementById('chat-input')
    const message = input.value.trim()
    if (!message) return

    // Display user message
    const messagesDiv = document.getElementById('chat-messages')
    messagesDiv.innerHTML += `<div style="text-align: right; background: #e3f2fd; padding: 8px; border-radius: 4px; margin-left: 40px;">${message}</div>`

    input.value = ''

    // Get AI response
    const response = await sendMessage(message)
    messagesDiv.innerHTML += `<div style="background: #f5f5f5; padding: 8px; border-radius: 4px; margin-right: 40px;">${response}</div>`
    messagesDiv.scrollTop = messagesDiv.scrollHeight
  })
</script>
```

---

## Step 7: Monitor & Manage

### Dashboard Analytics
- View customer conversations
- Track AI performance
- See FAQ effectiveness
- Monitor response accuracy

### Admin Features
1. **Cases Tab** - View and manage support tickets
2. **Integrations** - Manage connected stores
3. **Settings** - Update AI behavior and policies
4. **Analytics** - Performance metrics

### Manage Tenants

#### View/Update Tenant
1. Go to Settings → Select tenant from left sidebar
2. Edit tenant details (name, email, tone, system prompt)
3. Click **Save Changes**

#### Delete Tenant
1. Go to Settings → Select tenant
2. Scroll to **Danger Zone** (red section at bottom)
3. Click **Delete Tenant**
4. Confirm deletion (irreversible)
   - Deletes all tenant data
   - Removes all cases and integrations
   - Cannot be undone

#### Generate New API Key
1. Go to Settings → Select tenant
2. In **API Key** section, click **Generate New Key**
3. Copy the new key for integrations

---

## API Reference

### Create Tenant
```bash
POST http://localhost:8002/api/v1/tenants
Content-Type: application/json

{
  "name": "My Shop",
  "supportEmail": "support@shop.com",
  "tone": "professional",
  "systemPrompt": "You are a helpful assistant..."
}
```

### Send Message (Chat)
```bash
POST http://localhost:8002/api/v1/chat
Authorization: Bearer YOUR_API_KEY

{
  "tenant_id": "your_tenant_id",
  "message": "Where is my order?",
  "conversation_id": "customer_123"
}

Response:
{
  "response": "Your order #12345 is being shipped...",
  "confidence": 0.95,
  "resolved": true
}
```

### Get Tenant Info
```bash
GET http://localhost:8002/api/v1/tenants/YOUR_TENANT_ID
Authorization: Bearer YOUR_API_KEY
```

### List Tenants
```bash
GET http://localhost:8002/api/v1/tenants
Authorization: Bearer YOUR_API_KEY
```

### Delete Tenant
```bash
DELETE http://localhost:8002/api/v1/tenants/YOUR_TENANT_ID
Authorization: Bearer YOUR_API_KEY
```

---

## Troubleshooting

### Chat not responding?
- Check backend is running: `curl http://localhost:8000/health`
- Verify API key is correct
- Check tenant_id matches

### Store not syncing?
- Re-authenticate in Integrations tab
- Check store API credentials
- Look at backend logs for errors

### AI giving wrong answers?
- Update system prompt with correct information
- Upload FAQ/knowledge base
- Review and train on customer queries

---

## Deployment (Production)

When ready to deploy to production:

1. **Deploy Backend** (e.g., AWS, Heroku, Railway)
   - Update database to PostgreSQL
   - Set environment variables
   - Run migrations

2. **Deploy Frontend** (e.g., Vercel, Netlify)
   - Update API_URL to production backend
   - Configure Clerk production keys
   - Set environment variables

3. **Update Chat Widget** in your store
   - Change API_URL to production
   - Use production API key
   - Test thoroughly

---

## Support

For issues or questions:
- Check logs: `backend/logs/app.log`
- Review API responses
- Test with curl commands
- Check Luxe dashboard for errors

