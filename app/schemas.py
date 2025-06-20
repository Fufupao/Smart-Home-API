# app/schemas.py

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------------
# 用户部分
# -----------------------------

class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    house_area: Optional[float]


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    house_area: Optional[float]


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# 设备部分
# -----------------------------

class DeviceBase(BaseModel):
    name: str
    type: str
    location: Optional[str]
    user_id: int


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    location: Optional[str]
    user_id: Optional[int]


class Device(DeviceBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# 设备使用记录部分
# -----------------------------

class DeviceUsageBase(BaseModel):
    device_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    energy_consumption: Optional[float]


class DeviceUsageCreate(DeviceUsageBase):
    pass


class DeviceUsage(DeviceUsageBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# 安防事件部分
# -----------------------------

class SecurityEventBase(BaseModel):
    device_id: int
    event_type: str
    severity: str
    timestamp: Optional[datetime] = None


class SecurityEventCreate(SecurityEventBase):
    pass


class SecurityEvent(SecurityEventBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# 用户反馈部分
# -----------------------------

class UserFeedbackBase(BaseModel):
    user_id: int
    device_id: int
    feedback_type: str
    content: Optional[str]
    rating: Optional[int]
    created_at: Optional[datetime] = None


class UserFeedbackCreate(UserFeedbackBase):
    pass


class UserFeedback(UserFeedbackBase):
    id: int

    class Config:
        from_attributes = True
