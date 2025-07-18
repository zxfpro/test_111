# test_111/mock.py
from typing import Any, Dict, List

# ▼▼▼ MODIFICATION / ADDITION: Mock implementations of capabilities ▼▼▼
class MockDataReaderImpl: # 不直接继承接口，因为这里只是一个具体的实现，通过工厂注入
    def __init__(self):
        print("MockDataReaderImpl: Initialized (returns dummy CSV data).")

    def read_csv(self, source: str) -> List[Dict]:
        """模拟读取CSV数据，返回固定假数据。"""
        print(f"MockDataReaderImpl: Mock reading CSV from {source}.")
        return [
            {"id": "mock_1", "value": 10, "category": "X"},
            {"id": "mock_2", "value": 20, "category": "Y"},
            {"id": "mock_3", "value": 30, "category": "X"},
        ]

class MockDataAnalyzerImpl:
    def __init__(self):
        print("MockDataAnalyzerImpl: Initialized (returns dummy analysis).")

    def analyze_column_stats(self, data: List[Dict], column_name: str) -> Dict[str, Any]:
        """模拟分析指定列的统计数据，返回固定假结果。"""
        print(f"MockDataAnalyzerImpl: Mock analyzing column '{column_name}'.")
        return {"sum": 60, "avg": 20, "count": 3, "mocked": True} # 对应上面假数据10+20+30=60

class MockReportGeneratorImpl:
    def __init__(self):
        print("MockReportGeneratorImpl: Initialized (generates dummy report).")

    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """模拟生成报告，返回固定假报告字符串。"""
        print(f"MockReportGeneratorImpl: Mock generating report for {analysis_results}.")
        return "--- MOCK REPORT ---\nSum: 60\nAvg: 20\n-------------------"