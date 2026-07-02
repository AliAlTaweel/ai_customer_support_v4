from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import ApiKeyResponse
from models import Tenant
from db import get_db
from auth import get_clerk_user
import uuid

router = APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])

@router.post("/{tenant_id}", response_model=ApiKeyResponse)
async def generate_api_key(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Generate a new API key for a tenant."""
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        # Generate new API key
        new_key = str(uuid.uuid4())
        tenant.api_key = new_key
        db.commit()
        db.refresh(tenant)

        return ApiKeyResponse(
            key=new_key,
            createdAt=tenant.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tenant_id}")
async def get_api_key(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Get current API key (masked)."""
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        # Return masked key (only show last 4 chars)
        masked_key = f"sk_{'*' * (len(tenant.api_key) - 4)}{tenant.api_key[-4:]}"

        return {
            "key": masked_key,
            "createdAt": tenant.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
