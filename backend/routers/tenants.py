from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from schemas import TenantCreate, TenantUpdate, TenantResponse, TenantMetricsResponse
from db import db
from auth import get_clerk_user
import uuid

router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])

@router.post("", response_model=TenantResponse)
async def create_tenant(
    tenant_data: TenantCreate,
    user_data: dict = Depends(get_clerk_user)
):
    """Create a new tenant (admin only)."""
    try:
        tenant = await db.tenant.create(
            data={
                "name": tenant_data.name,
                "supportEmail": tenant_data.supportEmail,
                "tone": tenant_data.tone,
                "systemPrompt": tenant_data.systemPrompt or "You are a helpful customer support AI agent.",
                "logo": tenant_data.logo,
                "colors": tenant_data.colors,
                "clerkOrgId": str(uuid.uuid4()),
                "apiKey": str(uuid.uuid4()),
                "status": "trial",
                "plan": "starter",
            }
        )
        return tenant
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user)
):
    """Get tenant details."""
    tenant = await db.tenant.find_unique(where={"id": tenant_id})
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str,
    tenant_data: TenantUpdate,
    user_data: dict = Depends(get_clerk_user)
):
    """Update tenant configuration."""
    update_dict = {k: v for k, v in tenant_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        tenant = await db.tenant.update(
            where={"id": tenant_id},
            data=update_dict
        )
        return tenant
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}/metrics", response_model=TenantMetricsResponse)
async def get_tenant_metrics(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user)
):
    """Get tenant metrics (cases, automation rate, etc)."""
    tenant = await db.tenant.find_unique(where={"id": tenant_id})
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # For Phase 1, return placeholder metrics
    return TenantMetricsResponse(
        totalCases=0,
        resolvedCases=0,
        autopilotRate=0.0,
        avgResponseTime=0.0
    )

@router.get("", response_model=list[TenantResponse])
async def list_tenants(
    user_data: dict = Depends(get_clerk_user)
):
    """List all tenants for the current user (admin)."""
    tenants = await db.tenant.find_many()
    return tenants
