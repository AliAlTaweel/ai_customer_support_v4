from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import TenantCreate, TenantUpdate, TenantResponse, TenantMetricsResponse
from models import Tenant
from db import SessionLocal, get_db
from auth import get_clerk_user
from logger import logger
import uuid

router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])

@router.post("", response_model=TenantResponse)
async def create_tenant(
    tenant_data: TenantCreate,
    user_data: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
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
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        logger.info(f"✓ Tenant created: {tenant.id} ({tenant.name})")
        return tenant
    except Exception as e:
        db.rollback()
        logger.error(f"✗ Failed to create tenant: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Get tenant details."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: str,
    tenant_data: TenantUpdate,
    user_data: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Update tenant configuration."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    update_dict = {k: v for k, v in tenant_data.model_dump().items() if v is not None}

    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        for key, value in update_dict.items():
            setattr(tenant, key, value)
        db.commit()
        db.refresh(tenant)
        return tenant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}/metrics", response_model=TenantMetricsResponse)
async def get_tenant_metrics(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Get tenant metrics (cases, automation rate, etc)."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return TenantMetricsResponse(
        totalCases=0,
        resolvedCases=0,
        autopilotRate=0.0,
        avgResponseTime=0.0
    )

@router.delete("/{tenant_id}")
async def delete_tenant(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Delete a tenant and all associated data."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    try:
        logger.info(f"🗑️ Deleting tenant: {tenant.id} ({tenant.name})")
        db.delete(tenant)
        db.commit()
        logger.info(f"✓ Tenant deleted: {tenant.id}")
        return {"message": "Tenant deleted successfully", "id": tenant_id}
    except Exception as e:
        db.rollback()
        logger.error(f"✗ Failed to delete tenant: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=list[TenantResponse])
async def list_tenants(
    user_data: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """List all tenants for the current user (admin)."""
    tenants = db.query(Tenant).all()
    return tenants
