# AI 企业战略分析助手 - 项目总结

## 📋 项目概览

**AI 企业战略分析助手** 是一个基于 CrewAI 多智能体框架的企业级战略分析工具。它能够为任何行业生成五份专业的战略分析报告，通过白箱化的数据处理机制确保分析的透明度和可信度。

**版本**: 1.0.0  
**发布日期**: 2026-04-27  
**许可证**: MIT  
**作者**: Manus AI

---

## 🎯 核心特性

### 1. 五层次战略分析框架

该工具按照专业咨询公司的标准流程，生成五份结构化报告：

| 报告 | 核心内容 | 应用价值 |
| :--- | :--- | :--- |
| **PESTEL 宏观环境扫描** | 政策、经济、社会、技术、环境、法律六维分析 | 理解行业外部环境与机遇/威胁 |
| **行业价值链与利润池拆解** | 上游、中游、下游各环节的参与者与利润分配 | 识别价值链中的盈利机会 |
| **竞争格局与战略群组分析** | 市场集中度、竞争者、战略群组 | 定位自身的竞争地位 |
| **波特五力深度推演终局** | 基于前三份的逻辑合成，五力评分与建议 | 评估行业吸引力与竞争强度 |
| **数据审计与事实清单** | 数据采集量、清洗量、采纳量、来源链接 | 验证分析的数据基础与透明度 |

### 2. 白箱化数据处理

所有分析都基于可追溯的数据：

*   **采集量统计**：系统执行的搜索次数。
*   **清洗量统计**：搜索返回的信息片段总数。
*   **采纳量统计**：最终被纳入报告的硬数据个数。
*   **数据质量评分**：采纳量 / 片段量，反映数据处理的有效性。
*   **原文链接**：所有硬数据都附带来源 URL，用户可自行验证。

### 3. 灵活的 LLM 适配

支持多种 LLM 提供商，用户可自由选择：

*   **Groq (Llama 3)**：完全免费，速度极快，推荐用于开发和测试。
*   **Google Gemini**：有免费额度，功能强大，适合生产环境。
*   **OpenAI GPT-4**：需付费，质量最高，适合对分析质量要求极高的场景。

### 4. 三层 Agent 协同

通过多个专业角色的协同，确保分析的严密性：

*   **首席情报官**：负责数据采集与验证。
*   **资深战略分析师**：负责数据结构化与框架应用。
*   **管理合伙人**：负责逻辑闭环与最终质量把控。

---

## 📁 项目结构

```
ai-strategic-analyst-skill/
├── SKILL.md                    # Skill 元数据与使用说明
├── README.md                   # 快速开始指南
├── DEPLOYMENT.md               # 部署指南
├── PROJECT_SUMMARY.md          # 本文件
├── LICENSE                     # MIT 开源许可证
├── .gitignore                  # Git 忽略配置
├── requirements.txt            # Python 依赖列表
├── config.example.env          # 环境变量示例
├── src/
│   ├── __init__.py             # 包初始化
│   └── strategic_crew.py       # 核心 Agent 编排逻辑
├── examples/
│   └── sample_usage.py         # 使用示例脚本
├── templates/                  # 报告模板目录（预留）
└── tests/                      # 单元测试目录（预留）
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/yourusername/ai-strategic-analyst-skill.git
cd ai-strategic-analyst-skill

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# 复制配置文件
cp config.example.env .env

# 编辑 .env，选择一种 LLM 方案
# 方案 A: Groq (推荐)
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here

# 方案 B: Google Gemini
# LLM_PROVIDER=gemini
# GOOGLE_API_KEY=your_key_here
```

### 3. 运行分析

```python
from src.strategic_crew import StrategicCrew

crew = StrategicCrew()
result = crew.run(industry="中国新能源汽车充电桩行业")

# 访问各份报告
print(result['pestel_report']['content'])
print(result['value_chain_report']['content'])
print(result['landscape_report']['content'])
print(result['five_forces_report']['content'])
print(result['audit_report']['content'])
```

---

## 📊 输出示例

### PESTEL 报告示例

```
# PESTEL 宏观环境扫描报告

## 政治维度
- 国家出台了《关于推进新能源汽车产业发展的指导意见》(来源: 国家发改委, 2024)
- 各地政府提供充电桩建设补贴...

## 经济维度
- 2024年中国新能源汽车销量达到 850 万辆，同比增长 30% (来源: 中国汽车工业协会, 2024)
- 充电桩行业投资规模达到 200 亿元...

...
```

