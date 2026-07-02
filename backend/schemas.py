from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List
from datetime import datetime

# Tenant Schemas
class TenantCreate(BaseModel):
    name: str
    supportEmail: EmailStr
    tone: str = "professional"
    systemPrompt: Optional[str] = None
    logo: Optional[str] = None
    colors: Optional[Dict] = None

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    colors: Optional[Dict] = None
    tone: Optional[str] = None
    systemPrompt: Optional[str] = None
    supportEmail: Optional[EmailStr] = None

class TenantResponse(BaseModel):
    id: str
    name: str
    logo: Optional[str] = None
    colors: Optional[Dict] = None
    systemPrompt: str = Field(alias='system_prompt')
    tone: str
    supportEmail: str = Field(alias='support_email')
    apiKey: str = Field(alias='api_key')
    status: str
    plan: str
    createdAt: datetime = Field(alias='created_at')
    updatedAt: datetime = Field(alias='updated_at')

    class Config:
        from_attributes = True
        populate_by_name = True

# Tenant User Schemas
class TenantUserCreate(BaseModel):
    userId: str
    role: str = "agent"

class TenantUserUpdate(BaseModel):
    role: str

class TenantUserResponse(BaseModel):
    id: str
    tenantId: str
    userId: str
    role: str
    createdAt: datetime

    class Config:
        from_attributes = True

# Integration Schemas
class IntegrationCreate(BaseModel):
    type: str  # "shopify", "woocommerce", etc.
    shopifyStoreName: Optional[str] = None
    shopifyAccessToken: Optional[str] = None
    wooCommerceUrl: Optional[str] = None
    wooCommerceKey: Optional[str] = None
    wooCommerceSecret: Optional[str] = None
    stripeApiKey: Optional[str] = None

class IntegrationResponse(BaseModel):
    id: str
    tenantId: str
    type: str
    status: str
    lastSyncedAt: Optional[datetime]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# Auth Schemas
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    organizationName: str
    organizationSlug: str

class SignupResponse(BaseModel):
    userId: str
    organizationId: str
    organizationName: str
    email: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# API Key Schemas
class ApiKeyResponse(BaseModel):
    key: str
    createdAt: datetime

# Case Schemas (Phase 2)
class CaseMessageCreate(BaseModel):
    senderEmail: str
    senderName: Optional[str] = None
    content: str
    messageType: str = "message"

class CaseMessageResponse(BaseModel):
    id: str
    caseId: str
    sender: str
    senderEmail: Optional[str] = None
    content: str
    messageType: str
    createdAt: datetime = Field(alias='created_at')

    class Config:
        from_attributes = True
        populate_by_name = True

class CaseCreate(BaseModel):
    integrationId: str
    customerEmail: str
    customerName: Optional[str] = None
    subject: str
    description: str
    priority: str = "medium"

class CaseUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assignedTo: Optional[str] = None
    aiResponse: Optional[str] = None
    humanResponse: Optional[str] = None
    aiConfidence: Optional[str] = None

class CaseResponse(BaseModel):
    id: str
    tenantId: str = Field(alias='tenant_id')
    integrationId: str = Field(alias='integration_id')
    customerEmail: str = Field(alias='customer_email')
    customerName: Optional[str] = Field(alias='customer_name')
    subject: str
    description: str
    status: str
    priority: str
    assignedTo: Optional[str] = Field(alias='assigned_to')
    aiResponse: Optional[str] = Field(alias='ai_response')
    humanResponse: Optional[str] = Field(alias='human_response')
    aiConfidence: str = Field(alias='ai_confidence')
    createdAt: datetime = Field(alias='created_at')
    updatedAt: datetime = Field(alias='updated_at')

    class Config:
        from_attributes = True
        populate_by_name = True

class CaseDetailResponse(CaseResponse):
    messages: List[CaseMessageResponse] = []

class ApiKeyListResponse(BaseModel):
    keys: List[ApiKeyResponse]

# Metrics Schemas
class TenantMetricsResponse(BaseModel):
    totalCases: int = 0
    resolvedCases: int = 0
    autopilotRate: float = 0.0
    avgResponseTime: float = 0.0
    createdAt: datetime = None
