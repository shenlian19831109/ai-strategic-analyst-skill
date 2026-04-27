"""
核心战略分析引擎 - 基于 CrewAI 多智能体框架 (V2 - 深度分析版)
"""

from pydantic import BaseModel, Field, ConfigDict
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import BaseTool
import os
import json
import re
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============================================================================
# 数据审计类 - 白箱化统计
# ============================================================================

class DataAudit:
    """用于追踪数据采集、清洗、采纳的全过程"""
    
    def __init__(self):
        self.total_searches = 0
        self.total_snippets = 0
        self.adopted_facts = 0
        self.sources = []
        self.stage_stats = {}

    def add_search(self, stage: str, count: int = 1):
        self.total_searches += count
        if stage not in self.stage_stats:
            self.stage_stats[stage] = {"searches": 0, "facts": 0}
        self.stage_stats[stage]["searches"] += count

    def add_snippets(self, count: int):
        self.total_snippets += count

    def add_adopted(self, stage: str, count: int):
        self.adopted_facts += count
        if stage not in self.stage_stats:
            self.stage_stats[stage] = {"searches": 0, "facts": 0}
        self.stage_stats[stage]["facts"] += count

    def add_source(self, source: Dict):
        # 避免重复添加相同的源
        if source not in self.sources:
            self.sources.append(source)

    def get_quality_score(self) -> float:
        """计算数据质量评分 (采纳量 / 片段量)"""
        if self.total_snippets == 0:
            return 0.0
        return round(self.adopted_facts / self.total_snippets, 2)

    def to_dict(self) -> Dict:
        return {
            "total_searches": self.total_searches,
            "total_snippets": self.total_snippets,
            "adopted_facts": self.adopted_facts,
            "data_quality_score": self.get_quality_score(),
            "stage_breakdown": self.stage_stats,
            "unique_sources": len(self.sources)
        }

# 全局审计实例
audit_log = DataAudit()

# ============================================================================
# 工具包装器
# ============================================================================

class SearchToolWrapper(BaseTool):
    """DuckDuckGo 搜索工具包装器，用于深度市场数据、竞争格局、财务指标和政策环境。"""
    
    name: str = "deep_market_search"
    description: str = (
        "用于搜索特定行业的深度市场数据、竞争格局、财务指标和政策环境。" \
        "尤其擅长查找具体的市场份额、增长率、政策文件、财报数据和行业报告。"
    )
    
    def _run(self, query: str) -> str:
        audit_log.add_search("general_search", 1)
        search = DuckDuckGoSearchRun()
        res = search.run(query)
        # 估算片段数量，并记录来源
        snippets = len(res.split("\n"))
        audit_log.add_snippets(snippets)
        # 尝试从搜索结果中提取 URL 和描述
        for line in res.split("\n"):
            match = re.search(r"^\d+\. \[(.*?)\]\((.*?)\)", line)
            if match:
                audit_log.add_source({"description": match.group(1), "url": match.group(2), "credibility": 5})
        return res

# ============================================================================
# Pydantic 数据模型
# ============================================================================

class SourceReference(BaseModel):
    """来源引用"""
    description: str = Field(..., description="来源描述：机构/媒体, 年份, 报告/文章名")
    url: Optional[str] = Field(None, description="原文链接")
    credibility: int = Field(default=5, description="可信度评分 (1-10)")

class StrategicReport(BaseModel):
    """战略报告基础模型"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    title: str = Field(..., description="报告标题")
    content: str = Field(..., description="详细的文字报告内容，要求分段清晰，逻辑严密")
    key_data_points: List[str] = Field(default_factory=list, description="报告中引用的核心硬数据")
    references: List[SourceReference] = Field(default_factory=list, description="本阶段引用的参考资料")

class SWOTItem(BaseModel):
    """SWOT 分析的单个条目"""
    description: str = Field(..., description="条目描述")
    key_data_points: List[str] = Field(default_factory=list, description="支撑该条目的数据点")
    references: List[SourceReference] = Field(default_factory=list, description="支撑该条目的参考资料")

class SWOTReport(BaseModel):
    """SWOT 分析报告"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    title: str = Field("SWOT 深度分析报告", description="报告标题")
    strengths: List[SWOTItem] = Field(default_factory=list, description="优势")
    weaknesses: List[SWOTItem] = Field(default_factory=list, description="劣势")
    opportunities: List[SWOTItem] = Field(default_factory=list, description="机会")
    threats: List[SWOTItem] = Field(default_factory=list, description="威胁")
    strategic_implications: str = Field(..., description="基于 SWOT 分析的战略启示")

