from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from schemas import CaseCreate, CaseUpdate, CaseResponse, CaseDetailResponse, CaseMessageCreate, CaseMessageResponse
from models import Case, CaseMessage, Tenant, Integration
from auth import get_clerk_user
from logger import logger
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1/cases", tags=["cases"])

@router.post("/{tenant_id}", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(tenant_id: str, case_data: CaseCreate, user_data: dict = Depends(get_clerk_user)):
    """Create a new support case for a tenant"""
    try:
        tenant = await Tenant.get(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        integration = await Integration.get(case_data.integrationId)
        if not integration or integration.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Integration not found")

        case = Case(
            tenant_id=tenant_id,
            integration_id=case_data.integrationId,
            customer_email=case_data.customerEmail,
            customer_name=case_data.customerName,
            subject=case_data.subject,
            description=case_data.description,
            priority=case_data.priority,
            status="open"
        )
        await case.save()
        logger.info(f"Case created: {case.id} for tenant {tenant_id}")
        return case
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tenant_id}", response_model=list[CaseResponse])
async def list_cases(tenant_id: str, status_filter: str = None, user_data: dict = Depends(get_clerk_user)):
    """List all cases for a tenant"""
    try:
        query = Case.find(Case.tenant_id == tenant_id)
        if status_filter:
            query = Case.find(Case.tenant_id == tenant_id, Case.status == status_filter)
        cases = await query.to_list()
        return cases
    except Exception as e:
        logger.error(f"Error listing cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tenant_id}/{case_id}", response_model=CaseDetailResponse)
async def get_case(tenant_id: str, case_id: str, user_data: dict = Depends(get_clerk_user)):
    """Get a specific case with all messages"""
    try:
        case = await Case.get(case_id)
        if not case or case.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Case not found")
        return case
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{tenant_id}/{case_id}", response_model=CaseResponse)
async def update_case(tenant_id: str, case_id: str, case_update: CaseUpdate, user_data: dict = Depends(get_clerk_user)):
    """Update a case status, priority, or response"""
    try:
        case = await Case.get(case_id)
        if not case or case.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Case not found")

        update_data = case_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "assignedTo":
                case.assigned_to = value
            elif field == "aiResponse":
                case.ai_response = value
            elif field == "humanResponse":
                case.human_response = value
                case.status = "resolved"
            elif field == "aiConfidence":
                case.ai_confidence = value
            else:
                setattr(case, field, value)

        case.updated_at = datetime.utcnow()
        await case.save()
        logger.info(f"Case updated: {case_id}")
        return case
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{tenant_id}/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(tenant_id: str, case_id: str, user_data: dict = Depends(get_clerk_user)):
    """Delete a case and all its messages"""
    try:
        case = await Case.get(case_id)
        if not case or case.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Case not found")

        await case.delete()
        logger.info(f"Case deleted: {case_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{tenant_id}/{case_id}/messages", response_model=CaseMessageResponse, status_code=status.HTTP_201_CREATED)
async def add_case_message(tenant_id: str, case_id: str, message: CaseMessageCreate, user_data: dict = Depends(get_clerk_user)):
    """Add a message to a case"""
    try:
        case = await Case.get(case_id)
        if not case or case.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Case not found")

        case_message = CaseMessage(
            case_id=case_id,
            sender=message.senderName or message.senderEmail,
            sender_email=message.senderEmail,
            content=message.content,
            message_type=message.messageType
        )
        await case_message.save()
        case.updated_at = datetime.utcnow()
        await case.save()

        logger.info(f"Message added to case: {case_id}")
        return case_message
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tenant_id}/{case_id}/messages", response_model=list[CaseMessageResponse])
async def get_case_messages(tenant_id: str, case_id: str, user_data: dict = Depends(get_clerk_user)):
    """Get all messages for a case"""
    try:
        case = await Case.get(case_id)
        if not case or case.tenant_id != tenant_id:
            raise HTTPException(status_code=404, detail="Case not found")

        messages = await CaseMessage.find(CaseMessage.case_id == case_id).to_list()
        return messages
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
