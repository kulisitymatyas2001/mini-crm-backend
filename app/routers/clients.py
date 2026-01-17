from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.schemas import ClientCreate, ClientUpdate, ClientResponse, ClientWithNotes, NoteCreate, NoteResponse
from app.models import Client, Note, User
from app.auth_utils import get_current_user

router = APIRouter()

# ============ CLIENT ENDPOINTS ============

@router.get("/", response_model=List[ClientResponse])
def get_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Összes ügyfél listázása (csak a bejelentkezett user ügyfelei)"""
    clients = db.query(Client).filter(Client.owner_id == current_user.id).all()
    return clients


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Új ügyfél létrehozása"""
    new_client = Client(
        **client.dict(),
        owner_id=current_user.id
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.get("/{client_id}", response_model=ClientWithNotes)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Egy ügyfél részletes adatai a jegyzeteivel együtt"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ügyfél adatainak módosítása"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Csak a megadott mezőket frissítjük
    update_data = client_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ügyfél törlése"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return None


# ============ NOTE ENDPOINTS ============

@router.post("/{client_id}/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def add_note(
    client_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Jegyzet hozzáadása egy ügyfélhez - AUTOMATIKUSAN frissíti a last_contact-ot!"""
    # Ellenőrizzük, hogy a client a user-é
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Új jegyzet létrehozása
    new_note = Note(
        **note.dict(),
        client_id=client_id
    )
    db.add(new_note)
    
    # FONTOS: Automatikusan frissítjük az ügyfél utolsó kapcsolat dátumát
    client.last_contact = datetime.utcnow()
    
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/{client_id}/notes", response_model=List[NoteResponse])
def get_notes(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Egy ügyfél összes jegyzetének lekérése"""
    # Ellenőrizzük, hogy a client a user-é
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    notes = db.query(Note).filter(Note.client_id == client_id).order_by(Note.created_at.desc()).all()
    return notes


@router.delete("/{client_id}/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    client_id: int,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Jegyzet törlése"""
    # Ellenőrizzük, hogy a client a user-é
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Jegyzet törlése
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.client_id == client_id
    ).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return None