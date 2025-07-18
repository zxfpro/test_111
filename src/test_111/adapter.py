# 做适配器的文件

# test_111/adapter.py
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, TextIO
from src.test_111.funs import RealDataReaderImpl, RealDataAnalyzerImpl, RealReportGeneratorImpl
from src.test_111.mock import MockDataReader, MockDataAnalyzer, MockReportGenerator

# --- 1. 定义接口 (Interfaces / Ports) ---
# ▼▼▼ MODIFICATION / ADDITION: New interfaces for CSV analysis capabilities ▼▼▼
class IDataReader(ABC):
    """
    数据读取器接口：定义从源读取数据的能力。
    """
    @abstractmethod
    def read_csv(self, source: str) -> List[Dict]:
        """从指定源读取CSV数据并返回字典列表。"""
        pass

class IDataAnalyzer(ABC):
    """
    数据分析器接口：定义对数据进行统计分析的能力。
    """
    @abstractmethod
    def analyze_column_stats(self, data: List[Dict], column_name: str) -> Any: # 返回IAnalysisStrategy
        """分析指定列的统计数据（例如：总和、平均值）。"""
        pass

class IReportGenerator(ABC):
    """
    报告生成器接口：定义根据分析结果生成报告的能力。
    """
    @abstractmethod
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """根据分析结果生成可读的报告字符串。"""
        pass

# --- 2. AdapterType 枚举 (用于工厂模式) ---
class AdapterType(Enum):
    MOCK = 'MOCK'
    REAL = 'REAL'

# --- 3. 适配器工厂 (AdapterFactory) ---
# ▼▼▼ YOUR FACTORY TEMPLATE IS USED HERE (Adapted to our needs) ▼▼▼
class AdapterFactory:
    @classmethod
    def new_data_reader(cls, type: AdapterType, **kwargs) -> IDataReader:
        if type == AdapterType.MOCK:
            return MockDataReader()
        elif type == AdapterType.REAL:
            return RealDataReader()
        else:
            raise ValueError(f"Unknown AdapterType for IDataReader: {type}")

    @classmethod
    def new_data_analyzer(cls, type: AdapterType, **kwargs) -> IDataAnalyzer:
        if type == AdapterType.MOCK:
            return MockDataAnalyzer()
        elif type == AdapterType.REAL:
            return RealDataAnalyzer()
        else:
            raise ValueError(f"Unknown AdapterType for IDataAnalyzer: {type}")

    @classmethod
    def new_report_generator(cls, type: AdapterType, **kwargs) -> IReportGenerator:
        if type == AdapterType.MOCK:
            return MockReportGenerator()
        elif type == AdapterType.REAL:
            return RealReportGenerator()
        else:
            raise ValueError(f"Unknown AdapterType for IReportGenerator: {type}")

# --- 4. 适配器具体实现 (Mock & Real) ---
# Real 适配器 (继承自funs.py中的实现)
class RealDataReader(IDataReader, RealDataReaderImpl):
    def __init__(self):
        super().__init__()

from src.test_111.core import IAnalysisStrategy # 导入IAnalysisStrategy

class RealDataAnalyzer(IDataAnalyzer):
    def __init__(self):
        # RealDataAnalyzerImpl 实际上就是我们需要的分析策略
        self._strategy = RealDataAnalyzerImpl()

    def analyze_column_stats(self, data: List[Dict], column_name: str) -> IAnalysisStrategy:
        # 这里不再执行分析，而是返回一个IAnalysisStrategy的实例
        return self._strategy

class MockDataAnalyzer(IDataAnalyzer):
    def __init__(self):
        # MockDataAnalyzerImpl 实际上就是我们需要的分析策略
        self._strategy = MockDataAnalyzerImpl()

    def analyze_column_stats(self, data: List[Dict], column_name: str) -> IAnalysisStrategy:
        # 这里不再执行分析，而是返回一个IAnalysisStrategy的实例
        return self._strategy

class RealReportGenerator(IReportGenerator, RealReportGeneratorImpl):
    def __init__(self):
        super().__init__()