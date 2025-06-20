from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import analytics

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)

@router.get("/device-usage-frequency")
def device_usage_frequency(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """设备使用频率分析"""
    try:
        chart = analytics.device_usage_frequency(db=db, user_id=user_id)
        return {"chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage-patterns")
def device_usage_time_slot(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """设备使用时间段分析"""
    try:
        chart = analytics.device_usage_time_slot(db=db, user_id=user_id)
        return {"chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/area-impact")
def house_area_device_usage(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """房屋面积与设备使用行为分析"""
    try:
        chart = analytics.house_area_device_usage(db=db, user_id=user_id)
        return {"chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/security-device-correlation")
def security_event_device_correlation(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """安防事件与设备使用关联性分析"""
    try:
        chart = analytics.security_event_device_correlation(db=db, user_id=user_id)
        return {"chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/satisfaction-analysis")
def satisfaction_device_usage(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """用户满意度与设备使用频率的关系分析"""
    try:
        chart = analytics.satisfaction_device_usage(db=db, user_id=user_id)
        return {"chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/energy-consumption-distribution")
def energy_consumption_distribution(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """设备能耗分布分析"""
    try:
        chart = analytics.energy_consumption_distribution(db=db, user_id=user_id)
        return {"chart": chart}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
