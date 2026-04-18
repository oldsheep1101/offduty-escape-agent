# 下班逃离助手 🎬🍽️

基于 HelloAgents 框架和 Vue3 构建的智能下班娱乐规划助手，集成高德地图 MCP 服务，在回家路上为你规划一场电影+美食的逃离之旅。

## ✨ 功能特点

- 🎬 **智能影院推荐**: 在回家路线沿途自动搜索最近的电影院
- 🍽️ **周边美食搜索**: 基于电影院位置，搜索附近3公里内的餐厅
- 🛣️ **精准路线规划**: 使用高德地图 API 规划实际驾乘路线和耗时
- ⏰ **合理时间安排**: 根据下班时间和电影场次智能安排晚餐时间
- 📍 **直观地图展示**: 高德地图标记电影院、餐厅位置
- 🎨 **现代化前端**: Vue3 + TypeScript + Ant Design Vue，流畅用户体验

## 🏗️ 技术栈

### 后端

- **框架**: FastAPI + HelloAgents (SimpleAgent)
- **MCP工具**: amap-mcp-server (高德地图)
- **LLM**: 支持 OpenAI / DeepSeek 等多种 LLM 提供商
- **Python**: 3.10+

### 前端

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design Vue
- **地图服务**: 高德地图 JavaScript API
- **HTTP客户端**: Axios

## 📁 项目结构

```
helloagents-trip-planner/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── agents/            # Agent实现
│   │   │   ├── trip_planner_agent.py      # 旅行规划Agent
│   │   │   └── escape_planner_agent.py    # 逃离助手Agent
│   │   ├── api/               # FastAPI路由
│   │   │   ├── main.py
│   │   │   └── routes/
│   │   │       ├── trip.py              # 旅行规划API
│   │   │       └── escape.py            # 逃离助手API
│   │   ├── services/          # 服务层
│   │   │   ├── amap_service.py         # 高德地图服务
│   │   │   └── llm_service.py          # LLM服务
│   │   ├── models/            # 数据模型
│   │   │   └── schemas.py
│   │   └── config.py          # 配置管理
│   ├── requirements.txt
│   └── .env.example
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── services/          # API服务
│   │   ├── types/            # TypeScript类型
│   │   └── views/            # 页面视图
│   │       ├── Home.vue               # 旅行规划首页
│   │       ├── Result.vue            # 旅行结果页
│   │       ├── EscapeHome.vue        # 逃离助手首页
│   │       └── EscapeResult.vue       # 逃离结果页
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 🚀 快速开始

### 前提条件

- Python 3.10+
- Node.js 16+
- 高德地图 API 密钥 (Web 服务 API + Web 端 JS API)
- LLM API 密钥 (OpenAI / DeepSeek 等)

### 后端安装

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
```

启动后端服务：

```bash
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端安装

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
# 创建 .env 文件，填入高德地图 Web API Key 和 Web 端 JS API Key
VITE_AMAP_WEB_JS_KEY=你的高德Web端JS API Key
VITE_API_BASE_URL=http://localhost:8000

# 启动开发服务器
npm run dev
```

打开浏览器访问 `http://localhost:5173/escape` 开始使用下班逃离助手。

## 📝 使用指南

### 下班逃离助手

1. **填写信息**:
   - 公司/起点地址
   - 回家方向/终点地址
   - 下班时间
   - 所在城市
   - 电影偏好（可选）

2. **点击"开始规划"**:
   - 系统自动搜索路线沿途的电影院
   - 根据实际驾乘路线计算到达时间
   - 搜索电影院附近的餐厅
   - 生成完整的时间线

3. **查看结果**:
   - 逃离时间线：下班 → 晚餐 → 电影 → 结束
   - 电影院信息与可选场次（19:00 / 19:30 / 20:00）
   - 餐厅推荐与距离
   - 地图标记电影院和餐厅位置

### 智能旅行助手

访问 `http://localhost:5173/` 使用传统旅行规划功能。

## 🔧 核心实现

### 高德地图 MCP 集成

```python
from hello_agents.tools import MCPTool

# 创建高德地图 MCP 工具
amap_tool = MCPTool(
    name="amap",
    server_command=["uvx", "amap-mcp-server"],
    env={"AMAP_MAPS_API_KEY": "your_api_key"},
    auto_expand=True
)
```

### 智能体协作流程

```
用户输入 → 地理编码 → 搜索电影院 → 路线规划 → 搜索餐厅 → 生成时间线
   ↓           ↓            ↓           ↓           ↓           ↓
  起终点    获取坐标    沿途推荐    计算耗时    附近推荐    合理安排
```

### 关键 API 调用

- `maps_geo`: 地址转经纬度坐标
- `maps_text_search`: 搜索电影院、餐厅 POI
- `maps_direction_driving_by_address`: 驾乘路线规划

## 📄 API 文档

启动后端服务后，访问 `http://localhost:8000/docs` 查看完整 API 文档。

主要端点：

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/escape/plan` | POST | 生成下班逃离计划 |
| `/api/trip/plan` | POST | 生成旅行计划 |
| `/api/map/poi` | GET | 搜索 POI |
| `/api/map/route` | POST | 规划路线 |

## ⚙️ 环境变量配置

### 后端 (.env)

```env
# 高德地图
AMAP_API_KEY=你的高德地图API Key

# LLM 配置 (支持 OpenAI / DeepSeek 等)
LLM_API_KEY=你的LLM API Key
LLM_BASE_URL=https://api.openai.com/v1  # 或其他 LLM 提供商地址
LLM_MODEL_ID=gpt-4  # 或其他模型
```

### 前端 (.env)

```env
VITE_AMAP_WEB_JS_KEY=你的高德地图Web端JS API Key
VITE_API_BASE_URL=http://localhost:8000
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📜 开源协议

CC BY-NC-SA 4.0

## 🙏 致谢

- [HelloAgents](https://github.com/datawhalechina/Hello-Agents) - 智能体教程
- [HelloAgents框架](https://github.com/jjyaoao/HelloAgents) - 智能体框架
- [高德地图开放平台](https://lbs.amap.com/) - 地图服务
- [amap-mcp-server](https://github.com/sugarforever/amap-mcp-server) - 高德地图 MCP 服务器

---

**下班逃离助手** - 让每一个加班日都有逃离的可能 🎬🍽️
