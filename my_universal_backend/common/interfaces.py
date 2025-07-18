# my_universal_backend/common/interfaces.py
from abc import ABC, abstractmethod
from typing import Any, List, Dict

# ▼▼▼ THIS IS A MODIFICATION / ADDITION BASED ON YOUR TEMPLATE (abc usage) ▼▼▼
class IDataRepository(ABC):
    """
    数据仓储接口：定义数据持久化的能力。
    """
    @abstractmethod
    def save_data(self, data: Dict) -> Dict:
        """保存数据，返回保存后的数据（可能包含ID）"""
        pass

    @abstractmethod
    def get_data_by_id(self, item_id: str) -> Dict | None:
        """根据ID获取数据"""
        pass

    @abstractmethod
    def find_data(self, query: Dict) -> List[Dict]:
        """根据查询条件查找数据列表"""
        pass

# ▼▼▼ THIS IS A MODIFICATION / ADDITION BASED ON YOUR TEMPLATE (abc usage) ▼▼▼
class IExternalService(ABC):
    """
    外部服务接口：定义与外部系统交互的能力（如发送通知、调用第三方API）。
    """
    @abstractmethod
    def perform_action(self, payload: Dict) -> Dict:
        """执行一个外部动作"""
        pass

    @abstractmethod
    def get_status(self, action_id: str) -> str:
        """获取外部动作状态"""
        pass