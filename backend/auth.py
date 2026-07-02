import jwt
import httpx
from fastapi import HTTPException, Depends, Header
from typing import Optional
from config import settings

async def verify_clerk_token(authorization: Optional[str] = Header(None)) -> dict:
    """Verify Clerk JWT token from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    try:
        token = authorization.replace("Bearer ", "")
        # Note: In production, you'd verify the JWT properly with Clerk's JWKS
        # For now, we decode without verification for local testing
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

async def get_clerk_user(authorization: Optional[str] = Header(None)) -> dict:
    """Extract Clerk user from JWT token. Optional for local testing."""
    if not authorization:
        # Return dummy user for testing if no token provided
        return {"sub": "test_user", "email": "test@example.com"}

    try:
        token_data = await verify_clerk_token(authorization)
        return token_data
    except:
        # Return dummy user on auth error for testing
        return {"sub": "test_user", "email": "test@example.com"}

class ClerkClient:
    """Clerk API client for managing organizations and users."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.clerk.com/v1"
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"})

    async def create_organization(self, name: str, slug: str) -> dict:
        """Create a new organization in Clerk."""
        response = await self.client.post(
            f"{self.base_url}/organizations",
            json={"name": name, "slug": slug}
        )
        return response.json()

    async def get_organization(self, org_id: str) -> dict:
        """Get organization details."""
        response = await self.client.get(f"{self.base_url}/organizations/{org_id}")
        return response.json()

    async def update_organization(self, org_id: str, **kwargs) -> dict:
        """Update organization."""
        response = await self.client.patch(
            f"{self.base_url}/organizations/{org_id}",
            json=kwargs
        )
        return response.json()

    async def add_organization_member(self, org_id: str, user_id: str, role: str = "member") -> dict:
        """Add a user to an organization."""
        response = await self.client.post(
            f"{self.base_url}/organizations/{org_id}/memberships",
            json={"user_id": user_id, "role": role}
        )
        return response.json()

clerk_client = ClerkClient(settings.clerk_secret_key)
