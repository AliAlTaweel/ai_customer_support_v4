from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import SignupRequest, SignupResponse, TenantUserCreate, TenantUserResponse
from models import Tenant, TenantUser
from db import get_db
from auth import clerk_client, get_clerk_user
from logger import logger
import uuid
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/signup", response_model=SignupResponse)
async def signup(signup_data: SignupRequest, db: Session = Depends(get_db)):
    """Create new tenant with organization and user."""
    try:
        logger.info(f"🔐 Signup attempt: {signup_data.email} ({signup_data.organizationName})")

        # Create tenant in DB (Stripe integration added later)
        tenant = Tenant(
            name=signup_data.organizationName,
            support_email=signup_data.email,
            clerk_org_id=str(uuid.uuid4()),
            api_key=str(uuid.uuid4()),
            status="trial",
            plan="starter",
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

        logger.info(f"✓ Signup successful: {signup_data.email} (ID: {tenant.id})")

        return SignupResponse(
            userId=signup_data.email,
            organizationId=tenant.clerk_org_id,
            organizationName=signup_data.organizationName,
            email=signup_data.email
        )
    except Exception as e:
        db.rollback()
        logger.error(f"✗ Signup failed: {signup_data.email} - {str(e)}")
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)}")

@router.post("/login")
async def login(email: str, password: str):
    """Login (Clerk handles this on frontend, this is a placeholder)."""
    return {"message": "Use Clerk authentication on frontend"}

@router.get("/me")
async def get_current_user(user_data: dict = Depends(get_clerk_user)):
    """Get current authenticated user."""
    return user_data

@router.post("/tenant-users/{tenant_id}", response_model=TenantUserResponse)
async def add_tenant_user(
    tenant_id: str,
    user_data: TenantUserCreate,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """Add a user to a tenant."""
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        tenant_user = TenantUser(
            tenant_id=tenant_id,
            user_id=user_data.userId,
            role=user_data.role,
        )
        db.add(tenant_user)
        db.commit()
        db.refresh(tenant_user)
        return tenant_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tenant-users/{tenant_id}", response_model=list[TenantUserResponse])
async def list_tenant_users(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user),
    db: Session = Depends(get_db)
):
    """List all users in a tenant."""
    users = db.query(TenantUser).filter(TenantUser.tenant_id == tenant_id).all()
    return users
