# generate_test_data.py
"""
智能家居测试数据生成器
放在smart_home/目录下运行
"""
import random
import datetime
from datetime import timedelta
import sys
import os

# 添加app目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal, engine
from app.models import Base, User, Device, DeviceUsage, SecurityEvent, UserFeedback

# 确保所有表都已创建
Base.metadata.create_all(bind=engine)

# 测试数据配置
USERS_COUNT = 10
DEVICES_PER_USER = (3, 5)  # 每个用户3-5个设备
DATA_DAYS = 90  # 生成90天的数据

# 基础数据
CHINESE_NAMES = [
    "张伟", "李娜", "王磊", "刘敏", "陈杰", 
    "杨丽", "赵强", "孙婷", "周华", "吴刚"
]

DEVICE_TYPES = {
    "智能灯": {
        "names": ["客厅吊灯", "卧室台灯", "厨房射灯", "走廊感应灯", "阳台装饰灯"],
        "locations": ["客厅", "卧室", "厨房", "走廊", "阳台"],
        "power": (5, 60),  # 5-60瓦
        "usage_pattern": "evening_night"  # 傍晚和夜间使用多
    },
    "空调": {
        "names": ["客厅空调", "主卧空调", "次卧空调", "书房空调"],
        "locations": ["客厅", "主卧", "次卧", "书房"],
        "power": (800, 2000),  # 800-2000瓦
        "usage_pattern": "seasonal"  # 季节性使用
    },
    "摄像头": {
        "names": ["门口摄像头", "客厅摄像头", "阳台摄像头", "车库摄像头"],
        "locations": ["门口", "客厅", "阳台", "车库"],
        "power": (5, 15),  # 5-15瓦
        "usage_pattern": "24x7"  # 全天候
    },
    "智能门锁": {
        "names": ["入户门锁", "卧室门锁"],
        "locations": ["入户门", "卧室"],
        "power": (2, 5),  # 2-5瓦
        "usage_pattern": "occasional"  # 偶尔使用
    },
    "温度传感器": {
        "names": ["客厅温度传感器", "卧室温度传感器", "厨房温度传感器"],
        "locations": ["客厅", "卧室", "厨房"],
        "power": (1, 3),  # 1-3瓦
        "usage_pattern": "24x7"  # 全天候
    },
    "空气净化器": {
        "names": ["客厅净化器", "卧室净化器"],
        "locations": ["客厅", "卧室"],
        "power": (30, 80),  # 30-80瓦
        "usage_pattern": "day_night"  # 白天晚上都用
    },
    "智能插座": {
        "names": ["客厅智能插座", "卧室智能插座", "厨房智能插座"],
        "locations": ["客厅", "卧室", "厨房"],
        "power": (2, 100),  # 2-100瓦（取决于接入设备）
        "usage_pattern": "day_night"
    },
    "窗帘电机": {
        "names": ["客厅窗帘", "卧室窗帘"],
        "locations": ["客厅", "卧室"],
        "power": (15, 30),  # 15-30瓦
        "usage_pattern": "morning_evening"  # 早晚使用
    }
}

SECURITY_EVENT_TYPES = [
    {"type": "陌生人检测", "severity": "中等", "devices": ["摄像头"]},
    {"type": "异常开门", "severity": "高", "devices": ["智能门锁"]},
    {"type": "温度异常", "severity": "中等", "devices": ["温度传感器"]},
    {"type": "设备离线", "severity": "低", "devices": ["摄像头", "温度传感器", "智能插座"]},
    {"type": "入侵警报", "severity": "高", "devices": ["摄像头", "智能门锁"]},
    {"type": "网络异常", "severity": "中等", "devices": ["摄像头", "智能门锁", "温度传感器"]},
    {"type": "功耗异常", "severity": "中等", "devices": ["智能插座", "空调"]},
    {"type": "门锁电量低", "severity": "低", "devices": ["智能门锁"]},
    {"type": "运动检测", "severity": "低", "devices": ["摄像头"]},
    {"type": "温度过高", "severity": "高", "devices": ["温度传感器", "空调"]}
]

FEEDBACK_TYPES = [
    {"type": "故障报告", "ratings": [1, 2, 3]},
    {"type": "使用建议", "ratings": [3, 4, 5]},
    {"type": "满意度评价", "ratings": [4, 5]},
    {"type": "功能请求", "ratings": [3, 4]},
    {"type": "性能反馈", "ratings": [2, 3, 4, 5]}
]

