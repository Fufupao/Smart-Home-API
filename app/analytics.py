# app/analytics.py

import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy.orm import Session
from app import models
from typing import List, Optional
from datetime import datetime
from sqlalchemy import func, text

# 设置 Matplotlib 使用中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ------------------------------
# 工具函数：生成Base64图像
# ------------------------------
def fig_to_base64(fig):
    """将图表转换为base64编码"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    return img_str


# ------------------------------
# 设备使用频率分析
# ------------------------------
def device_usage_frequency(db: Session, user_id: Optional[str] = None) -> str:
    """生成设备使用频率柱状图并返回Base64"""
    query = db.query(
        models.DeviceUsage.device_id,
        models.Device.name,
        func.count(models.DeviceUsage.id).label('usage_count')
    ).join(models.Device, models.Device.id == models.DeviceUsage.device_id)

    if user_id:
        query = query.filter(models.Device.user_id == user_id)

    usage_data = query.group_by(models.DeviceUsage.device_id, models.Device.name)\
                      .order_by(text("usage_count DESC")).all()

    df = pd.DataFrame(usage_data, columns=["device_id", "device_name", "usage_count"])
    
    # 创建柱状图
    plt.figure(figsize=(10, 6))
    sns.barplot(x="usage_count", y="device_name", data=df, palette="Blues_d")
    plt.title("Device Usage Frequency")
    plt.xlabel("Usage Count")
    plt.ylabel("Device Name")
    
    # 转换为Base64并返回
    return fig_to_base64(plt)


# ------------------------------
# 设备使用时间段分析
# ------------------------------
def device_usage_time_slot(db: Session, user_id: Optional[str] = None) -> str:
    """生成设备使用时间段分析的线形图并返回Base64"""
    query = db.query(
        models.DeviceUsage.device_id,
        models.Device.name,
        func.extract('hour', models.DeviceUsage.start_time).label('hour')
    ).join(models.Device, models.Device.id == models.DeviceUsage.device_id)

    if user_id:
        query = query.filter(models.Device.user_id == user_id)

    usage_data = query.all()

    df = pd.DataFrame(usage_data, columns=["device_id", "device_name", "hour"])
    
    # 创建设备使用时间段的线形图
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="hour", y="device_id", data=df, hue="device_name", marker="o")
    plt.title("Device Usage by Hour of the Day")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Device ID")
    
    # 转换为Base64并返回
    return fig_to_base64(plt)

# ------------------------------
# 用户使用习惯挖掘（设备组合使用模式）
# ------------------------------
def device_usage_patterns(user_id: Optional[int], db: Session) -> str:
    """分析用户使用习惯，找出哪些设备经常同时使用"""
    # 获取设备使用记录
    query = db.query(
        models.DeviceUsage.device_id,
        models.Device.name,
        func.date_trunc('hour', models.DeviceUsage.start_time).label("time_slot")
    ).join(models.Device, models.Device.id == models.DeviceUsage.device_id)

    if user_id is not None:
        query = query.join(models.User, models.User.id == models.Device.user_id).filter(models.User.id == user_id)

    usage_data = query.all()

    df = pd.DataFrame(usage_data, columns=["device_id", "device_name", "time_slot"])

    if df.empty:
        raise ValueError("无足够的使用记录进行模式分析")

    # 生成共现矩阵
    pivot_df = df.pivot_table(index="time_slot", columns="device_name", aggfunc="size", fill_value=0)
    correlation_matrix = pivot_df.T.dot(pivot_df)
    
    # 归一化（可选，使热力图更明显）
    normalized = correlation_matrix.div(correlation_matrix.sum(axis=1), axis=0)

    # 可视化
    plt.figure(figsize=(10, 8))
    sns.heatmap(normalized, annot=True, cmap="Blues", fmt=".2f", cbar_kws={"label": "Co-Usage Frequency"})
    plt.title("Device Co-Usage Pattern")

    return fig_to_base64(plt)


# ------------------------------
# 房屋面积对设备使用行为的影响
# ------------------------------
def house_area_device_usage(db: Session, user_id: Optional[str] = None) -> str:
    """生成房屋面积与设备使用行为的散点图并返回Base64"""
    query = db.query(
        models.User.house_area,
        models.Device.name,
        func.count(models.DeviceUsage.id).label('usage_count')
    ).join(models.Device, models.Device.user_id == models.User.id)\
     .join(models.DeviceUsage, models.DeviceUsage.device_id == models.Device.id)

    if user_id:
        query = query.filter(models.User.id == user_id)

    usage_data = query.group_by(models.User.house_area, models.Device.name).all()

    df = pd.DataFrame(usage_data, columns=["house_area", "device_name", "usage_count"])
    
    # 创建散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="house_area", y="usage_count", hue="device_name", data=df, s=100)
    plt.title("House Area vs Device Usage Behavior")
    plt.xlabel("House Area (sq meters)")
    plt.ylabel("Usage Count")
    
    # 转换为Base64并返回
    return fig_to_base64(plt)


# ------------------------------
# 安防事件与设备使用的关联性分析
# ------------------------------
def security_event_device_correlation(db: Session, user_id: Optional[str] = None) -> str:
    """生成安防事件与设备使用关联性的热力图并返回Base64"""
    query = db.query(
        models.Device.name,
        models.SecurityEvent.event_type,
        func.count(models.DeviceUsage.id).label('usage_count')
    ).join(models.Device, models.Device.id == models.DeviceUsage.device_id)\
     .join(models.SecurityEvent, models.SecurityEvent.device_id == models.Device.id)

    if user_id:
        query = query.filter(models.Device.user_id == user_id)

    usage_data = query.group_by(models.Device.name, models.SecurityEvent.event_type).all()

    df = pd.DataFrame(usage_data, columns=["device_name", "event_type", "usage_count"])
    df_pivot = df.pivot_table(index="device_name", columns="event_type", values="usage_count", aggfunc="sum", fill_value=0)
    
    # 创建热力图
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_pivot, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Usage Count'})
    plt.title("Security Event vs Device Usage Correlation")
    
    # 转换为Base64并返回
    return fig_to_base64(plt)


# ------------------------------
# 用户满意度与设备使用频率的关系
# ------------------------------
def satisfaction_device_usage(db: Session, user_id: Optional[str] = None) -> str:
    """生成用户满意度与设备使用频率关系的散点图并返回Base64"""
    query = db.query(
        models.UserFeedback.device_id,
        models.Device.name,
        models.UserFeedback.rating,
        func.count(models.DeviceUsage.id).label('usage_count')
    ).join(models.Device, models.Device.id == models.UserFeedback.device_id)\
     .join(models.DeviceUsage, models.DeviceUsage.device_id == models.Device.id)

    if user_id:
        query = query.filter(models.Device.user_id == user_id)

    feedback_data = query.group_by(
        models.UserFeedback.device_id,
        models.Device.name,
        models.UserFeedback.rating
    ).all()

    df = pd.DataFrame(feedback_data, columns=["device_id", "device_name", "rating", "usage_count"])
    
    # 创建散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="usage_count", y="rating", hue="device_name", data=df, s=100)
    plt.title("Satisfaction vs Device Usage Frequency")
    plt.xlabel("Usage Count")
    plt.ylabel("Satisfaction Rating")
    
    # 转换为Base64并返回
    return fig_to_base64(plt)


# ------------------------------
# 设备能耗分布饼图
# ------------------------------
def energy_consumption_distribution(db: Session, user_id: Optional[str] = None) -> str:
    """生成设备能耗分布的饼图并返回Base64"""
    query = db.query(
        models.Device.name,
        func.sum(models.DeviceUsage.energy_consumption).label('total_energy')
    ).join(models.DeviceUsage, models.Device.id == models.DeviceUsage.device_id)

    if user_id:
        query = query.filter(models.Device.user_id == user_id)

    energy_data = query.group_by(models.Device.name).all()

    df = pd.DataFrame(energy_data, columns=["device_name", "total_energy"])

    # 创建饼图
    plt.figure(figsize=(8, 8))
    plt.pie(df['total_energy'], labels=df['device_name'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set3", len(df)))
    plt.title("Energy Consumption Distribution by Device")
    
    # 转换为Base64并返回
    return fig_to_base64(plt)