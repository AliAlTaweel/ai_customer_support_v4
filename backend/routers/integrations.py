from fastapi import APIRouter, HTTPException, Depends
from schemas import IntegrationCreate, IntegrationResponse
from db import db
from auth import get_clerk_user

router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])

@router.post("/{tenant_id}", response_model=IntegrationResponse)
async def create_integration(
    tenant_id: str,
    integration_data: IntegrationCreate,
    auth_user: dict = Depends(get_clerk_user)
):
    """Connect a new integration for a tenant."""
    try:
        tenant = await db.tenant.find_unique(where={"id": tenant_id})
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        # Build integration data
        integration_dict = {
            "tenantId": tenant_id,
            "type": integration_data.type,
            "status": "connected",
        }

        # Add provider-specific fields
        if integration_data.type == "shopify":
            integration_dict["shopifyStoreName"] = integration_data.shopifyStoreName
            integration_dict["shopifyAccessToken"] = integration_data.shopifyAccessToken
        elif integration_data.type == "woocommerce":
            integration_dict["wooCommerceUrl"] = integration_data.wooCommerceUrl
            integration_dict["wooCommerceKey"] = integration_data.wooCommerceKey
            integration_dict["wooCommerceSecret"] = integration_data.wooCommerceSecret
        elif integration_data.type == "stripe":
            integration_dict["stripeApiKey"] = integration_data.stripeApiKey

        integration = await db.integration.create(data=integration_dict)
        return integration
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}", response_model=list[IntegrationResponse])
async def list_integrations(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user)
):
    """List all integrations for a tenant."""
    integrations = await db.integration.find_many(
        where={"tenantId": tenant_id}
    )
    return integrations

@router.get("/{tenant_id}/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    tenant_id: str,
    integration_id: str,
    auth_user: dict = Depends(get_clerk_user)
):
    """Get a specific integration."""
    integration = await db.integration.find_first(
        where={
            "id": integration_id,
            "tenantId": tenant_id
        }
    )
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integration

@router.delete("/{tenant_id}/{integration_id}")
async def delete_integration(
    tenant_id: str,
    integration_id: str,
    auth_user: dict = Depends(get_clerk_user)
):
    """Disconnect an integration."""
    integration = await db.integration.find_first(
        where={
            "id": integration_id,
            "tenantId": tenant_id
        }
    )
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")

    await db.integration.delete(where={"id": integration_id})
    return {"status": "deleted"}

@router.post("/{tenant_id}/{integration_id}/sync")
async def sync_integration(
    tenant_id: str,
    integration_id: str,
    auth_user: dict = Depends(get_clerk_user)
):
    """Manually sync integration data."""
    integration = await db.integration.find_first(
        where={
            "id": integration_id,
            "tenantId": tenant_id
        }
    )
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")

    # For Phase 1, just mark as synced
    # In later phases, this will actually fetch data from Shopify/WooCommerce
    updated = await db.integration.update(
        where={"id": integration_id},
        data={"lastSyncedAt": __import__("datetime").datetime.utcnow()}
    )

    return {"status": "synced", "integration": updated}
