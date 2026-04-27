# AI 企业战略分析助手

**版本**: 2.0.0  
**作者**: Manus AI  
**发布日期**: 2026-04-27  
**许可证**: MIT

## 概述

这是一个**企业战略深度分析工具**，基于 CrewAI 多智能体框架，能够为任何行业生成专业级的战略分析报告。该工具通过多阶段推演（PESTEL → 价值链 → 竞争格局 → SWOT → BCG → 蓝海战略 → 波特五力），确保分析的逻辑严密性和数据透明度。

## 核心特性

*   **七份结构化报告**：PESTEL 宏观分析、价值链拆解、竞争格局、SWOT 深度分析、BCG 矩阵、蓝海战略、波特五力推演、数据审计清单。
*   **白箱化数据处理**：完整展示数据采集量、清洗量、采纳量，以及所有原文链接。
*   **灵活 LLM 适配**：支持 OpenAI、Groq (Llama 3)、Google Gemini，用户可自由选择。
*   **免费 API 方案**：搜索默认使用 DuckDuckGo（完全免费），LLM 支持免费额度方案。
*   **企业级质量控制**：三层 Agent 协同（情报官、分析师、合伙人），确保逻辑闭环。

## 使用场景

*   **行业研究**：快速获得某个细分行业的战略全景。
*   **竞争分析**：深入理解竞争对手的战略定位与护城河。
*   **投资决策**：为 VC/PE 提供行业吸引力评估。
*   **战略规划**：为企业内部战略制定提供数据支撑。

## 快速开始

### 1. 环境准备

```bash
git clone https://github.com/yourusername/ai-strategic-analyst-skill.git
cd ai-strategic-analyst-skill
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `config.example.env` 为 `.env`，并填入您的 API Key：

```bash
cp config.example.env .env
```

**选项 A：使用 Groq（推荐，完全免费）**
```
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
```
申请地址：https://console.groq.com

**选项 B：使用 Google Gemini（推荐，有免费额度）**
```
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key_here
```
申请地址：https://ai.google.dev

**选项 C：使用 OpenAI（需付费）**
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 运行分析

```python
from src.strategic_crew import StrategicCrew

# 初始化（会自动读取 .env 中的 LLM_PROVIDER）
crew = StrategicCrew()

# 执行分析
result = crew.run(industry="中国商用低轨卫星互联网行业 - 面向大型能源企业的专线接入服务")

# 输出七份报告
print(result["pestel_report"]["content"])
print(result["value_chain_report"]["content"])
print(result["landscape_report"]["content"])
print(result["swot_report"]["content"])
print(result["bcg_matrix_report"]["content"])
print(result["blue_ocean_report"]["content"])
print(result["five_forces_report"]["content"])
print(result["audit_report"]["content"])
```

## 输出结构

### 七份报告的完整输出

每份报告都遵循以下结构：

```json
{
  "pestel_report": {
    "title": "PESTEL 宏观环境扫描报告",
    "content": "详细的文字分析...",
    "key_data_points": ["政策点1", "经济指标1", ...],
    "references": [
      {
        "description": "国家发改委, 2024, 《关于推进低轨卫星产业发展的指导意见》",
        "url": "https://example.com/policy"
      }
    ]
  },
  "value_chain_report": {...},
  "landscape_report": {...},
  "swot_report": {...},
  "bcg_matrix_report": {...},
  "blue_ocean_report": {...},
  "five_forces_report": {...},
  "audit_report": {
    "total_searches": 42,
    "total_snippets": 156,
    "adopted_facts": 38,
    "data_quality_score": 0.87
  }
}
```

## 数据审计说明

**数据审计报告** 展示了以下关键指标：

*   **采集量 (Total Searches)**：系统执行的搜索次数。
*   **片段量 (Total Snippets)**：搜索返回的信息片段总数。
*   **采纳量 (Adopted Facts)**：最终被纳入报告的硬数据个数。
*   **清洗率 (Data Quality Score)**：采纳量 / 片段量，反映数据清洗的有效性。

## 扩展与定制

### 添加自定义数据源

编辑 `src/strategic_crew.py` 中的 `SearchToolWrapper` 类，集成您自己的数据源：

```python
class SearchToolWrapper(BaseTool):
    def _run(self, query: str) -> str:
        # 集成您的专有数据库、API 或爬虫
        custom_data = your_data_source.search(query)
        return custom_data
```

### 自定义报告模板

编辑 `templates/` 目录下的 Markdown 模板文件，调整报告的格式与内容结构。

## 常见问题

**Q: 分析需要多长时间？**  
A: 通常 3-8 分钟，取决于行业复杂度和网络速度。

**Q: 可以离线使用吗？**  
A: 不可以。该工具需要网络连接以获取最新数据和调用 LLM API。

**Q: 数据准确性如何保证？**  
A: 通过三层 Agent 协同与数据审计机制。所有硬数据都附带来源链接，用户可自行验证。

## 许可证

MIT License - 详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请在 GitHub 上提交 Issue。
