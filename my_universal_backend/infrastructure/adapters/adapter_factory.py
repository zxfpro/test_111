# my_universal_backend/infrastructure/adapters/adapter_factory.py
from enum import Enum
from typing import Any
# ▼▼▼ THIS IS A MODIFICATION / ADDITION (Import interfaces and concrete adapters) ▼▼▼
from my_universal_backend.common.interfaces import IDataRepository, IExternalService
from my_universal_backend.infrastructure.adapters.data_repository import MockDataRepository, RealDataRepository
from my_universal_backend.infrastructure.adapters.external_service import MockExternalService, RealExternalService

# ▼▼▼ THIS IS A MODIFICATION / ADDITION (Using your provided Enum template structure) ▼▼▼
class AdapterType(Enum):
    MOCK = 'MOCK'
    REAL = 'REAL'
    # 添加更多选项，例如针对不同云服务商的类型

# ▼▼▼ YOUR FACTORY TEMPLATE IS USED HERE ▼▼▼
class AdapterFactory:
    """
    工厂模式：根据类型创建适配器实例。
    """
    @classmethod # 使用classmethod以便直接通过类调用，无需实例化工厂
    def new_data_repository(cls, type: AdapterType, **kwargs) -> IDataRepository: # type hint to interface
        assert type.value in [i.value for i in AdapterType]
        instance = None

        if type.value == AdapterType.MOCK.value:
            instance = MockDataRepository()
            print("AdapterFactory: Creating MockDataRepository.")
        elif type.value == AdapterType.REAL.value:
            instance = RealDataRepository(**kwargs) # 允许传入连接字符串等参数
            print(f"AdapterFactory: Creating RealDataRepository with kwargs: {kwargs}.")
        else:
            raise Exception(f"Unknown AdapterType for DataRepository: {type.value}")
        return instance

    @classmethod # 针对不同类型的适配器，工厂中可以有不同的new方法
    def new_external_service(cls, type: AdapterType, **kwargs) -> IExternalService: # type hint to interface
        assert type.value in [i.value for i in AdapterType]
        instance = None

        if type.value == AdapterType.MOCK.value:
            instance = MockExternalService()
            print("AdapterFactory: Creating MockExternalService.")
        elif type.value == AdapterType.REAL.value:
            instance = RealExternalService(**kwargs) # 允许传入API Key等参数
            print(f"AdapterFactory: Creating RealExternalService with kwargs: {kwargs}.")
        else:
            raise Exception(f"Unknown AdapterType for ExternalService: {type.value}")
        return instance