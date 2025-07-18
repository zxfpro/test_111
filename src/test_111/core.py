# 编写核心使用代码的部分

# test_111/funs.py
from typing import Any, Dict, List
from abc import ABC, abstractmethod
from src.test_111.adapter import IDataReader, IDataAnalyzer, IReportGenerator, AdapterFactory, AdapterType

# 定义分析策略接口
class IAnalysisStrategy(ABC):
    """
    分析策略接口：定义不同的数据分析算法。
    """
    @abstractmethod
    def analyze(self, data: List[Dict], column_name: str) -> Dict[str, Any]:
        """执行具体的分析算法。"""
        pass

# 这里应该只包含设计模式相关的内容，而不包含具体的逻辑实现
# 具体的逻辑实现都应该从adapter导入
# 例如，你可以定义一个使用这些接口的Facade或者Service类
class CSVProcessor:
    def __init__(self, data_reader: IDataReader, data_analyzer: IDataAnalyzer, report_generator: IReportGenerator):
        self.data_reader = data_reader
        self.data_analyzer = data_analyzer
        self.report_generator = report_generator

    def process_csv_data(self, source: str, column_name: str) -> str:
        data = self.data_reader.read_csv(source)
        # 从data_analyzer获取IAnalysisStrategy的实例
        analysis_strategy: IAnalysisStrategy = self.data_analyzer.analyze_column_stats(data, column_name)
        analysis_results = analysis_strategy.analyze(data, column_name)
        report = self.report_generator.generate_report(analysis_results)
        return report

# 示例如何使用AdapterFactory来获取具体的实现
def get_real_csv_processor():
    reader = AdapterFactory.new_data_reader(AdapterType.REAL)
    analyzer = AdapterFactory.new_data_analyzer(AdapterType.REAL)
    generator = AdapterFactory.new_report_generator(AdapterType.REAL)
    return CSVProcessor(reader, analyzer, generator)

def get_mock_csv_processor():
    reader = AdapterFactory.new_data_reader(AdapterType.MOCK)
    analyzer = AdapterFactory.new_data_analyzer(AdapterType.MOCK)
    generator = AdapterFactory.new_report_generator(AdapterType.MOCK)
    return CSVProcessor(reader, analyzer, generator)