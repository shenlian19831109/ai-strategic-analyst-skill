"""
AI 企业战略分析助手 - 使用示例
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.strategic_crew import StrategicCrew

def main():
    """主函数 - 运行战略分析示例"""
    
    print("=" * 100)
    print("AI 企业战略分析助手 - 使用示例")
    print("=" * 100)
    print()
    
    # 初始化 Crew（会自动从 .env 读取 LLM_PROVIDER）
    print("正在初始化战略分析引擎...")
    crew = StrategicCrew()
    print("✓ 初始化完成")
    print()
    
    # 定义分析行业
    industry = "中国新能源汽车充电桩行业 - 面向个人用户的快充服务"
    
    print(f"正在分析行业：{industry}")
    print("这可能需要 2-5 分钟，请耐心等待...")
    print()
    
    # 执行分析
    result = crew.run(industry=industry)
    
    # ========== 输出 PESTEL 报告 ==========
    print("=" * 100)
    print("📊 PESTEL 宏观环境扫描报告")
    print("=" * 100)
    print()
    
    pestel = result.get('pestel_report', {})
    if isinstance(pestel, dict):
        print(f"标题: {pestel.get('title', 'N/A')}")
        print()
        print(pestel.get('content', 'N/A'))
        print()
        
        if pestel.get('key_data_points'):
            print("核心数据点:")
            for point in pestel['key_data_points']:
                print(f"  • {point}")
        print()
        
        if pestel.get('references'):
            print("参考资料:")
            for ref in pestel['references']:
                print(f"  • {ref.get('description', 'N/A')}")
                if ref.get('url'):
                    print(f"    链接: {ref['url']}")
    print()
    
    # ========== 输出价值链报告 ==========
    print("=" * 100)
    print("🔗 行业价值链与利润池拆解报告")
    print("=" * 100)
    print()
    
    value_chain = result.get('value_chain_report', {})
    if isinstance(value_chain, dict):
        print(f"标题: {value_chain.get('title', 'N/A')}")
        print()
        print(value_chain.get('content', 'N/A'))
        print()
        
        if value_chain.get('key_data_points'):
            print("核心数据点:")
            for point in value_chain['key_data_points']:
                print(f"  • {point}")
        print()
        
        if value_chain.get('references'):
            print("参考资料:")
            for ref in value_chain['references']:
                print(f"  • {ref.get('description', 'N/A')}")
                if ref.get('url'):
                    print(f"    链接: {ref['url']}")
    print()
    
    # ========== 输出竞争格局报告 ==========
    print("=" * 100)
    print("⚔️ 竞争格局与战略群组分析报告")
    print("=" * 100)
    print()
    
    landscape = result.get('landscape_report', {})
    if isinstance(landscape, dict):
        print(f"标题: {landscape.get('title', 'N/A')}")
        print()
        print(landscape.get('content', 'N/A'))
        print()
        
        if landscape.get('key_data_points'):
            print("核心数据点:")
            for point in landscape['key_data_points']:
                print(f"  • {point}")
        print()
        
        if landscape.get('references'):
            print("参考资料:")
            for ref in landscape['references']:
                print(f"  • {ref.get('description', 'N/A')}")
                if ref.get('url'):
                    print(f"    链接: {ref['url']}")
    print()
    
    # ========== 输出波特五力报告 ==========
    print("=" * 100)
    print("💪 波特五力深度推演终局报告")
    print("=" * 100)
    print()
    
    five_forces = result.get('five_forces_report', {})
    if isinstance(five_forces, dict):
        print(f"标题: {five_forces.get('title', 'N/A')}")
        print()
        print(five_forces.get('content', 'N/A'))
        print()
        
        if five_forces.get('key_data_points'):
            print("核心数据点:")
            for point in five_forces['key_data_points']:
                print(f"  • {point}")
        print()
        
        if five_forces.get('references'):
            print("参考资料:")
            for ref in five_forces['references']:
                print(f"  • {ref.get('description', 'N/A')}")
                if ref.get('url'):
                    print(f"    链接: {ref['url']}")
    print()
    
    # ========== 输出数据审计报告 ==========
    print("=" * 100)
    print("🔍 数据审计与事实清单")
    print("=" * 100)
    print()
    
    audit = result.get('audit_report', {})
    if isinstance(audit, dict):
        print(f"标题: {audit.get('title', 'N/A')}")
        print()
        print(audit.get('content', 'N/A'))
        print()
        
        if audit.get('statistics'):
            stats = audit['statistics']
            print("审计统计:")
            print(f"  • 总搜索次数: {stats.get('total_searches', 'N/A')}")
            print(f"  • 信息片段总数: {stats.get('total_snippets', 'N/A')}")
            print(f"  • 采纳硬数据个数: {stats.get('adopted_facts', 'N/A')}")
            print(f"  • 数据质量评分: {stats.get('data_quality_score', 'N/A')}")
            print(f"  • 独立数据源数: {stats.get('unique_sources', 'N/A')}")
    print()
    
    print("=" * 100)
    print("✓ 分析完成！")
    print("=" * 100)

if __name__ == "__main__":
    main()
