# AI 企业战略分析助手

一个基于 CrewAI 的**企业级战略分析工具**，能够为任何行业生成专业的深度战略分析报告。

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![Status](https://img.shields.io/badge/status-Active-success)

## 🎯 核心价值

*   **深度分析**：从宏观环境到微观竞争，再到战略选择的全景推演。
*   **数据透明**：白箱化展示数据采集、清洗、采纳的全过程，并提供来源追溯。
*   **即插即用**：支持多种免费 LLM 方案，用户无需复杂配置。
*   **专业输出**：七份结构化报告，可直接用于董事会汇报。

## 📊 输出报告

该工具生成以下七份专业报告：

| 报告名称 | 核心内容 | 应用场景 |
| :--- | :--- | :--- |
| **PESTEL 宏观环境扫描报告** | 政策、经济、社会、技术、环境、法律六个维度的宏观分析 | 理解行业外部环境与机遇/威胁 |
| **行业价值链与利润池拆解报告** | 上游、中游、下游各环节的参与者、利润分配与价值捕获 | 识别价值链中的盈利机会 |
| **竞争格局与战略群组分析报告** | 市场集中度、主要竞争者、战略群组分析 | 定位自身的竞争地位 |
| **SWOT 深度分析报告** | 内部优势/劣势，外部机会/威胁，并提供战略启示 | 综合评估企业内外环境，制定战略方向 |
| **BCG 矩阵分析报告** | 业务单元的相对市场份额与市场增长率，象限判断与战略建议 | 评估业务组合，优化资源配置 |
| **蓝海战略分析报告** | ERRC 框架（剔除、减少、增加、创造），重塑价值曲线，发现新市场 | 寻找差异化竞争，开辟新市场空间 |
| **波特五力深度推演终局报告** | 基于所有分析的综合，五力评分与战略建议 | 评估行业吸引力与竞争强度 |
| **数据审计与事实清单** | 数据采集量、清洗量、采纳量、原文链接汇总 | 验证分析的数据基础与透明度 |

## 🚀 快速开始

### 前置要求

*   Python 3.9+
*   pip 或 conda
*   Git

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/ai-strategic-analyst-skill.git
cd ai-strategic-analyst-skill
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key（选择一种方案）

**方案 A：Groq（推荐，完全免费）**

1. 访问 https://console.groq.com，注册并获取 API Key。
2. 创建 `.env` 文件：

```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
```

**方案 B：Google Gemini（推荐，有免费额度）**

1. 访问 https://ai.google.dev，申请 API Key。
2. 创建 `.env` 文件：

```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key_here
```

**方案 C：OpenAI（需付费）**

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. 运行分析

```python
from src.strategic_crew import StrategicCrew

# 初始化
crew = StrategicCrew()

# 执行分析（输入行业名称）
result = crew.run(industry="中国新能源汽车充电桩行业 - 面向个人用户的快充服务")

# 访问各份报告
print("=" * 80)
print("📊 PESTEL 宏观环境扫描报告")
print("=" * 80)
print(result["pestel_report"]["content"])

print("\n" + "=" * 80)
print("🔗 行业价值链与利润池拆解报告")
print("=" * 80)
print(result["value_chain_report"]["content"])

print("\n" + "=" * 80)
print("⚔️ 竞争格局与战略群组分析报告")
print("=" * 80)
print(result["landscape_report"]["content"])

print("\n" + "=" * 80)
print("💪 SWOT 深度分析报告")
print("=" * 80)
print(result["swot_report"]["content"])

print("\n" + "=" * 80)
print("📈 BCG 矩阵分析报告")
print("=" * 80)
print(result["bcg_matrix_report"]["content"])

print("\n" + "=" * 80)
print("🌊 蓝海战略分析报告")
print("=" * 80)
print(result["blue_ocean_report"]["content"])

print("\n" + "=" * 80)
print("🔥 波特五力深度推演终局报告")
print("=" * 80)
print(result["five_forces_report"]["content"])

print("\n" + "=" * 80)
print("🔍 数据审计与事实清单")
print("=" * 80)
print(result["audit_report"]["content"])
```

## 📁 项目结构

```
ai-strategic-analyst-skill/
├── SKILL.md                    # Skill 元数据
├── README.md                   # 本文件
├── requirements.txt            # Python 依赖
├── config.example.env          # 环境变量示例
├── src/
│   ├── __init__.py
│   └── strategic_crew.py       # 核心 Agent 编排
├── templates/
│   ├── pestel_template.md
│   ├── value_chain_template.md
│   ├── landscape_template.md
│   ├── swot_template.md
│   ├── bcg_template.md
│   ├── blue_ocean_template.md
│   └── five_forces_template.md
├── examples/
│   └── sample_usage.py         # 示例输出
└── tests/
    └── test_crew.py            # 单元测试
```

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置以下变量：

```bash
# LLM 提供商选择：groq, gemini, openai
LLM_PROVIDER=groq

# 对应的 API Key
GROQ_API_KEY=xxx
GOOGLE_API_KEY=xxx
OPENAI_API_KEY=xxx

# 搜索工具（默认 DuckDuckGo，无需配置）
SEARCH_PROVIDER=duckduckgo
```

## 📈 输出示例

详见 `examples/sample_analysis.json`，包含完整的七份报告输出示例。

## 🔍 数据审计机制

每份报告都附带详细的数据审计信息：

*   **采集量**：系统执行的搜索次数。
*   **片段量**：搜索返回的信息片段总数。
*   **采纳量**：最终被纳入报告的硬数据个数。
*   **清洗率**：采纳量 / 片段量，反映数据质量。
*   **来源链接**：所有引用的原文 URL。

## 🛠️ 扩展与定制

### 集成自定义数据源

编辑 `src/strategic_crew.py`，修改 `SearchToolWrapper` 类以集成您的数据源：

```python
class SearchToolWrapper(BaseTool):
    def _run(self, query: str) -> str:
        # 集成您的专有数据库或 API
        return your_data_source.search(query)
```

### 自定义报告模板

编辑 `templates/` 目录下的 Markdown 文件，调整报告格式。

### 添加新的分析维度

在 `StrategicCrew` 类中添加新的 Task，实现额外的分析维度（如 SWOT、蓝海战略等）。

## ❓ 常见问题

**Q: 分析需要多长时间？**  
A: 通常 3-8 分钟，取决于行业复杂度和网络速度。

**Q: 可以离线使用吗？**  
A: 不可以。该工具需要网络连接以获取最新数据。

**Q: 如何保证分析的准确性？**  
A: 通过三层 Agent 协同（情报官、分析师、合伙人）和完整的数据审计机制。所有数据都附带来源链接。

**Q: 支持哪些行业？**  
A: 理论上支持所有行业。建议输入具体的细分行业和目标客群以获得最佳结果。

**Q: 如何选择 LLM 提供商？**  
A: 
- **开发/测试**：使用 Groq（完全免费，速度快）。
- **生产环境**：使用 Gemini（有免费额度，功能强大）。
- **高质量需求**：使用 OpenAI GPT-4（需付费）。

## 📝 许可证

MIT License - 详见 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请在 GitHub 上提交 Issue。

---

**版本**: 2.0.0  
**最后更新**: 2026-04-27  
**维护者**: Manus AI
