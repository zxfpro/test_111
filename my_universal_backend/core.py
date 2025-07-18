# my_universal_backend/core.py
from my_universal_backend.domain.services import CoreDomainService
from typing import Dict, List, Any

# ▼▼▼ THIS IS A MODIFICATION / ADDITION (CoreAPI class as the public interface) ▼▼▼
class CoreAPI:
    """
    核心API：对外提供所有业务流程的统一入口。
    通过此API，可以像Python包一样调用业务功能。
    """
    _instance: 'CoreAPI' = None # 单例模式，确保只有一个CoreAPI实例
    _domain_service: CoreDomainService = None

    def __new__(cls, domain_service: CoreDomainService = None):
        if cls._instance is None:
            if domain_service is None:
                raise ValueError("CoreAPI must be initialized with a CoreDomainService instance on first creation.")
            cls._instance = super(CoreAPI, cls).__new__(cls)
            cls._domain_service = domain_service
            print("CoreAPI: Instance created and initialized.")
        elif domain_service is not None and cls._domain_service is not domain_service:
            # 允许在调试/测试时重新初始化，或者在确保安全的情况下更新依赖
            print("CoreAPI: Re-initializing with new CoreDomainService instance. (Warning: Usually done only once)")
            cls._domain_service = domain_service
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'CoreAPI':
        """获取CoreAPI的单例实例。"""
        if cls._instance is None:
            raise RuntimeError("CoreAPI has not been initialized. Call CoreAPI(domain_service_instance) first.")
        return cls._instance

    # ▼▼▼ 这是一个“流程”：处理一个通用请求，包含多个能力 ▼▼▼
    def process_general_request(self, request_payload: Dict) -> Dict:
        """
        处理一个通用的业务请求。
        这是一个高层次的“流程”，它编排底层原子能力。
        """
        print(f"CoreAPI (Process Flow): Starting general request processing for {request_payload.get('name')}.")
        # 流程步骤1：调用能力处理请求数据
        processed_data = self._domain_service.process_generic_item(request_payload)

        # 流程步骤2：根据请求类型，调用不同的能力进行进一步处理
        if processed_data.get("type") == "special_query":
            retrieved_items = self._domain_service.retrieve_items_by_type(processed_data["type"])
            processed_data["retrieved_items_count"] = len(retrieved_items)
            print("CoreAPI (Process Flow): Handled special query type.")
        
        # 流程步骤3：执行一个关键业务动作
        status = self._domain_service.execute_critical_business_action({"trigger": processed_data.get("id")})
        processed_data["critical_action_status"] = status
        print("CoreAPI (Process Flow): Completed general request processing.")
        return processed_data

    # ▼▼▼ 这是一个“流程”：获取所有特定类型的数据 ▼▼▼
    def retrieve_all_items_of_type(self, item_type: str) -> List[Dict]:
        """
        获取所有特定类型的数据。
        这是一个相对简单的“流程”，直接调用一个核心能力。
        """
        print(f"CoreAPI (Process Flow): Retrieving all items of type {item_type}.")
        items = self._domain_service.retrieve_items_by_type(item_type)
        print("CoreAPI (Process Flow): Finished retrieving items.")
        return items
    
    # ▼▼▼ 这是一个“流程”：触发外部关键动作（直接调用原子能力） ▼▼▼
    def trigger_external_critical_action(self, action_payload: Dict) -> str:
        """
        触发一个关键的外部动作，并返回其状态。
        """
        print("CoreAPI (Process Flow): Triggering external critical action.")
        status = self._domain_service.execute_critical_business_action(action_payload)
        return status