class BCGUnit(BaseModel):
    """BCG 矩阵中的单个业务单元"""
    name: str = Field(..., description="业务单元名称")
    relative_market_share: float = Field(..., description="相对市场份额 (0-1)")
    market_growth_rate: float = Field(..., description="市场增长率 (%)")
    quadrant: str = Field(..., description="所属象限 (Star, Cash Cow, Question Mark, Dog)")
    key_data_points: List[str] = Field(default_factory=list, description="支撑该业务单元判断的数据点")
    references: List[SourceReference] = Field(default_factory=list, description="支撑该业务单元判断的参考资料")

class BCGMatrixReport(BaseModel):
    """BCG 矩阵分析报告"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    title: str = Field("BCG 矩阵分析报告", description="报告标题")
    business_units: List[BCGUnit] = Field(default_factory=list, description="业务单元列表")
    strategic_recommendations: str = Field(..., description="基于 BCG 矩阵的战略建议")

class ERRCElement(BaseModel):
    """蓝海战略 ERRC 框架的单个元素"""
    action: str = Field(..., description="行动 (Eliminate, Reduce, Raise, Create)")
    element: str = Field(..., description="具体元素描述")

class BlueOceanStrategyReport(BaseModel):
    """蓝海战略分析报告"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    title: str = Field("蓝海战略分析报告", description="报告标题")
    current_value_curve_description: str = Field(..., description="当前行业价值曲线描述")
    errc_framework: List[ERRCElement] = Field(default_factory=list, description="ERRC 框架")
    new_value_proposition: str = Field(..., description="新的价值主张")
    strategic_implications: str = Field(..., description="蓝海战略的战略启示")

