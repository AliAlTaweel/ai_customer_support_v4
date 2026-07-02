from fastapi import APIRouter, HTTPException, Depends
from schemas import ApiKeyResponse
from models import Tenant
from auth import get_clerk_user
from logger import logger
import uuid

router = APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])

@router.post("/{tenant_id}", response_model=ApiKeyResponse)
async def generate_api_key(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Generate a new API key for a tenant."""
    try:
        tenant = await Tenant.get(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        api_key = str(uuid.uuid4())
        tenant.api_key = api_key
        await tenant.save()

        logger.info(f"✓ API key generated for tenant {tenant_id}")
        return ApiKeyResponse(key=api_key, createdAt=tenant.created_at)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to generate API key: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}", response_model=ApiKeyResponse)
async def get_api_key(
    tenant_id: str,
    user_data: dict = Depends(get_clerk_user),
):
    """Get tenant's API key."""
    try:
        tenant = await Tenant.get(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        return ApiKeyResponse(key=tenant.api_key, createdAt=tenant.created_at)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to get API key: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
