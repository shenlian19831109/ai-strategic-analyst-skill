# 部署指南

本文档提供了将 **AI 企业战略分析助手** 部署到不同环境的详细步骤。

## 目录

1. [本地开发环境](#本地开发环境)
2. [Docker 容器部署](#docker-容器部署)
3. [云平台部署](#云平台部署)
4. [故障排查](#故障排查)

---

## 本地开发环境

### 前置要求

*   Python 3.9+
*   pip 或 conda
*   Git

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/ai-strategic-analyst-skill.git
cd ai-strategic-analyst-skill
```

#### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

```bash
cp config.example.env .env
```

编辑 `.env` 文件，填入您的 API Key（选择一种 LLM 方案）。

#### 5. 运行示例

```bash
python examples/sample_usage.py
```

---

## Docker 容器部署

### 前置要求

*   Docker
*   Docker Compose (可选)

### 创建 Dockerfile

在项目根目录创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口（如果使用 Streamlit）
EXPOSE 8501

# 设置入口点
CMD ["python", "examples/sample_usage.py"]
```

### 构建并运行

```bash
# 构建镜像
docker build -t ai-strategic-analyst:latest .

# 运行容器
docker run --env-file .env ai-strategic-analyst:latest
```

### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  strategic-analyst:
    build: .
    env_file: .env
    volumes:
      - ./output:/app/output
    ports:
      - "8501:8501"
```

运行：

```bash
docker-compose up
```

---

## 云平台部署

### AWS Lambda

1. 打包项目：

```bash
zip -r function.zip . -x "venv/*" ".git/*"
```

2. 在 AWS Lambda 控制台创建函数，上传 `function.zip`。

3. 设置环境变量（LLM_PROVIDER, GROQ_API_KEY 等）。

### Google Cloud Run

1. 创建 `main.py`：

```python
from src.strategic_crew import StrategicCrew

def analyze(request):
    request_json = request.get_json()
    industry = request_json.get('industry', 'default_industry')
    
    crew = StrategicCrew()
    result = crew.run(industry=industry)
    
    return result
```

2. 部署：

```bash
gcloud run deploy strategic-analyst \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars LLM_PROVIDER=groq,GROQ_API_KEY=your_key
```

### Heroku

1. 创建 `Procfile`：

```
web: python examples/sample_usage.py
```

2. 部署：

```bash
heroku create your-app-name
heroku config:set LLM_PROVIDER=groq GROQ_API_KEY=your_key
git push heroku main
```

---

## 故障排查

### 问题 1: ImportError - 找不到模块

**解决方案**：确保虚拟环境已激活，依赖已安装。

```bash
pip install -r requirements.txt
```

### 问题 2: API Key 无效

**解决方案**：检查 `.env` 文件中的 API Key 是否正确，是否已过期。

### 问题 3: 网络连接错误

**解决方案**：确保网络连接正常，防火墙未阻止 API 调用。

### 问题 4: LLM 响应超时

**解决方案**：增加超时时间或选择更快的 LLM 提供商（如 Groq）。

---

## 性能优化

### 1. 缓存搜索结果

在 `src/strategic_crew.py` 中添加缓存机制：

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_search(query: str) -> str:
    # 搜索逻辑
    pass
```

### 2. 并行处理

使用 `concurrent.futures` 并行执行多个搜索：

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(search_function, queries)
```

### 3. 数据库缓存

集成 Redis 或 MongoDB 以缓存分析结果。

---

## 监控与日志

### 配置日志

在 `src/strategic_crew.py` 中添加日志：

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('strategic_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### 监控指标

*   API 调用次数
*   平均响应时间
*   错误率
*   数据质量评分

---

## 安全建议

1. **不要在代码中硬编码 API Key**，使用环境变量。
2. **使用 HTTPS** 传输数据。
3. **定期轮换 API Key**。
4. **限制 API 调用频率**，防止滥用。
5. **对输入进行验证**，防止注入攻击。

---

## 支持

如有部署问题，请在 GitHub 上提交 Issue。
