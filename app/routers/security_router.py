# app/routers/security_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/v1/security",
    tags=["Security"]
)

@router.get("/", response_model=List[schemas.SecurityEvent])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取安防事件列表"""
    return crud.get_events(db, skip=skip, limit=limit)

@router.get("/{event_id}", response_model=schemas.SecurityEvent)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """获取某条安防事件"""
    event = crud.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="事件不存在")
    return event

@router.post("/", response_model=schemas.SecurityEvent)
def create_event(event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    """创建安防事件"""
    return crud.create_event(db, event=event)

@router.put("/{event_id}", response_model=schemas.SecurityEvent)
def update_event(event_id: int, event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    """更新安防事件"""
    db_event = crud.update_event(db, event_id=event_id, event=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="事件不存在")
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """删除安防事件"""
    db_event = crud.delete_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="事件不存在")
    return {"message": "安防事件删除成功"}
