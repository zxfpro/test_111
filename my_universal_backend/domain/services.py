# my_universal_backend/domain/services.py
from my_universal_backend.common.interfaces import IDataRepository, IExternalService
from typing import Dict, List, Any
import time

# ▼▼▼ THIS IS A MODIFICATION / ADDITION (Class for Domain Services and Dependency Injection) ▼▼▼
class CoreDomainService:
    """
    核心领域服务：封装原子能力和业务规则。
    """
    def __init__(self, data_repo: IDataRepository, external_service: IExternalService):
        # 依赖注入：接收接口实例
        self._data_repo = data_repo
        self._external_service = external_service
        print("CoreDomainService: Initialized with injected dependencies.")

    # ▼▼▼ 这是一个“能力”：处理通用数据（例如，创建或更新数据项） ▼▼▼
    def process_generic_item(self, item_data: Dict) -> Dict:
        """处理一个通用数据项，进行业务逻辑和持久化。"""
        # 实际业务逻辑：例如，验证数据，添加时间戳等
        item_data["processed_at"] = int(time.time())
        print(f"CoreDomainService: Processing item {item_data.get('name')}.")
        saved_item = self._data_repo.save_data(item_data)
        return saved_item

    # ▼▼▼ 这是一个“能力”：获取特定类型的数据列表 ▼▼▼
    def retrieve_items_by_type(self, item_type: str) -> List[Dict]:
        """根据类型获取数据列表，并可能触发外部服务。"""
        # 实际业务逻辑：例如，查询数据库
        items = self._data_repo.find_data({"type": item_type})
        print(f"CoreDomainService: Retrieved {len(items)} items of type {item_type}.")
        
        # ▼▼▼ 这是一个“能力”的“虚假实现”示例 ▼▼▼
        # 假设这里有一个复杂的外部分析或通知逻辑
        if items:
            self._external_service.perform_action({"event": "items_retrieved", "count": len(items), "type": item_type})
        print("CoreDomainService: Simulating complex external interaction for data retrieval. (Placeholder)")
        # 真实实现可能会有更复杂的逻辑或调用多个外部API
        return items

    # ▼▼▼ 这是一个“能力”：执行一个关键业务动作并报告状态 ▼▼▼
    def execute_critical_business_action(self, action_payload: Dict) -> str:
        """执行一个关键业务动作，并返回其外部状态。"""
        print(f"CoreDomainService: Executing critical business action.")
        response = self._external_service.perform_action(action_payload)
        # 实际业务逻辑：例如，根据响应解析action_id，然后查询状态
        action_id = response.get("action_id", "mock_action_id")
        status = self._external_service.get_status(action_id)
        return status