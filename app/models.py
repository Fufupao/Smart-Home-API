# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# 用户表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    house_area = Column(Float, nullable=True)  # 房屋面积
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    devices = relationship("Device", back_populates="owner")
    feedbacks = relationship("UserFeedback", back_populates="user")


# 设备表
class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    location = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="devices")
    usage_records = relationship("DeviceUsage", back_populates="device")
    security_events = relationship("SecurityEvent", back_populates="device")
    feedbacks = relationship("UserFeedback", back_populates="device")


# 设备使用记录表
class DeviceUsage(Base):
    __tablename__ = "device_usage"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    energy_consumption = Column(Float, nullable=True)

    device = relationship("Device", back_populates="usage_records")


# 安防事件表
class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    event_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    device = relationship("Device", back_populates="security_events")


# 用户反馈表
class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))
    feedback_type = Column(String(100), nullable=False)
    content = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
    device = relationship("Device", back_populates="feedbacks")
