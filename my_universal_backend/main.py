# my_universal_backend/main.py
from my_universal_backend.infrastructure.adapters.adapter_factory import AdapterFactory, AdapterType
from my_universal_backend.domain.services import CoreDomainService
from my_universal_backend.core import CoreAPI
from typing import Literal

# ▼▼▼ THIS IS A MODIFICATION / ADDITION (Main assembly logic) ▼▼▼
def initialize_application(env: Literal["dev", "prod"] = "dev"):
    """
    初始化应用程序，根据环境组装依赖并初始化CoreAPI。
    """
    print(f"\n--- Initializing Application in '{env}' environment ---")

    data_repo_type = AdapterType.MOCK if env == "dev" else AdapterType.REAL
    external_service_type = AdapterType.MOCK if env == "dev" else AdapterType.REAL

    # 1. 组装基础设施层适配器 (能力实现)
    # 使用工厂模式创建具体适配器
    data_repository = AdapterFactory.new_data_repository(
        type=data_repo_type,
        connection_string="mongodb://localhost:27017/my_db" if env == "prod" else "mock_db_connection"
    )
    external_service = AdapterFactory.new_external_service(
        type=external_service_type,
        api_key="PROD_API_KEY_123" if env == "prod" else "mock_api_key"
    )

    # 2. 组装领域服务 (注入能力接口实现)
    # 遵循依赖注入原则，将适配器注入到领域服务中
    domain_service = CoreDomainService(
        data_repo=data_repository,
        external_service=external_service
    )

    # 3. 初始化 CoreAPI (将流程层与领域层连接)
    # CoreAPI是单例，确保只初始化一次
    CoreAPI(domain_service=domain_service) # 第一次调用会创建实例并注入依赖
    print("--- Application Initialization Complete ---\n")

def get_core_api_instance() -> CoreAPI:
    """
    获取已初始化CoreAPI的单例实例，供其他模块调用。
    """
    return CoreAPI.get_instance()

# 示例：作为Python包被调用时的入口
if __name__ == "__main__":
    # 作为主程序运行的示例
    print("Running as main application...")

    # 在开发模式下初始化应用程序
    initialize_application(env="dev")
    core_api = get_core_api_instance()

    # 示例调用一个流程
    print("\n--- CoreAPI Flow Call Example (Dev Mode) ---")
    result = core_api.process_general_request({"name": "Test Item A", "type": "product"})
    print(f"Flow Result: {result}")

    result_items = core_api.retrieve_all_items_of_type("product")
    print(f"Retrieved Items: {result_items}")

    # 切换到生产模式重新初始化 (通常在实际部署时只做一次)
    print("\n--- Re-initializing in 'prod' mode ---")
    initialize_application(env="prod")
    core_api_prod = get_core_api_instance() # 此时获取的是prod配置的实例

    print("\n--- CoreAPI Flow Call Example (Prod Mode) ---")
    result_prod = core_api_prod.process_general_request({"name": "Real Item X", "type": "service"})
    print(f"Flow Result (Prod): {result_prod}")