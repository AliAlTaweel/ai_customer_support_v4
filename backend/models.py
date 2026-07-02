from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    clerk_org_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    colors = Column(JSON, nullable=True)
    system_prompt = Column(Text, default="You are a helpful customer support AI agent. Be professional and concise.")
    tone = Column(String, default="professional")
    support_email = Column(String, nullable=False)
    webhook_url = Column(String, nullable=True)
    api_key = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="trial")
    plan = Column(String, default="starter")
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    users = relationship("TenantUser", back_populates="tenant", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="tenant", cascade="all, delete-orphan")


class TenantUser(Base):
    __tablename__ = "tenant_users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, nullable=False)
    role = Column(String, default="agent")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    tenant = relationship("Tenant", back_populates="users")

    __table_args__ = (UniqueConstraint('tenant_id', 'user_id', name='uq_tenant_user'),)


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="disconnected")
    shopify_store_name = Column(String, nullable=True)
    shopify_access_token = Column(Text, nullable=True)
    woocommerce_url = Column(String, nullable=True)
    woocommerce_key = Column(Text, nullable=True)
    woocommerce_secret = Column(Text, nullable=True)
    stripe_api_key = Column(Text, nullable=True)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    tenant = relationship("Tenant", back_populates="integrations")
    cases = relationship("Case", back_populates="integration", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('tenant_id', 'type', name='uq_tenant_integration_type'),)


class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    integration_id = Column(String, ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False)
    customer_email = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="open")
    priority = Column(String, default="medium")
    assigned_to = Column(String, ForeignKey("tenant_users.id"), nullable=True)
    ai_response = Column(Text, nullable=True)
    human_response = Column(Text, nullable=True)
    ai_confidence = Column(String, default="medium")
    external_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    tenant = relationship("Tenant", foreign_keys=[tenant_id])
    integration = relationship("Integration", back_populates="cases")
    assigned_agent = relationship("TenantUser")
    messages = relationship("CaseMessage", back_populates="case", cascade="all, delete-orphan")


class CaseMessage(Base):
    __tablename__ = "case_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String, nullable=False)
    sender_email = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    message_type = Column(String, default="message")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    case = relationship("Case", back_populates="messages")
