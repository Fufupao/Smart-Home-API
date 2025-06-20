from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

# ------------------------
# User CRUD (已完成)
# ------------------------

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# ------------------------
# Device CRUD (已完成)
# ------------------------

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[int] = None):
    query = db.query(models.Device)
    if user_id:
        query = query.filter(models.Device.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, device_id: int, device: schemas.DeviceUpdate):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device:
        for key, value in device.dict(exclude_unset=True).items():
            setattr(db_device, key, value)
        db.commit()
        db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device:
        db.delete(db_device)
        db.commit()
    return db_device

# ------------------------
# DeviceUsage CRUD
# ------------------------

def get_usage(db: Session, usage_id: int):
    return db.query(models.DeviceUsage).filter(models.DeviceUsage.id == usage_id).first()

def get_usages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DeviceUsage).offset(skip).limit(limit).all()

def create_usage(db: Session, usage: schemas.DeviceUsageCreate):
    db_usage = models.DeviceUsage(**usage.dict())
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage

def update_usage(db: Session, usage_id: int, usage: schemas.DeviceUsageCreate):
    db_usage = db.query(models.DeviceUsage).filter(models.DeviceUsage.id == usage_id).first()
    if db_usage:
        for key, value in usage.dict(exclude_unset=True).items():
            setattr(db_usage, key, value)
        db.commit()
        db.refresh(db_usage)
    return db_usage

def delete_usage(db: Session, usage_id: int):
    db_usage = db.query(models.DeviceUsage).filter(models.DeviceUsage.id == usage_id).first()
    if db_usage:
        db.delete(db_usage)
        db.commit()
    return db_usage

# ------------------------
# SecurityEvent CRUD
# ------------------------

def get_event(db: Session, event_id: int):
    return db.query(models.SecurityEvent).filter(models.SecurityEvent.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SecurityEvent).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.SecurityEventCreate):
    db_event = models.SecurityEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event: schemas.SecurityEventCreate):
    db_event = db.query(models.SecurityEvent).filter(models.SecurityEvent.id == event_id).first()
    if db_event:
        for key, value in event.dict(exclude_unset=True).items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.SecurityEvent).filter(models.SecurityEvent.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event

# ------------------------
# UserFeedback CRUD
# ------------------------

def get_feedback(db: Session, feedback_id: int):
    return db.query(models.UserFeedback).filter(models.UserFeedback.id == feedback_id).first()

def get_feedbacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserFeedback).offset(skip).limit(limit).all()

def create_feedback(db: Session, feedback: schemas.UserFeedbackCreate):
    db_feedback = models.UserFeedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_feedback(db: Session, feedback_id: int, feedback: schemas.UserFeedbackCreate):
    db_feedback = db.query(models.UserFeedback).filter(models.UserFeedback.id == feedback_id).first()
    if db_feedback:
        for key, value in feedback.dict(exclude_unset=True).items():
            setattr(db_feedback, key, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_feedback(db: Session, feedback_id: int):
    db_feedback = db.query(models.UserFeedback).filter(models.UserFeedback.id == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
    return db_feedback
