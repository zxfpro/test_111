# my_universal_backend/infrastructure/adapters/external_service.py
from my_universal_backend.common.interfaces import IExternalService
from typing import Dict, Any

# ▼▼▼ THIS IS A MODIFICATION / ADDITION BASED ON YOUR TEMPLATE (Adapter pattern implementation) ▼▼▼
class MockExternalService(IExternalService):
    """
    IExternalService 的 Mock 实现，模拟外部服务行为。
    """
    def __init__(self):
        print("MockExternalService: Initialized (simulating external calls).")

    def perform_action(self, payload: Dict) -> Dict:
        print(f"MockExternalService: Simulating action with payload {payload}. (Success)")
        return {"status": "mock_success", "payload_echo": payload}

    def get_status(self, action_id: str) -> str:
        print(f"MockExternalService: Simulating status for action ID {action_id}. (Completed)")
        return "mock_completed"

# ▼▼▼ THIS IS A MODIFICATION / ADDITION BASED ON YOUR TEMPLATE (Adapter pattern implementation) ▼▼▼
class RealExternalService(IExternalService):
    """
    IExternalService 的真实实现占位符（例如，这里会调用真实的第三方API）。
    """
    def __init__(self, api_key: str = "default_api_key"):
        self._api_key = api_key
        # 实际项目中，这里会配置API客户端
        print(f"RealExternalService: Initialized with API Key {api_key}. (Placeholder)")

    def perform_action(self, payload: Dict) -> Dict:
        # 实际项目中，这里会发起真实的HTTP请求
        print(f"RealExternalService: Performing real action with payload {payload}. (Placeholder)")
        return {"status": "real_success", "api_response": "...", "payload_echo": payload}

    def get_status(self, action_id: str) -> str:
        # 实际项目中，这里会查询真实API状态
        print(f"RealExternalService: Getting real status for action ID {action_id}. (Placeholder)")
        return "real_completed"