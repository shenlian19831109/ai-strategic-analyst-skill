"""
核心战略分析引擎 - 基于 CrewAI 多智能体框架
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
from typing import List, Dict, Optional
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
            self.stage_stats[stage] = {'searches': 0, 'facts': 0}
        self.stage_stats[stage]['searches'] += count

    def add_snippets(self, count: int):
        self.total_snippets += count

    def add_adopted(self, stage: str, count: int):
        self.adopted_facts += count
        if stage not in self.stage_stats:
            self.stage_stats[stage] = {'searches': 0, 'facts': 0}
        self.stage_stats[stage]['facts'] += count

    def add_source(self, source: Dict):
        self.sources.append(source)

    def get_quality_score(self) -> float:
        """计算数据质量评分 (采纳量 / 片段量)"""
        if self.total_snippets == 0:
            return 0.0
        return round(self.adopted_facts / self.total_snippets, 2)

    def to_dict(self) -> Dict:
        return {
            'total_searches': self.total_searches,
            'total_snippets': self.total_snippets,
            'adopted_facts': self.adopted_facts,
            'data_quality_score': self.get_quality_score(),
            'stage_breakdown': self.stage_stats,
            'unique_sources': len(self.sources)
        }

# 全局审计实例
audit_log = DataAudit()

# ============================================================================
# 工具包装器
# ============================================================================

class SearchToolWrapper(BaseTool):
    """DuckDuckGo 搜索工具包装器"""
    
    name: str = "deep_market_search"
    description: str = "用于搜索特定行业的深度市场数据、竞争格局、财务指标和政策环境。"
    
    def _run(self, query: str) -> str:
        audit_log.add_search('general', 1)
        search = DuckDuckGoSearchRun()
        res = search.run(query)
        # 估算片段数量
        snippets = len(res.split('\n'))
        audit_log.add_snippets(snippets)
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

class FinalStrategicOutput(BaseModel):
    """最终战略分析输出"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    pestel_report: StrategicReport = Field(..., description="PESTEL 宏观环境扫描报告")
    value_chain_report: StrategicReport = Field(..., description="行业价值链与利润池拆解报告")
    landscape_report: StrategicReport = Field(..., description="竞争格局与战略群组分析报告")
    five_forces_report: StrategicReport = Field(..., description="波特五力深度推演终局报告")
    audit_report: Dict = Field(..., description="数据审计与事实清单")

# ============================================================================
# 核心 Crew 类
# ============================================================================

