# app/routers/device_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/v1/devices",
    tags=["Devices"]
)

@router.get("/", response_model=List[schemas.Device])
def get_devices(skip: int = 0, limit: int = 100, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """获取设备列表（可选按用户过滤）"""
    return crud.get_devices(db, skip=skip, limit=limit, user_id=user_id)

@router.get("/{device_id}", response_model=schemas.Device)
def get_device(device_id: int, db: Session = Depends(get_db)):
    """获取设备详情"""
    device = crud.get_device(db, device_id=device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return device

@router.post("/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """创建设备"""
    return crud.create_device(db, device=device)

@router.put("/{device_id}", response_model=schemas.Device)
def update_device(device_id: int, device: schemas.DeviceUpdate, db: Session = Depends(get_db)):
    """更新设备信息"""
    db_device = crud.update_device(db, device_id=device_id, device=device)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return db_device

@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """删除设备"""
    db_device = crud.delete_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="设备不存在")
    return {"message": "设备删除成功"}




