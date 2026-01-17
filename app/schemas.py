from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ============ USER SCHEMAS ============
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ CLIENT SCHEMAS ============
class ClientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    owner_id: int
    created_at: datetime
    last_contact: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============ NOTE SCHEMAS ============
class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    client_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ DETAILED CLIENT WITH NOTES ============
class ClientWithNotes(ClientResponse):
    """Ügyfél az összes jegyzetével (adatlap view-hoz)"""
    notes: List[NoteResponse] = []
    
    class Config:
        from_attributes = True