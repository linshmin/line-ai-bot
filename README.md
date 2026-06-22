# LINE客服AI机器人

基于FastAPI和OpenAI的LINE客服机器人，支持AI对话、上下文记忆、知识库检索和富文本消息。

## 功能特性

- ✅ LINE消息接收与回复
- ✅ AI智能对话（基于OpenAI GPT-4o-mini）
- ✅ 上下文记忆（Redis）
- ✅ 知识库检索（RAG）
- ✅ 快速回复按钮
- ✅ 图片和卡片消息支持
- ✅ 云端部署（Render）

## 技术栈

- **后端框架**: FastAPI + Uvicorn
- **AI模型**: OpenAI GPT-4o-mini
- **向量数据库**: sentence-transformers
- **缓存**: Redis
- **部署**: Render

## 本地开发

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd line-ai-bot
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
OPENAI_API_KEY=your_openai_api_key
REDIS_URL=redis://localhost:6379/0
```

### 5. 安装Redis

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
```

**Windows:**
下载并安装 [Redis for Windows](https://github.com/microsoftarchive/redis/releases)

### 6. 启动Redis

```bash
redis-server
```

### 7. 运行应用

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

应用将在 `http://localhost:8000` 运行。

### 8. 测试Webhook

使用ngrok暴露本地服务器：

```bash
ngrok http 8000
```

将ngrok URL + `/webhook` 配置到LINE Developers Console。

## 部署到Render

### 1. 准备工作

- 创建 [Render](https://render.com/) 账户
- 准备好GitHub仓库
- 准备好LINE和OpenAI的API密钥

### 2. 部署步骤

#### 方法一：使用render.yaml（推荐）

1. 将代码推送到GitHub
2. 在Render中点击 "New +"
3. 选择 "Blueprint"
4. 连接你的GitHub仓库
5. Render会自动读取 `render.yaml` 配置
6. 配置环境变量：
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_CHANNEL_SECRET`
   - `OPENAI_API_KEY`
7. 点击 "Deploy"

#### 方法二：手动部署

1. 在Render中创建新的Web Service
2. 选择Python运行时
3. 连接GitHub仓库
4. 配置构建和启动命令：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. 配置环境变量（同上）
6. 添加Redis数据库：
   - 在Dashboard中创建Redis实例
   - 获取Redis连接信息
   - 更新环境变量 `REDIS_URL`

### 3. 获取部署URL

部署完成后，Render会提供一个URL，例如：`https://line-ai-bot.onrender.com`

### 4. 配置LINE Webhook

1. 登录 [LINE Developers Console](https://developers.line.biz/console/)
2. 选择你的Messaging API Channel
3. 在 "Messaging API" 设置中：
   - Webhook URL: `https://your-app-url.onrender.com/webhook`
   - 启用 "Use webhook"
4. 点击 "Verify" 验证Webhook

## 免费部署平台推荐

### 1. Render
- **免费额度**: 免费层（750小时/月）
- **优点**: 自动SSL，支持Python，配置简单
- **缺点**: 免费实例会休眠，首次访问需要冷启动
- **适用**: 小型项目，低流量应用

### 2. Railway
- **免费额度**: 每月$5额度
- **优点**: 界面友好，支持多语言
- **缺点**: 免费额度有限
- **适用**: 测试和开发环境

### 3. Fly.io
- **免费额度**: 永久免费层（3个256MB VM）
- **优点**: 全球部署，性能好
- **缺点**: 配置相对复杂
- **适用**: 需要全球部署的项目

### 4. Vercel
- **免费额度**: 无限静态部署，Server Functions有限制
- **优点**: 部署速度快，CDN好
- **缺点**: 主要用于前端，Python支持有限
- **适用**: 前端为主的项目

## 知识库管理

### 查看当前知识库

知识库数据存储在 `data/knowledge_base/knowledge.json`。

### 添加知识

你可以通过以下方式添加知识：

1. **直接编辑JSON文件**：
   ```json
   {
     "documents": [
       {
         "id": "1",
         "content": "你的知识内容",
         "category": "分类"
       }
     ],
     "embeddings": []
   }
   ```

2. **使用代码添加**：
   ```python
   from app.knowledge_base import knowledge_base

   knowledge_base.add_document(
       content="新的知识内容",
       category="分类"
   )
   ```

## 测试

运行测试：

```bash
pytest tests/ -v
```

## API文档

启动应用后，访问：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 环境变量说明

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Channel Access Token | 是 |
| `LINE_CHANNEL_SECRET` | LINE Channel Secret | 是 |
| `OPENAI_API_KEY` | OpenAI API密钥 | 是 |
| `OPENAI_MODEL` | OpenAI模型名称 | 否（默认gpt-4o-mini） |
| `REDIS_URL` | Redis连接URL | 是 |
| `EMBEDDING_MODEL` | 向量嵌入模型 | 否 |
| `APP_HOST` | 应用主机地址 | 否（默认0.0.0.0） |
| `APP_PORT` | 应用端口 | 否（默认8000） |
| `DEBUG` | 调试模式 | 否（默认True） |

## 故障排除

### 1. Redis连接失败

确保Redis正在运行：
```bash
redis-cli ping
# 应该返回 PONG
```

### 2. LINE Webhook验证失败

检查：
- Webhook URL是否正确
- 签名验证是否通过
- 防火墙是否允许访问

### 3. OpenAI API调用失败

检查：
- API密钥是否正确
- 账户是否有足够额度
- 网络连接是否正常

## 项目结构

```
line-ai-bot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI主应用
│   ├── line_handler.py      # LINE消息处理
│   ├── ai_handler.py        # AI对话处理
│   ├── memory.py            # 上下文记忆
│   └── knowledge_base.py    # 知识库管理
├── config/
│   ├── __init__.py
│   └── settings.py          # 配置管理
├── data/
│   └── knowledge_base/      # 知识库数据
├── tests/
│   ├── __init__.py
│   └── test_main.py         # 测试文件
├── .env.example             # 环境变量示例
├── .gitignore
├── requirements.txt         # Python依赖
├── Dockerfile               # Docker配置
├── Procfile                 # Render部署配置
├── render.yaml              # Render Blueprint配置
└── README.md                # 项目文档
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！