from fastapi import APIRouter, HTTPException, Depends
from schemas import SignupRequest, SignupResponse, TenantUserCreate, TenantUserResponse
from models import Tenant, TenantUser
from auth import get_clerk_user
from logger import logger
import uuid

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/signup", response_model=SignupResponse)
async def signup(signup_data: SignupRequest):
    """Sign up a new user and create tenant."""
    try:
        logger.info(f"📝 New signup: {signup_data.email}")
        
        tenant = Tenant(
            name=signup_data.organizationName,
            support_email=signup_data.email,
            clerk_org_id=str(uuid.uuid4()),
            api_key=str(uuid.uuid4()),
        )
        await tenant.save()

        return SignupResponse(
            userId=str(uuid.uuid4()),
            organizationId=tenant.id,
            organizationName=tenant.name,
            email=signup_data.email,
        )
    except Exception as e:
        logger.error(f"✗ Signup failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tenant-users/{tenant_id}", response_model=TenantUserResponse)
async def add_tenant_user(
    tenant_id: str,
    user_data: TenantUserCreate,
    current_user: dict = Depends(get_clerk_user),
):
    """Create new tenant user."""
    try:
        tenant = await Tenant.get(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        tenant_user = TenantUser(
            tenant_id=tenant_id,
            user_id=user_data.userId,
            role=user_data.role,
        )
        await tenant_user.save()
        logger.info(f"✓ Tenant user added: {tenant_user.id}")
        return tenant_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to add tenant user: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tenant-users/{tenant_id}", response_model=list[TenantUserResponse])
async def list_tenant_users(
    tenant_id: str,
    current_user: dict = Depends(get_clerk_user),
):
    """List tenant users."""
    users = await TenantUser.find(TenantUser.tenant_id == tenant_id).to_list()
    return users

@router.get("/me")
async def get_current_user(user_data: dict = Depends(get_clerk_user)):
    """Get current authenticated user."""
    return {"user": user_data}
