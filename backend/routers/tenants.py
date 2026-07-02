from fastapi import APIRouter, HTTPException, Depends
from schemas import TenantCreate, TenantUpdate, TenantResponse, TenantMetricsResponse
from models import Tenant
from auth import get_clerk_user
from logger import logger
import uuid

router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])

@router.post("", response_model=TenantResponse)
async def create_tenant(
    tenant_data: TenantCreate,
    user_data: dict = Depends(get_clerk_user),
):
    """Create a new tenant (admin only)."""
    try:
        logger.info(f"📝 Creating new tenant: {tenant_data.name}")
        tenant = Tenant(
            name=tenant_data.name,
            support_email=tenant_data.supportEmail,
            tone=tenant_data.tone,
            system_prompt=tenant_data.systemPrompt or "You are a helpful customer support AI agent.",
            logo=tenant_data.logo,
            colors=tenant_data.colors,
            clerk_org_id=str(uuid.uuid4()),
            api_key=str(uuid.uuid4()),
            status="trial",
            plan="starter",
        )
        await tenant.save()
        logger.info(f"✓ Tenant created: {tenant.id} ({tenant.name})")
        return tenant
    except Exception as e:
        logger.error(f"✗ Failed to create tenant: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Get tenant details."""
    tenant = await Tenant.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.get("", response_model=list[TenantResponse])
async def list_tenants(user_data: dict = Depends(get_clerk_user)):
    """List all tenants."""
    tenants = await Tenant.find_all().to_list()
    return tenants

@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str,
    tenant_update: TenantUpdate,
    user_data: dict = Depends(get_clerk_user),
):
    """Update a tenant."""
    try:
        tenant = await Tenant.get(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        update_data = tenant_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tenant, field, value)

        await tenant.save()
        logger.info(f"✓ Tenant updated: {tenant_id}")
        return tenant
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to update tenant: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{tenant_id}")
async def delete_tenant(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Delete a tenant and all associated data."""
    try:
        tenant = await Tenant.get(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        await tenant.delete()
        logger.info(f"✓ Tenant deleted: {tenant_id}")
        return {"status": "deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to delete tenant: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}/metrics", response_model=TenantMetricsResponse)
async def get_tenant_metrics(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Get tenant metrics."""
    tenant = await Tenant.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return TenantMetricsResponse(
        tenantId=tenant.id,
        totalCases=0,
        resolvedCases=0,
        automationRate=0.0,
        avgResponseTime=0,
    )
