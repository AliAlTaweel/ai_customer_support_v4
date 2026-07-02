from beanie import Document, PydanticObjectId
from pydantic import Field
from datetime import datetime
from typing import Optional, List
import uuid

class Tenant(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    clerk_org_id: str
    name: str
    logo: Optional[str] = None
    colors: Optional[dict] = None
    system_prompt: str = Field(default="You are a helpful customer support AI agent. Be professional and concise.")
    tone: str = Field(default="professional")
    support_email: str
    webhook_url: Optional[str] = None
    api_key: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = Field(default="trial")
    plan: str = Field(default="starter")
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tenants"


class TenantUser(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    tenant_id: str
    user_id: str
    role: str = Field(default="agent")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tenant_users"


class Integration(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    tenant_id: str
    type: str
    status: str = Field(default="disconnected")
    shopify_store_name: Optional[str] = None
    shopify_access_token: Optional[str] = None
    woocommerce_url: Optional[str] = None
    woocommerce_key: Optional[str] = None
    woocommerce_secret: Optional[str] = None
    stripe_api_key: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "integrations"


class Case(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    tenant_id: str
    integration_id: str
    customer_email: str
    customer_name: Optional[str] = None
    subject: str
    description: str
    status: str = Field(default="open")
    priority: str = Field(default="medium")
    assigned_to: Optional[str] = None
    ai_response: Optional[str] = None
    human_response: Optional[str] = None
    ai_confidence: str = Field(default="medium")
    external_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "cases"


class CaseMessage(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    case_id: str
    sender: str
    sender_email: Optional[str] = None
    content: str
    message_type: str = Field(default="message")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "case_messages"
