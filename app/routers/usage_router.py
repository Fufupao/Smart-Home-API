# app/routers/usage_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/v1/usage",
    tags=["Usage"]
)

@router.get("/", response_model=List[schemas.DeviceUsage])
def get_usages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取设备使用记录列表"""
    return crud.get_usages(db, skip=skip, limit=limit)

@router.get("/{usage_id}", response_model=schemas.DeviceUsage)
def get_usage(usage_id: int, db: Session = Depends(get_db)):
    """获取某条设备使用记录"""
    usage = crud.get_usage(db, usage_id=usage_id)
    if usage is None:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    return usage

@router.post("/", response_model=schemas.DeviceUsage)
def create_usage(usage: schemas.DeviceUsageCreate, db: Session = Depends(get_db)):
    """创建设备使用记录"""
    return crud.create_usage(db, usage=usage)

@router.put("/{usage_id}", response_model=schemas.DeviceUsage)
def update_usage(usage_id: int, usage: schemas.DeviceUsageCreate, db: Session = Depends(get_db)):
    """更新设备使用记录"""
    db_usage = crud.update_usage(db, usage_id=usage_id, usage=usage)
    if db_usage is None:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    return db_usage

@router.delete("/{usage_id}")
def delete_usage(usage_id: int, db: Session = Depends(get_db)):
    """删除设备使用记录"""
    db_usage = crud.delete_usage(db, usage_id=usage_id)
    if db_usage is None:
        raise HTTPException(status_code=404, detail="使用记录不存在")
    return {"message": "设备使用记录删除成功"}
