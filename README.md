# Smart-Home-API

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)


一个基于 FastAPI + PostgreSQL 构建的智能家居系统后端 API，支持用户管理、设备管理、使用记录、安防事件、用户反馈与数据分析等功能。

## 🌟 核心功能


- **用户与设备管理** 
  -  用户注册、设备添加、绑定用户
- **使用记录追踪** 
  - 记录设备的开启时间、关闭时间和能耗
- **安防事件管理** 
  - 安全事件记录与警报，包括事件类型、时间和处理状态
- **用户反馈系统** 
  - 用户满意度调查与反馈收集
- **数据分析可视化** 
  - 不同设备的使用频率和使用时间段分析
  - 用户使用习惯分析
  - 房屋面积与设备使用行为相关性分析
  - 安防事件相关性分析
  - 用户满意度与使用频率分析
  - 设备能耗分析
> 📌 数据分析接口支持通过 user_id 参数进行个性化用户分析，未提供时则进行全局分析。

## 📁 项目结构

```bash
Smart-Home-API/
├── app/
│   ├── database.py          # 数据库连接配置
│   ├── models.py            # SQLAlchemy ORM 数据模型
│   ├── schemas.py           # Pydantic 校验模型
│   ├── crud.py              # 数据库增删改查逻辑
│   ├── analytics.py         # 数据分析（返回 Base64 图像）
│   └── routers/             # API 路由模块
│       ├── user_router.py
│       ├── device_router.py
│       ├── usage_router.py
│       ├── security_router.py
│       ├── feedback_router.py
│       └── analytics_router.py
├── .env                     # 环境变量配置
├── generator.py             # 测试数据生成脚本
├── main.py                  # FastAPI 应用入口
├── requirements.txt         # 项目依赖
├── alembic/                     # 数据库迁移工具
│   ├── env.py                   # Alembic环境配置
│   └── versions/                # 数据库版本管理
├── alembic.ini              # Alembic 配置文件
└── README.md
```

## 🚀 快速开始

### 1. 配置环境变量

修改根目录下 `.env` 文件：

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smart_home
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库初始化

确保 PostgreSQL 中已存在名为 `smart_home` 的数据库，否则请手动创建：
    
```bash
# 使用PostgreSQL命令行工具创建数据库
createdb -U postgres smart_home

# 或者使用SQL命令
psql -U postgres -c "CREATE DATABASE smart_home;"
```

执行数据库迁移：

```bash
# 初始化Alembic（如果是第一次使用）
alembic init alembic

# 创建新的迁移文件
alembic revision --autogenerate -m "描述你的更改"

# 执行迁移
alembic upgrade head
```

### 6. 启动 API 服务

```
uvicorn main:app --reload
```

### 7. 访问API文档

服务启动后，访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs

- **Redoc 文档**: http://localhost:8000/redoc

## 🧪 测试数据生成（可选）

项目提供了测试数据生成脚本，用于快速填充数据库：

```bash
python generator.py
```

该脚本将生成：
- 模拟用户数据
- 各类智能设备信息
- 设备使用记录
- 安防事件记录
- 用户反馈数据


## 📊 数据分析功能

### 支持的分析类型

提供数据分析接口，支持 `user_id` （整数）作为查询参数（可选，支持全局或用户级分析），可视化结果返回 Base64 编码图像：

| 分析功能 | 接口路径 | 图表类型 | 说明 |
|---------|----------|----------|------|
| 设备使用频率 | `/api/v1/analytics/device-usage-frequency` | 柱状图 | 统计各设备的使用频次 |
| 使用时间模式 | `/api/v1/analytics/device_usage_time_slot` | 折线图 | 分析设备使用的时间分布 |
| 用户使用习惯 | `/api/v1/analytics/usage-patterns` | 热力图 | 分析设备协同使用模式 |
| 房屋面积影响 | `/api/v1/analytics/area-impact` | 散点图 | 房屋面积与设备使用的关系 |
| 安防事件关联 | `/api/v1/analytics/security-device-correlation` | 热力图 | 安防事件与设备的关联度 |
| 满意度分析 | `/api/v1/analytics/satisfaction-analysis` | 散点图 | 用户满意度与使用频率关系 |
| 能耗分布 | `/api/v1/analytics/energy-consumption-distribution` | 饼图 | 各设备类型的能耗占比 |


### 使用示例

```bash
# 获取用户ID为1的设备使用频率分析
curl -X GET "http://localhost:8000/api/v1/analytics/device-usage-frequency?user_id=1"

# 获取全局使用模式分析
curl -X GET "http://localhost:8000/api/v1/analytics/usage-patterns"

# 获取特定用户的满意度分析
curl -X GET "http://localhost:8000/api/v1/analytics/satisfaction-analysis?user_id=1"
```

### 返回格式
所有分析接口返回Base64编码的图像数据：

```
{
  "chart": "iVBORw0KGgoAAAANSUhEUgAAA+gAAAJYCAYAAADxHswlAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuMiwgaHR0cHM6Ly9t="
}
```

由于本项目只提供后端建立，为测试图像可视化效果，可选择复制 Base64 编码到 Base64 图片转换网站进行测试。

网站示例：[BASE64转图片](https://tool.jisuapi.com/base642pic.html)

