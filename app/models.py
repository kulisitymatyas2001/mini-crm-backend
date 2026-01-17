from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    """Szakember (coach/edző/terapeuta) aki használja a CRM-et"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Kapcsolat: egy szakembernek sok ügyfele van
    clients = relationship("Client", back_populates="owner", cascade="all, delete-orphan")


class Client(Base):
    """Ügyfél adatai"""
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Alapadatok
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # Tracking mezők
    created_at = Column(DateTime, default=datetime.utcnow)
    last_contact = Column(DateTime, nullable=True)  # Ez automatikusan frissül jegyzet hozzáadásakor
    
    # Kapcsolatok
    owner = relationship("User", back_populates="clients")
    notes = relationship("Note", back_populates="client", cascade="all, delete-orphan")


class Note(Base):
    """Jegyzetek egy ügyféllel kapcsolatban"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Kapcsolat
    client = relationship("Client", back_populates="notes")