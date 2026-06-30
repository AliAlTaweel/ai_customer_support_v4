from fastapi import APIRouter, HTTPException, Depends
from schemas import ApiKeyResponse
from db import db
from auth import get_clerk_user
import uuid

router = APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])

@router.post("/{tenant_id}", response_model=ApiKeyResponse)
async def generate_api_key(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user)
):
    """Generate a new API key for a tenant."""
    try:
        tenant = await db.tenant.find_unique(where={"id": tenant_id})
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        # Generate new API key
        new_key = str(uuid.uuid4())

        # Update tenant with new key
        updated_tenant = await db.tenant.update(
            where={"id": tenant_id},
            data={"apiKey": new_key}
        )

        return ApiKeyResponse(
            key=new_key,
            createdAt=updated_tenant.createdAt
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}")
async def get_api_key(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user)
):
    """Get current API key (masked)."""
    try:
        tenant = await db.tenant.find_unique(where={"id": tenant_id})
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        # Return masked key (only show last 4 chars)
        masked_key = f"sk_{'*' * (len(tenant.apiKey) - 4)}{tenant.apiKey[-4:]}"

        return {
            "key": masked_key,
            "createdAt": tenant.createdAt
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
