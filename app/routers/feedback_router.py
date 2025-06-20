# app/routers/feedback_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/v1/feedback",
    tags=["Feedback"]
)

@router.get("/", response_model=List[schemas.UserFeedback])
def get_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户反馈列表"""
    return crud.get_feedbacks(db, skip=skip, limit=limit)

@router.get("/{feedback_id}", response_model=schemas.UserFeedback)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """获取某条反馈"""
    feedback = crud.get_feedback(db, feedback_id=feedback_id)
    if feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return feedback

@router.post("/", response_model=schemas.UserFeedback)
def create_feedback(feedback: schemas.UserFeedbackCreate, db: Session = Depends(get_db)):
    """创建反馈"""
    return crud.create_feedback(db, feedback=feedback)

@router.put("/{feedback_id}", response_model=schemas.UserFeedback)
def update_feedback(feedback_id: int, feedback: schemas.UserFeedbackCreate, db: Session = Depends(get_db)):
    """更新反馈"""
    db_feedback = crud.update_feedback(db, feedback_id=feedback_id, feedback=feedback)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return db_feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """删除反馈"""
    db_feedback = crud.delete_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return {"message": "反馈删除成功"}
