# my_universal_backend/infrastructure/adapters/data_repository.py
from my_universal_backend.common.interfaces import IDataRepository
from typing import Dict, List, Any
import uuid

# ▼▼▼ THIS IS A MODIFICATION / ADDITION BASED ON YOUR TEMPLATE (Adapter pattern implementation) ▼▼▼
class MockDataRepository(IDataRepository):
    """
    IDataRepository 的 Mock 实现，使用内存字典模拟数据库。
    """
    def __init__(self):
        self._data_store: Dict[str, Dict] = {}
        print("MockDataRepository: Initialized (in-memory store).")

    def save_data(self, data: Dict) -> Dict:
        item_id = data.get("id") or str(uuid.uuid4())
        data["id"] = item_id
        self._data_store[item_id] = data
        print(f"MockDataRepository: Saved data with ID {item_id}")
        return data

    def get_data_by_id(self, item_id: str) -> Dict | None:
        print(f"MockDataRepository: Getting data for ID {item_id}")
        return self._data_store.get(item_id)

    def find_data(self, query: Dict) -> List[Dict]:
        print(f"MockDataRepository: Finding data with query {query}")
        results = [d for d in self._data_store.values() if all(d.get(k) == v for k, v in query.items())]
        return results

# ▼▼▼ THIS IS A MODIFICATION / ADDITION BASED ON YOUR TEMPLATE (Adapter pattern implementation) ▼▼▼
class RealDataRepository(IDataRepository):
    """
    IDataRepository 的真实实现占位符（例如，这里会连接到数据库）。
    """
    def __init__(self, connection_string: str = "default_db_conn"):
        self._connection_string = connection_string
        # 实际项目中，这里会建立数据库连接
        print(f"RealDataRepository: Initialized with connection {connection_string}. (Placeholder)")

    def save_data(self, data: Dict) -> Dict:
        # 实际项目中，这里会执行数据库插入/更新操作
        print(f"RealDataRepository: Saving data to DB. (Placeholder)")
        return data # 返回模拟数据

    def get_data_by_id(self, item_id: str) -> Dict | None:
        # 实际项目中，这里会执行数据库查询操作
        print(f"RealDataRepository: Getting data from DB for ID {item_id}. (Placeholder)")
        return {"id": item_id, "name": "RealData", "status": "retrieved"}

    def find_data(self, query: Dict) -> List[Dict]:
        # 实际项目中，这里会执行数据库查询操作
        print(f"RealDataRepository: Finding data from DB with query {query}. (Placeholder)")
        return [{"id": "real_1", "name": "Item1"}, {"id": "real_2", "name": "Item2"}]