from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import IntegrationCreate, IntegrationResponse
from models import Tenant, Integration
from db import get_db
from auth import get_clerk_user
from datetime import datetime

router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])

@router.post("/{tenant_id}", response_model=IntegrationResponse)
async def create_integration(
    tenant_id: str,
    integration_data: IntegrationCreate,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Connect a new integration for a tenant."""
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        integration = Integration(
            tenant_id=tenant_id,
            type=integration_data.type,
            status="connected",
            shopify_store_name=integration_data.shopifyStoreName,
            shopify_access_token=integration_data.shopifyAccessToken,
            woocommerce_url=integration_data.wooCommerceUrl,
            woocommerce_key=integration_data.wooCommerceKey,
            woocommerce_secret=integration_data.wooCommerceSecret,
            stripe_api_key=integration_data.stripeApiKey,
        )
        db.add(integration)
        db.commit()
        db.refresh(integration)
        return integration
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}", response_model=list[IntegrationResponse])
async def list_integrations(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """List all integrations for a tenant."""
    integrations = db.query(Integration).filter(Integration.tenant_id == tenant_id).all()
    return integrations

@router.get("/{tenant_id}/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    tenant_id: str,
    integration_id: str,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Get a specific integration."""
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.tenant_id == tenant_id
    ).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integration

@router.delete("/{tenant_id}/{integration_id}")
async def delete_integration(
    tenant_id: str,
    integration_id: str,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Disconnect an integration."""
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.tenant_id == tenant_id
    ).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")

    db.delete(integration)
    db.commit()
    return {"status": "deleted"}

@router.post("/{tenant_id}/{integration_id}/sync")
async def sync_integration(
    tenant_id: str,
    integration_id: str,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Manually sync integration data."""
    integration = db.query(Integration).filter(
        Integration.id == integration_id,
        Integration.tenant_id == tenant_id
    ).first()
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")

    # Mark as synced
    integration.last_synced_at = datetime.utcnow()
    db.commit()
    db.refresh(integration)

    return {"status": "synced", "integration": integration}