class FinalStrategicOutput(BaseModel):
    """最终战略分析输出 (V2)"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    pestel_report: StrategicReport = Field(..., description="PESTEL 宏观环境扫描报告")
    value_chain_report: StrategicReport = Field(..., description="行业价值链与利润池拆解报告")
    landscape_report: StrategicReport = Field(..., description="竞争格局与战略群组分析报告")
    swot_report: SWOTReport = Field(..., description="SWOT 深度分析报告")
    bcg_matrix_report: BCGMatrixReport = Field(..., description="BCG 矩阵分析报告")
    blue_ocean_report: BlueOceanStrategyReport = Field(..., description="蓝海战略分析报告")
    five_forces_report: StrategicReport = Field(..., description="波特五力深度推演终局报告")
    audit_report: Dict = Field(..., description="数据审计与事实清单")

# ============================================================================
# 核心 Crew 类
# ============================================================================

class StrategicCrew:
    """企业战略分析 Crew (V2 - 深度分析版)"""
    
    def __init__(self, api_provider: str = None, api_key: str = None):
        """
        初始化 StrategicCrew
        
        Args:
            api_provider: LLM 提供商 (\'groq\', \'gemini\', \'openai\')，默认读取环境变量
            api_key: API Key，默认读取环境变量
        """
        self.search_tool = SearchToolWrapper()
        
        # 从环境变量读取配置
        if api_provider is None:
            api_provider = os.getenv("LLM_PROVIDER", "groq")
        
        # 初始化 LLM
        if api_provider == "groq":
            api_key = api_key or os.getenv("GROQ_API_KEY")
            self.llm = ChatGroq(
                model_name="llama-3.1-70b-versatile",
                api_key=api_key,
                temperature=0.2
            )
        elif api_provider == "gemini":
            api_key = api_key or os.getenv("GOOGLE_API_KEY")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.2
            )
        else:  # openai
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.llm = ChatOpenAI(
                model_name="gpt-4.1-mini", # 使用更小的模型进行测试，生产环境可切换为 gpt-4
                api_key=api_key,
                temperature=0.2
            )

    def run(self, industry: str) -> Dict:
        """
        执行战略分析
        
        Args:
            industry: 行业名称，例如 "中国新能源汽车充电桩行业 - 面向个人用户的快充服务"
        
        Returns:
            包含所有报告的字典
        """
        
        # ====== 定义 Agent ======
        researcher = Agent(
            role=\'首席情报官\',
            goal=f\'为【{industry}】行业搜集最详实的白箱化数据事实，尤其关注市场份额、增长率、政策文件、财报数据、用户痛点和行业关键成功因素。\',
            backstory=\'你是一个数据极客，坚持"无数据不结论"。你负责为后续分析提供硬核支撑，能够从海量信息中精准提取量化数据和可信来源。\',
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        analyst = Agent(
            role=\'资深战略分析师\',
            goal=f\'基于情报事实，分阶段撰写PESTEL、价值链、竞争格局、SWOT、BCG和蓝海战略报告。\',
            backstory=\'你擅长将碎片化数据转化为结构化的战略洞察。你精通各种分析框架，能够识别数据背后的商业逻辑。\',
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        partner = Agent(
            role=\'管理合伙人\',
            goal=f\'整合所有分析，推导波特五力模型，并进行最终的数据审计和战略建议。\',
            backstory=\'你拥有20年顶级咨询经验，负责最后的逻辑闭环和质量把控，确保报告的商业价值和可操作性。\',
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # ====== 定义任务 ======
        # PESTEL 任务
        pestel_task = Task(
            description=(
                f"执行【{industry}】的PESTEL宏观环境分析。\n"
                "要求：\n"
                "1. 政治维度：列出最新的相关政策、法规变化，并评估其对行业的影响。\n"
                "2. 经济维度：分析宏观经济指标、行业增长率、消费能力，并评估其对行业的影响。\n"
                "3. 社会维度：分析消费者需求、人口趋势、文化价值观，并评估其对行业的影响。\n"
                "4. 技术维度：分析新兴技术、研发投入、技术成熟度，并评估其对行业的影响。\n"
                "5. 环境维度：分析环保政策、可持续发展因素、气候变化，并评估其对行业的影响。\n"
                "6. 法律维度：分析行业监管框架、知识产权保护，并评估其对行业的影响。\n"
                "每个维度至少包含一个具体数据或事实，并标注来源链接。"
            ),
            expected_output="PESTEL 深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=analyst,
            output_json=StrategicReport
        )

        # 价值链任务
        value_chain_task = Task(
            description=(
                f"执行【{industry}】的行业价值链分析。\n"
                "要求：\n"
                "1. 上游分析：原材料供应商、技术提供商，分析其议价能力和集中度。\n"
                "2. 中游分析：制造商、运营商、服务提供商，分析其核心竞争力、成本结构和利润空间。\n"
                "3. 下游分析：分销商、终端客户，分析其议价能力、渠道控制和客户忠诚度。\n"
                "4. 利润池分析：识别各环节的利润分配情况，找出利润最丰厚的环节。\n"
                "5. 价值捕获：分析谁在赚钱，为什么，以及价值如何从一个环节流向另一个环节。\n"
                "所有事实和数据必须标注来源。"
            ),
            expected_output="价值链深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=analyst,
            context=[pestel_task],
            output_json=StrategicReport
        )

        # 竞争格局任务
        landscape_task = Task(
            description=(
                f"执行【{industry}】的竞争格局分析。\n"
                "要求：\n"
                "1. 市场集中度：计算CR3或CR5（前三或前五名企业市场份额总和）或HHI指数，并说明数据来源。\n"
                "2. 主要竞争者：列出至少5个主要竞争者及其市场份额、核心产品、竞争策略和优劣势。\n"
                "3. 战略群组：分析行业内的战略群组，描述不同群组的竞争策略和市场定位。\n"
                "4. 竞争动态：分析行业内的并购、新进入者、退出者、技术创新等动态。\n"
                "所有事实和数据必须标注来源。"
            ),
            expected_output="竞争格局深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=analyst,
            context=[pestel_task, value_chain_task],
            output_json=StrategicReport
        )

        # SWOT 任务
        swot_task = Task(
            description=(
                f"基于PESTEL、价值链和竞争格局的分析结果，执行【{industry}】的SWOT深度分析。\n"
                "要求：\n"
                "1. 优势 (Strengths)：列出内部优势，并提供数据支撑。\n"
                "2. 劣势 (Weaknesses)：列出内部劣势，并提供数据支撑。\n"
                "3. 机会 (Opportunities)：列出外部机会，并提供数据支撑。\n"
                "4. 威胁 (Threats)：列出外部威胁，并提供数据支撑。\n"
                "每个SWOT条目必须有具体描述、支撑数据点和来源。\n"
                "最后给出基于SWOT分析的战略启示。"
            ),
            expected_output="SWOT 深度分析报告，包含标题、优势、劣势、机会、威胁列表和战略启示。",
            agent=analyst,
            context=[pestel_task, value_chain_task, landscape_task],
            output_json=SWOTReport
        )

        # BCG 矩阵任务
        bcg_task = Task(
            description=(
                f"基于【{industry}】的竞争格局和市场数据，执行BCG矩阵分析。\n"
                "要求：\n"
                "1. 识别至少3-5个主要业务单元或产品线。\n"
                "2. 为每个业务单元计算或估算其相对市场份额和市场增长率，并提供数据来源。\n"
                "3. 根据相对市场份额和市场增长率，判断每个业务单元所属的象限（明星、现金牛、问题、瘦狗）。\n"
                "4. 最后给出基于BCG矩阵的整体战略建议。"
            ),
            expected_output="BCG 矩阵分析报告，包含标题、业务单元列表、象限判断和战略建议。",
            agent=analyst,
            context=[landscape_task],
            output_json=BCGMatrixReport
        )

        # 蓝海战略任务
        blue_ocean_task = Task(
            description=(
                f"基于【{industry}】的价值链和竞争格局分析，执行蓝海战略分析。\n"
                "要求：\n"
                "1. 描述当前行业的普遍价值曲线，识别行业内普遍存在的竞争要素。\n"
                "2. 应用 ERRC 框架（剔除 Eliminate、减少 Reduce、增加 Raise、创造 Create），提出新的价值主张。\n"
                "3. 描述如何通过 ERRC 框架创造新的市场空间，实现价值创新。\n"
                "4. 最后给出蓝海战略的战略启示。"
            ),
            expected_output="蓝海战略分析报告，包含标题、当前价值曲线描述、ERRC 框架、新的价值主张和战略启示。",
            agent=analyst,
            context=[value_chain_task, landscape_task],
            output_json=BlueOceanStrategyReport
        )

        # 波特五力任务 (由 Partner Agent 完成)
        five_forces_task = Task(
            description=(
                f"基于PESTEL、价值链、竞争格局、SWOT、BCG和蓝海战略的分析结果，执行【{industry}】的波特五力深度推演。\n"
                "要求：\n"
                "1. 同业竞争强度：基于市场集中度、增长率、固定成本、退出壁垒等因素评分（1-10分），并提供数据支撑。\n"
                "2. 供应商议价能力：基于供应商集中度、转换成本、替代品威胁等因素评分（1-10分），并提供数据支撑。\n"
                "3. 买方议价能力：基于买方集中度、产品差异化、转换成本等因素评分（1-10分），并提供数据支撑。\n"
                "4. 替代品威胁：分析替代技术、替代产品的威胁程度、性价比，并提供数据支撑。\n"
                "5. 新进入者威胁：分析进入壁垒（资本、技术、政策）、规模经济，并提供数据支撑。\n"
                "每个力的评分必须有严密的逻辑推导和具体数据支撑。\n"
                "最后给出基于所有分析的综合战略建议。"
            ),
            expected_output="波特五力深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=partner,
            context=[pestel_task, value_chain_task, landscape_task, swot_task, bcg_task, blue_ocean_task],
            output_json=StrategicReport
        )

        # ====== 执行 Crew ======
        crew = Crew(
            agents=[researcher, analyst, partner],
            tasks=[
                pestel_task,
                value_chain_task,
                landscape_task,
                swot_task,
                bcg_task,
                blue_ocean_task,
                five_forces_task
            ],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff(inputs={\'industry\': industry})

        # ====== 解析结果 ======
        final_output = {}
        try:
            # CrewAI 1.x 版本直接返回 JSON 字符串，需要手动解析
            # CrewAI 2.x 版本可能直接返回 Pydantic 对象或字典
            if isinstance(result, str):
                # 尝试从文本中提取 JSON
                match = re.search(r\'\{.*\}\' , result, re.DOTALL)
                if match:
                    parsed_result = json.loads(match.group())
                else:
                    parsed_result = {"error": "无法解析 CrewAI 结果"}
            elif isinstance(result, dict):
                parsed_result = result
            else:
                # 假设是 Pydantic 对象，尝试转换为字典
                parsed_result = result.model_dump() if hasattr(result, 'model_dump') else result.dict()

            # 提取各个报告
            final_output["pestel_report"] = parsed_result.get("pestel_report", {})
            final_output["value_chain_report"] = parsed_result.get("value_chain_report", {})
            final_output["landscape_report"] = parsed_result.get("landscape_report", {})
            final_output["swot_report"] = parsed_result.get("swot_report", {})
            final_output["bcg_matrix_report"] = parsed_result.get("bcg_matrix_report", {})
            final_output["blue_ocean_report"] = parsed_result.get("blue_ocean_report", {})
            final_output["five_forces_report"] = parsed_result.get("five_forces_report", {})

        except Exception as e:
            print(f"Error parsing CrewAI result: {e}")
            final_output = {"error": str(e)}

        # ====== 注入数据审计信息 ======
        audit_dict = audit_log.to_dict()
        
        # 生成审计报告文本
        audit_report_content = f"""
# 数据审计与事实清单

## 审计摘要

- **总搜索次数**: {audit_dict["total_searches"]}
- **信息片段总数**: {audit_dict["total_snippets"]}
- **采纳硬数据个数**: {audit_dict["adopted_facts"]}
- **数据质量评分**: {audit_dict["data_quality_score"]} (采纳量/片段量)
- **独立数据源数**: {audit_dict["unique_sources"]}

## 阶段数据分布

"""
        for stage, stats in audit_dict["stage_breakdown"].items():
            audit_report_content += f"- **{stage}**: 搜索 {stats["searches"]} 次，采纳 {stats["facts"]} 条事实\n"

        audit_report_content += f"""

## 数据质量说明

数据质量评分反映了系统在信息采集、清洗、采纳过程中的效率。评分越高，说明系统能够从海量信息中精准提取出有价值的硬数据。

**评分解读**:
- 0.8-1.0: 优秀 - 信息利用率极高
- 0.6-0.8: 良好 - 信息利用率较高
- 0.4-0.6: 中等 - 信息利用率一般
- <0.4: 需改进 - 信息利用率较低

当前评分 **{audit_dict["data_quality_score"]}** 表明系统的数据处理能力处于 {"优秀" if audit_dict["data_quality_score"] >= 0.8 else "良好" if audit_dict["data_quality_score"] >= 0.6 else "中等"} 水平。

## 来源透明度

所有报告中引用的数据都附带了原文链接，用户可自行验证。详见各报告末尾的参考资料部分。
"""

        final_output["audit_report"] = {
            "title": "数据审计与事实清单",
            "content": audit_report_content,
            "statistics": audit_dict,
            "references": audit_log.sources # 将所有收集到的源都放入审计报告
        }

        return final_output