FEEDBACK_CONTENTS = {
    "故障报告": [
        "设备经常断线，需要重新连接",
        "响应速度变慢，操作不流畅",
        "设备发热严重，担心安全问题",
        "夜间模式不工作，影响使用",
        "App经常崩溃，无法正常控制",
        "语音识别准确率不高"
    ],
    "使用建议": [
        "希望能增加定时功能",
        "建议优化手机App界面",
        "希望支持语音控制",
        "建议增加节能模式",
        "希望能设置更多自动化场景",
        "建议增加儿童锁功能"
    ],
    "满意度评价": [
        "产品质量很好，使用体验佳",
        "智能化程度高，很方便",
        "性价比不错，推荐购买",
        "客服态度好，问题解决及时",
        "安装简单，操作方便",
        "外观设计很漂亮，很满意"
    ],
    "功能请求": [
        "希望支持更多智能场景",
        "建议增加数据统计功能",
        "希望能远程控制",
        "建议支持第三方平台接入",
        "希望增加地理围栏功能",
        "建议支持更多品牌设备"
    ],
    "性能反馈": [
        "运行稳定，很少出问题",
        "能耗控制得不错",
        "反应速度还可以提升",
        "整体表现符合预期",
        "连接稳定性有待提高",
        "电池续航表现良好"
    ]
}

def generate_usage_times(device_type, base_date, device_power):
    """根据设备类型生成使用时间记录"""
    usage_records = []
    pattern = DEVICE_TYPES[device_type]["usage_pattern"]
    
    current_date = base_date
    
    if pattern == "24x7":
        # 全天候设备，生成长时间连续使用记录
        segments = random.randint(2, 4)  # 分2-4段运行
        hours_per_segment = 24 / segments
        
        for i in range(segments):
            start_hour = int(i * hours_per_segment) + random.randint(0, 2)
            start_time = current_date.replace(
                hour=min(start_hour, 23), 
                minute=random.randint(0, 59), 
                second=0
            )
            
            # 运行3-8小时
            duration_hours = random.uniform(3, 8)
            end_time = start_time + timedelta(hours=duration_hours)
            
            # 确保不超过当天
            max_end = current_date.replace(hour=23, minute=59, second=59)
            if end_time > max_end:
                end_time = max_end
            
            if start_time < end_time:
                energy = calculate_energy_consumption(device_power, start_time, end_time)
                usage_records.append((start_time, end_time, energy))
    
    elif pattern == "evening_night":
        # 傍晚和夜间使用（18:00-23:00）
        for _ in range(random.randint(1, 3)):
            hour = random.randint(18, 22)
            minute = random.randint(0, 59)
            start_time = current_date.replace(hour=hour, minute=minute, second=0)
            
            # 使用1-5小时
            duration_hours = random.uniform(1, 5)
            end_time = start_time + timedelta(hours=duration_hours)
            
            # 确保不超过当天23:59
            max_end = current_date.replace(hour=23, minute=59, second=59)
            if end_time > max_end:
                end_time = max_end
            
            energy = calculate_energy_consumption(device_power, start_time, end_time)
            usage_records.append((start_time, end_time, energy))
    
    elif pattern == "morning_evening":
        # 早晚使用，如窗帘
        # 早上开窗帘
        if random.random() < 0.8:  # 80%概率早上使用
            morning_hour = random.randint(6, 9)
            start_time = current_date.replace(hour=morning_hour, minute=random.randint(0, 59), second=0)
            end_time = start_time + timedelta(minutes=random.randint(1, 3))  # 1-3分钟
            energy = calculate_energy_consumption(device_power, start_time, end_time)
            usage_records.append((start_time, end_time, energy))
        
        # 晚上关窗帘
        if random.random() < 0.9:  # 90%概率晚上使用
            evening_hour = random.randint(18, 22)
            start_time = current_date.replace(hour=evening_hour, minute=random.randint(0, 59), second=0)
            end_time = start_time + timedelta(minutes=random.randint(1, 3))  # 1-3分钟
            energy = calculate_energy_consumption(device_power, start_time, end_time)
            usage_records.append((start_time, end_time, energy))
    
    elif pattern == "seasonal":
        # 空调季节性使用，夏天使用多
        month = base_date.month
        if month in [6, 7, 8, 9]:  # 夏季使用多
            usage_probability = 0.8
            daily_hours = random.uniform(6, 12)
        elif month in [12, 1, 2]:  # 冬季使用中等
            usage_probability = 0.5
            daily_hours = random.uniform(3, 8)
        else:  # 其他月份使用少
            usage_probability = 0.2
            daily_hours = random.uniform(1, 4)
        
        if random.random() < usage_probability:
            # 可能分几个时间段使用
            segments = random.randint(1, 3)
            hours_per_segment = daily_hours / segments
            
            for _ in range(segments):
                hour = random.randint(8, 22)
                minute = random.randint(0, 59)
                start_time = current_date.replace(hour=hour, minute=minute, second=0)
                end_time = start_time + timedelta(hours=hours_per_segment)
                
                # 确保不超过当天
                max_end = current_date.replace(hour=23, minute=59, second=59)
                if end_time > max_end:
                    end_time = max_end
                
                if start_time < end_time:
                    energy = calculate_energy_consumption(device_power, start_time, end_time)
                    usage_records.append((start_time, end_time, energy))
    
    elif pattern == "day_night":
        # 白天晚上都使用
        for _ in range(random.randint(2, 4)):
            hour = random.randint(7, 22)
            minute = random.randint(0, 59)
            start_time = current_date.replace(hour=hour, minute=minute, second=0)
            
            duration_hours = random.uniform(2, 6)
            end_time = start_time + timedelta(hours=duration_hours)
            
            # 确保不超过当天
            max_end = current_date.replace(hour=23, minute=59, second=59)
            if end_time > max_end:
                end_time = max_end
            
            if start_time < end_time:
                energy = calculate_energy_consumption(device_power, start_time, end_time)
                usage_records.append((start_time, end_time, energy))
    
    elif pattern == "occasional":
        # 偶尔使用，如门锁
        if random.random() < 0.3:  # 30%概率使用
            for _ in range(random.randint(1, 8)):  # 1-8次开关门
                hour = random.randint(6, 23)
                minute = random.randint(0, 59)
                start_time = current_date.replace(hour=hour, minute=minute, second=0)
                
                # 使用时间很短，几秒到几分钟
                duration_seconds = random.uniform(5, 30)
                end_time = start_time + timedelta(seconds=duration_seconds)
                
                energy = calculate_energy_consumption(device_power, start_time, end_time)
                usage_records.append((start_time, end_time, energy))
    
    return usage_records

