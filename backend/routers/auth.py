from fastapi import APIRouter, HTTPException, Depends, Header
from schemas import SignupRequest, SignupResponse, TenantUserCreate, TenantUserResponse
from db import db
from auth import clerk_client, get_clerk_user
import uuid
import stripe
from config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

stripe.api_key = settings.stripe_secret_key

@router.post("/signup", response_model=SignupResponse)
async def signup(signup_data: SignupRequest):
    """Create new tenant with organization and user."""
    try:
        # Create Clerk organization
        clerk_org = await clerk_client.create_organization(
            name=signup_data.organizationName,
            slug=signup_data.organizationSlug
        )
        clerk_org_id = clerk_org["id"]

        # Create Stripe customer
        stripe_customer = stripe.Customer.create(
            email=signup_data.email,
            name=signup_data.organizationName
        )

        # Create tenant in DB
        tenant = await db.tenant.create(
            data={
                "name": signup_data.organizationName,
                "supportEmail": signup_data.email,
                "clerkOrgId": clerk_org_id,
                "apiKey": str(uuid.uuid4()),
                "status": "trial",
                "plan": "starter",
                "stripeCustomerId": stripe_customer["id"],
            }
        )

        # For Phase 1, we'll skip direct user creation as Clerk handles it
        # In production, you'd sync users from Clerk

        return SignupResponse(
            userId=signup_data.email,  # Placeholder - would use Clerk user ID
            organizationId=clerk_org_id,
            organizationName=signup_data.organizationName,
            email=signup_data.email
        )
    except Exception as e:
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
    auth_user: dict = Depends(get_clerk_user)
):
    """Add a user to a tenant."""
    try:
        tenant = await db.tenant.find_unique(where={"id": tenant_id})
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        tenant_user = await db.tenant_user.create(
            data={
                "tenantId": tenant_id,
                "userId": user_data.userId,
                "role": user_data.role,
            }
        )
        return tenant_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tenant-users/{tenant_id}", response_model=list[TenantUserResponse])
async def list_tenant_users(
    tenant_id: str,
    auth_user: dict = Depends(get_clerk_user)
):
    """List all users in a tenant."""
    users = await db.tenant_user.find_many(
        where={"tenantId": tenant_id}
    )
    return users