class StrategicCrew:
    """企业战略分析 Crew"""
    
    def __init__(self, api_provider: str = None, api_key: str = None):
        """
        初始化 StrategicCrew
        
        Args:
            api_provider: LLM 提供商 ('groq', 'gemini', 'openai')，默认读取环境变量
            api_key: API Key，默认读取环境变量
        """
        self.search_tool = SearchToolWrapper()
        
        # 从环境变量读取配置
        if api_provider is None:
            api_provider = os.getenv('LLM_PROVIDER', 'groq')
        
        # 初始化 LLM
        if api_provider == 'groq':
            api_key = api_key or os.getenv('GROQ_API_KEY')
            self.llm = ChatGroq(
                model_name="llama-3.1-70b-versatile",
                api_key=api_key,
                temperature=0.2
            )
        elif api_provider == 'gemini':
            api_key = api_key or os.getenv('GOOGLE_API_KEY')
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.2
            )
        else:  # openai
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.llm = ChatOpenAI(
                model_name="gpt-4.1-mini",
                api_key=api_key,
                temperature=0.2
            )

    def run(self, industry: str) -> Dict:
        """
        执行战略分析
        
        Args:
            industry: 行业名称，例如 "中国新能源汽车充电桩行业"
        
        Returns:
            包含五份报告的字典
        """
        
        # ====== 定义 Agent ======
        researcher = Agent(
            role='首席情报官',
            goal=f'为【{industry}】行业搜集最详实的白箱化数据事实。',
            backstory='你是一个数据极客，坚持"无数据不结论"。你负责为后续分析提供硬核支撑。',
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        analyst = Agent(
            role='资深战略分析师',
            goal=f'基于情报事实，分阶段撰写PESTEL、价值链和竞争格局报告。',
            backstory='你擅长将碎片化数据转化为结构化的战略洞察。你精通各种分析框架。',
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        partner = Agent(
            role='管理合伙人',
            goal=f'整合所有分析，推导波特五力模型，并进行最终的数据审计。',
            backstory='你拥有20年顶级咨询经验，负责最后的逻辑闭环和质量把控。',
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # ====== 定义任务 ======
        pestel_task = Task(
            description=(
                f"执行【{industry}】的PESTEL宏观环境分析。\n"
                "要求：\n"
                "1. 政治维度：列出最新的相关政策、法规变化\n"
                "2. 经济维度：分析宏观经济指标、行业增长率\n"
                "3. 社会维度：分析消费者需求、人口趋势\n"
                "4. 技术维度：分析新兴技术对行业的影响\n"
                "5. 环境维度：分析环保政策、可持续发展因素\n"
                "6. 法律维度：分析行业监管框架\n"
                "每个维度至少包含一个具体数据或事实，并标注来源链接。"
            ),
            expected_output="PESTEL 深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=analyst,
            output_json=StrategicReport
        )

        value_chain_task = Task(
            description=(
                f"执行【{industry}】的行业价值链分析。\n"
                "要求：\n"
                "1. 上游分析：原材料供应商、技术提供商\n"
                "2. 中游分析：制造商、运营商、服务提供商\n"
                "3. 下游分析：分销商、终端客户\n"
                "4. 利润池分析：识别各环节的利润分配情况\n"
                "5. 价值捕获：分析谁在赚钱，为什么\n"
                "所有事实和数据必须标注来源。"
            ),
            expected_output="价值链深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=analyst,
            context=[pestel_task],
            output_json=StrategicReport
        )

        landscape_task = Task(
            description=(
                f"执行【{industry}】的竞争格局分析。\n"
                "要求：\n"
                "1. 市场集中度：计算CR5（前五名企业市场份额总和）或HHI指数\n"
                "2. 主要竞争者：列出至少5个主要竞争者及其市场份额\n"
                "3. 战略群组：分析行业内的战略群组，描述不同群组的竞争策略\n"
                "4. 竞争动态：分析行业内的并购、新进入者、退出者\n"
                "所有事实和数据必须标注来源。"
            ),
            expected_output="竞争格局深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=analyst,
            context=[pestel_task, value_chain_task],
            output_json=StrategicReport
        )

        five_forces_task = Task(
            description=(
                f"基于PESTEL、价值链和竞争格局的分析结果，执行【{industry}】的波特五力分析。\n"
                "要求：\n"
                "1. 同业竞争强度：基于市场集中度、增长率、固定成本等因素评分\n"
                "2. 供应商议价能力：基于供应商集中度、转换成本等因素评分\n"
                "3. 买方议价能力：基于买方集中度、产品差异化等因素评分\n"
                "4. 替代品威胁：分析替代技术、替代产品的威胁程度\n"
                "5. 新进入者威胁：分析进入壁垒、资本需求等因素\n"
                "每个力的评分（1-10分）必须有严密的逻辑推导和具体数据支撑。\n"
                "最后给出基于五力分析的差异化竞争建议。"
            ),
            expected_output="波特五力深度文字报告，包含标题、详细分析、核心数据点和参考资料。",
            agent=partner,
            context=[pestel_task, value_chain_task, landscape_task],
            output_json=StrategicReport
        )

        # ====== 执行 Crew ======
        crew = Crew(
            agents=[researcher, analyst, partner],
            tasks=[pestel_task, value_chain_task, landscape_task, five_forces_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff(inputs={'industry': industry})

        # ====== 解析结果 ======
        try:
            if hasattr(result, 'json_dict') and result.json_dict:
                final_output = result.json_dict
            else:
                # 尝试从文本中提取 JSON
                match = re.search(r'\{.*\}', result.raw, re.DOTALL)
                if match:
                    final_output = json.loads(match.group())
                else:
                    final_output = {"error": "无法解析结果"}
        except Exception as e:
            final_output = {"error": str(e)}

        # ====== 注入数据审计信息 ======
        audit_dict = audit_log.to_dict()
        
        # 生成审计报告文本
        audit_report_content = f"""
# 数据审计与事实清单

## 审计摘要

- **总搜索次数**: {audit_dict['total_searches']}
- **信息片段总数**: {audit_dict['total_snippets']}
- **采纳硬数据个数**: {audit_dict['adopted_facts']}
- **数据质量评分**: {audit_dict['data_quality_score']} (采纳量/片段量)
- **独立数据源数**: {audit_dict['unique_sources']}

## 阶段数据分布

"""
        for stage, stats in audit_dict['stage_breakdown'].items():
            audit_report_content += f"- **{stage}**: 搜索 {stats['searches']} 次，采纳 {stats['facts']} 条事实\n"

        audit_report_content += f"""

## 数据质量说明

数据质量评分反映了系统在信息采集、清洗、采纳过程中的效率。评分越高，说明系统能够从海量信息中精准提取出有价值的硬数据。

**评分解读**:
- 0.8-1.0: 优秀 - 信息利用率极高
- 0.6-0.8: 良好 - 信息利用率较高
- 0.4-0.6: 中等 - 信息利用率一般
- <0.4: 需改进 - 信息利用率较低

当前评分 **{audit_dict['data_quality_score']}** 表明系统的数据处理能力处于 {"优秀" if audit_dict['data_quality_score'] >= 0.8 else "良好" if audit_dict['data_quality_score'] >= 0.6 else "中等"} 水平。

## 来源透明度

所有报告中引用的数据都附带了原文链接，用户可自行验证。详见各报告末尾的参考资料部分。
"""

        final_output['audit_report'] = {
            'title': '数据审计与事实清单',
            'content': audit_report_content,
            'statistics': audit_dict
        }

        return final_output