### 数据审计报告示例

```
# 数据审计与事实清单

## 审计摘要
- 总搜索次数: 42
- 信息片段总数: 156
- 采纳硬数据个数: 38
- 数据质量评分: 0.87 (采纳量/片段量)
- 独立数据源数: 12

## 数据质量说明
当前评分 0.87 表明系统的数据处理能力处于优秀水平。
```

---

## 🔧 技术栈

| 组件 | 技术选型 | 说明 |
| :--- | :--- | :--- |
| **Agent 框架** | CrewAI | 多智能体协同编排 |
| **LLM 集成** | LangChain | 支持多种 LLM 提供商 |
| **搜索工具** | DuckDuckGo API | 完全免费，无需 Key |
| **数据处理** | Pydantic | 结构化数据验证 |
| **环境管理** | python-dotenv | 配置文件管理 |

---

## 💡 使用场景

### 1. 行业研究
快速获得某个细分行业的战略全景，了解宏观环境、价值链、竞争格局。

### 2. 竞争分析
深入理解竞争对手的战略定位、护城河、市场份额。

### 3. 投资决策
为 VC/PE 提供行业吸引力评估，支持投资决策。

### 4. 战略规划
为企业内部战略制定提供数据支撑和逻辑框架。

### 5. 市场进入评估
评估进入新市场的可行性和风险。

---

## 🔍 数据透明度机制

### 白箱化展示

每份报告都包含详细的数据审计信息，用户可以清晰地看到：

*   数据从哪里来（来源机构、媒体、报告）。
*   数据如何被处理（采集、清洗、采纳的数量）。
*   数据的可信度（来源可信度评分）。

### 可验证性

所有硬数据都附带原文链接，用户可以：

*   点击链接查看原始信息。
*   交叉验证多个来源的数据。
*   独立评估数据的准确性。

---

## 🛠️ 扩展与定制

### 集成自定义数据源

编辑 `src/strategic_crew.py` 中的 `SearchToolWrapper` 类，集成您的专有数据库或 API。

### 自定义报告模板

编辑 `templates/` 目录下的 Markdown 文件，调整报告的格式与内容结构。

### 添加新的分析维度

在 `StrategicCrew` 类中添加新的 Task，实现额外的分析维度（如 SWOT、蓝海战略等）。

---

## 📈 性能指标

| 指标 | 目标值 | 说明 |
| :--- | :--- | :--- |
| **分析耗时** | 2-5 分钟 | 取决于行业复杂度和网络速度 |
| **数据质量评分** | >0.8 | 采纳量 / 片段量 |
| **报告完整性** | 100% | 五份报告都应完整生成 |
| **来源覆盖** | >10 个 | 至少 10 个独立数据源 |

---

## ❓ 常见问题

**Q: 分析需要多长时间？**  
A: 通常 2-5 分钟，取决于行业复杂度和网络速度。

**Q: 可以离线使用吗？**  
A: 不可以。该工具需要网络连接以获取最新数据和调用 LLM API。

**Q: 数据准确性如何保证？**  
A: 通过三层 Agent 协同与完整的数据审计机制。所有硬数据都附带来源链接，用户可自行验证。

**Q: 支持哪些行业？**  
A: 理论上支持所有行业。建议输入具体的细分行业和目标客群以获得最佳结果。

**Q: 如何选择 LLM 提供商？**  
A: 
- **开发/测试**：使用 Groq（完全免费，速度快）。
- **生产环境**：使用 Gemini（有免费额度，功能强大）。
- **高质量需求**：使用 OpenAI GPT-4（需付费）。

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Issue

描述问题、期望行为和实际行为。

### 提交 Pull Request

1. Fork 仓库。
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 开启 Pull Request。

---

## 📞 联系方式

如有问题或建议，请在 GitHub 上提交 Issue 或联系 Manus AI 团队。

---

## 📄 许可证

MIT License - 详见 LICENSE 文件。

---

## 🙏 致谢

感谢以下开源项目的支持：

*   [CrewAI](https://github.com/joaomdmoura/crewai)
*   [LangChain](https://github.com/langchain-ai/langchain)
*   [Pydantic](https://github.com/pydantic/pydantic)

---

**版本**: 1.0.0  
**最后更新**: 2026-04-27  
**维护者**: Manus AI