def calculate_energy_consumption(device_power, start_time, end_time):
    """计算能耗（千瓦时）"""
    duration_hours = (end_time - start_time).total_seconds() / 3600
    # 功率（瓦）× 时间（小时）÷ 1000 = 千瓦时
    energy_kwh = (device_power * duration_hours) / 1000
    return round(energy_kwh, 4)

def generate_test_data():
    """生成测试数据的主函数"""
    db = SessionLocal()
    
    try:
        print("开始生成智能家居测试数据...")
        print("=" * 50)
        
        # 1. 生成用户数据
        print(f"正在生成 {USERS_COUNT} 个用户...")
        users = []
        for i in range(USERS_COUNT):
            user = User(
                name=CHINESE_NAMES[i],
                email=f"user{i+1}@smarthome.com",
                phone=f"1{random.randint(30, 89)}{random.randint(10000000, 99999999)}",
                house_area=round(random.uniform(60, 200), 1)  # 60-200平米
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"✓ 用户数据生成完成")
        
        # 2. 生成设备数据
        print("正在生成设备数据...")
        all_devices = []
        total_devices = 0
        
        for user in users:
            device_count = random.randint(*DEVICES_PER_USER)
            # 确保每个用户至少有一些基础设备
            available_types = list(DEVICE_TYPES.keys())
            user_device_types = random.sample(available_types, min(device_count, len(available_types)))
            
            # 如果设备数量多于类型数量，允许重复类型但不同位置
            while len(user_device_types) < device_count:
                user_device_types.append(random.choice(available_types))
            
            for device_type in user_device_types:
                device_info = DEVICE_TYPES[device_type]
                device_name = random.choice(device_info["names"])
                device_location = random.choice(device_info["locations"])
                
                # 确保同一用户不会有重复的设备名称
                existing_names = [d[0].name for d in all_devices if d[0].user_id == user.id]
                attempts = 0
                while device_name in existing_names and attempts < 10:
                    device_name = f"{random.choice(device_info['names'])}-{random.randint(1, 99)}"
                    attempts += 1
                
                device = Device(
                    name=device_name,
                    type=device_type,
                    location=device_location,
                    user_id=user.id
                )
                db.add(device)
                all_devices.append((device, device_type))
                total_devices += 1
        
        db.commit()
        print(f"✓ 设备数据生成完成，共生成 {total_devices} 个设备")
        
        # 3. 生成设备使用记录
        print("正在生成设备使用记录（这可能需要一些时间）...")
        base_date = datetime.datetime.now() - timedelta(days=DATA_DAYS)
        
        usage_count = 0
        batch_size = 100  # 批量提交，提高性能
        
        for device, device_type in all_devices:
            device_power = random.uniform(*DEVICE_TYPES[device_type]["power"])
            
            # 为每一天生成使用记录
            for day in range(DATA_DAYS):
                current_date = base_date + timedelta(days=day)
                usage_records = generate_usage_times(device_type, current_date, device_power)
                
                for start_time, end_time, energy in usage_records:
                    usage = DeviceUsage(
                        device_id=device.id,
                        user_id=device.user_id,
                        start_time=start_time,
                        end_time=end_time,
                        energy_consumption=energy
                    )
                    db.add(usage)
                    usage_count += 1
                    
                    # 批量提交
                    if usage_count % batch_size == 0:
                        db.commit()
                        print(f"  已生成 {usage_count} 条使用记录...")
        
        db.commit()
        print(f"✓ 设备使用记录生成完成，共生成 {usage_count} 条记录")
        
        # 4. 生成安防事件
        print("正在生成安防事件...")
        security_count = 0
        
        for device, device_type in all_devices:
            # 筛选适用的安防事件类型
            applicable_events = [e for e in SECURITY_EVENT_TYPES if device_type in e["devices"]]
            
            if applicable_events:
                # 每个设备随机生成0-8个安防事件
                event_count = random.randint(0, 8)
                for _ in range(event_count):
                    event_info = random.choice(applicable_events)
                    event_time = base_date + timedelta(
                        days=random.randint(0, DATA_DAYS-1),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59),
                        seconds=random.randint(0, 59)
                    )
                    
                    security_event = SecurityEvent(
                        device_id=device.id,
                        event_type=event_info["type"],
                        severity=event_info["severity"],
                        timestamp=event_time
                    )
                    db.add(security_event)
                    security_count += 1
        
        db.commit()
        print(f"✓ 安防事件生成完成，共生成 {security_count} 个事件")
        
        # 5. 生成用户反馈
        print("正在生成用户反馈...")
        feedback_count = 0
        
        for user in users:
            user_devices = [device for device, _ in all_devices if device.user_id == user.id]
            
            # 每个用户随机对30%-80%的设备提供反馈
            feedback_ratio = random.uniform(0.3, 0.8)
            feedback_device_count = max(1, int(len(user_devices) * feedback_ratio))
            feedback_devices = random.sample(user_devices, min(feedback_device_count, len(user_devices)))
            
            for device in feedback_devices:
                # 每个设备可能有多条反馈
                feedback_per_device = random.randint(1, 3)
                
                for _ in range(feedback_per_device):
                    feedback_type_info = random.choice(FEEDBACK_TYPES)
                    feedback_type = feedback_type_info["type"]
                    rating = random.choice(feedback_type_info["ratings"])
                    content = random.choice(FEEDBACK_CONTENTS[feedback_type])
                    
                    feedback_time = base_date + timedelta(
                        days=random.randint(0, DATA_DAYS-1),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                    
                    feedback = UserFeedback(
                        user_id=user.id,
                        device_id=device.id,
                        feedback_type=feedback_type,
                        content=content,
                        rating=rating,
                        created_at=feedback_time
                    )
                    db.add(feedback)
                    feedback_count += 1
        
        db.commit()
        print(f"✓ 用户反馈生成完成，共生成 {feedback_count} 条反馈")
                
        # 生成数据统计信息
        print("\n" + "=" * 50)
        print("📊 测试数据生成完成！")
        print("=" * 50)
        print(f"👥 用户数量: {USERS_COUNT}")
        print(f"🏠 设备数量: {total_devices}")
        print(f"📈 使用记录: {usage_count:,}")
        print(f"🔒 安防事件: {security_count}")
        print(f"💬 用户反馈: {feedback_count}")
        print(f"📅 数据时间范围: {base_date.strftime('%Y-%m-%d')} 到 {datetime.datetime.now().strftime('%Y-%m-%d')}")
        
        # 设备类型统计
        device_type_count = {}
        for device, device_type in all_devices:
            device_type_count[device_type] = device_type_count.get(device_type, 0) + 1
        
        print(f"\n📱 设备类型分布:")
        for device_type, count in sorted(device_type_count.items()):
            print(f"  {device_type}: {count} 个")
        
        print(f"\n🔧 你现在可以启动你的FastAPI应用来查看这些数据了！")
        
    except Exception as e:
        print(f"❌ 生成数据时出错: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    success = generate_test_data()
    if success:
        print("\n🎉 数据生成成功！")
    else:
        print("\n💥 数据生成失败，请检查错误信息。")