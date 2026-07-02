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

class ApiKeyListResponse(BaseModel):
    keys: List[ApiKeyResponse]

# Metrics Schemas
class TenantMetricsResponse(BaseModel):
    totalCases: int = 0
    resolvedCases: int = 0
    autopilotRate: float = 0.0
    avgResponseTime: float = 0.0
    createdAt: datetime = None
