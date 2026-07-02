from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime

from db import get_db
from auth import get_clerk_user
from models import Case, CaseMessage, Tenant, Integration, TenantUser
from schemas import CaseCreate, CaseUpdate, CaseResponse, CaseDetailResponse, CaseMessageCreate, CaseMessageResponse
from logger import logger
import uuid

router = APIRouter(prefix="/api/v1/cases", tags=["cases"])


@router.post("/{tenant_id}", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(tenant_id: str, case_data: CaseCreate, db: Session = Depends(get_db), user_data: dict = Depends(get_clerk_user)):
    """Create a new support case for a tenant"""
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        integration = db.query(Integration).filter(Integration.id == case_data.integrationId, Integration.tenant_id == tenant_id).first()
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")

        case = Case(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            integration_id=case_data.integrationId,
            customer_email=case_data.customerEmail,
            customer_name=case_data.customerName,
            subject=case_data.subject,
            description=case_data.description,
            priority=case_data.priority,
            status="open"
        )
        db.add(case)
        db.commit()
        db.refresh(case)

        logger.info(f"Case created: {case.id} for tenant {tenant_id}")
        return case
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tenant_id}", response_model=List[CaseResponse])
async def list_cases(tenant_id: str, status_filter: str = None, db: Session = Depends(get_db), user_data: dict = Depends(get_clerk_user)):
    """List all cases for a tenant"""
    try:
        query = db.query(Case).filter(Case.tenant_id == tenant_id)

        if status_filter:
            query = query.filter(Case.status == status_filter)

        cases = query.order_by(desc(Case.created_at)).all()
        return cases
    except Exception as e:
        logger.error(f"Error listing cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tenant_id}/{case_id}", response_model=CaseDetailResponse)
async def get_case(tenant_id: str, case_id: str, db: Session = Depends(get_db), user_data: dict = Depends(get_clerk_user)):
    """Get a specific case with all messages"""
    try:
        case = db.query(Case).filter(Case.id == case_id, Case.tenant_id == tenant_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        return case
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{tenant_id}/{case_id}", response_model=CaseResponse)
async def update_case(tenant_id: str, case_id: str, case_update: CaseUpdate, db: Session = Depends(get_db), user_data: dict = Depends(get_clerk_user)):
    """Update a case status, priority, or response"""
    try:
        case = db.query(Case).filter(Case.id == case_id, Case.tenant_id == tenant_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        if case_update.status:
            case.status = case_update.status
        if case_update.priority:
            case.priority = case_update.priority
        if case_update.assignedTo:
            case.assigned_to = case_update.assignedTo
        if case_update.aiResponse:
            case.ai_response = case_update.aiResponse
        if case_update.humanResponse:
            case.human_response = case_update.humanResponse
            case.status = "resolved"
        if case_update.aiConfidence:
            case.ai_confidence = case_update.aiConfidence

        case.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(case)

        logger.info(f"Case updated: {case_id}")
        return case
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{tenant_id}/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(tenant_id: str, case_id: str, db: Session = Depends(get_db), user_data: dict = Depends(get_clerk_user)):
    """Delete a case and all its messages"""
    try:
        case = db.query(Case).filter(Case.id == case_id, Case.tenant_id == tenant_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        db.delete(case)
        db.commit()
        logger.info(f"Case deleted: {case_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{tenant_id}/{case_id}/messages", response_model=CaseMessageResponse, status_code=status.HTTP_201_CREATED)
async def add_case_message(tenant_id: str, case_id: str, message: CaseMessageCreate, db: Session = Depends(get_db), user_data: dict = Depends(get_clerk_user)):
    """Add a message to a case (customer, AI agent, or human agent)"""
    try:
        case = db.query(Case).filter(Case.id == case_id, Case.tenant_id == tenant_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        case_message = CaseMessage(
            id=str(uuid.uuid4()),
            case_id=case_id,
            sender=message.senderName or message.senderEmail,
            sender_email=message.senderEmail,
            content=message.content,
            message_type=message.messageType
        )
        db.add(case_message)
        case.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(case_message)

        logger.info(f"Message added to case: {case_id}")
        return case_message
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tenant_id}/{case_id}/messages", response_model=List[CaseMessageResponse])
async def get_case_messages(tenant_id: str, case_id: str, db: Session = Depends(get_db), user_data: dict = Depends(get_clerk_user)):
    """Get all messages for a case"""
    try:
        case = db.query(Case).filter(Case.id == case_id, Case.tenant_id == tenant_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        messages = db.query(CaseMessage).filter(CaseMessage.case_id == case_id).order_by(CaseMessage.created_at).all()
        return messages
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
