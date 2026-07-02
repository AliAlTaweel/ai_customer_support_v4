from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from schemas import IntegrationCreate, IntegrationResponse
from models import Tenant, Integration
from auth import get_clerk_user
from logger import logger
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])

@router.post("/{tenant_id}", response_model=IntegrationResponse, status_code=status.HTTP_201_CREATED)
async def create_integration(
    tenant_id: str,
    integration_data: IntegrationCreate,
    user_data: dict = Depends(get_clerk_user),
):
    """Connect a new integration for a tenant."""
    try:
        tenant = await Tenant.get(tenant_id)
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
        await integration.save()
        logger.info(f"✓ Integration created: {integration.id} for tenant {tenant_id}")
        return integration
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to create integration: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}", response_model=list[IntegrationResponse])
async def list_integrations(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """List all integrations for a tenant."""
    integrations = await Integration.find(Integration.tenant_id == tenant_id).to_list()
    return integrations

@router.get("/{tenant_id}/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    tenant_id: str,
    integration_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Get a specific integration."""
    integration = await Integration.get(integration_id)
    if not integration or integration.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integration

@router.delete("/{tenant_id}/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_integration(
    tenant_id: str,
    integration_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Delete an integration."""
    try:
        integration = await Integration.get(integration_id)
        if not integration or integration.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Integration not found")

        await integration.delete()
        logger.info(f"✓ Integration deleted: {integration_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to delete integration: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{tenant_id}/{integration_id}/sync", response_model=IntegrationResponse)
async def sync_integration(
    tenant_id: str,
    integration_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Sync integration data."""
    try:
        integration = await Integration.get(integration_id)
        if not integration or integration.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Integration not found")

        integration.last_synced_at = datetime.utcnow()
        await integration.save()
        logger.info(f"✓ Integration synced: {integration_id}")
        return integration
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to sync integration: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
