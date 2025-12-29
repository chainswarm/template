"""
Base repository pattern for database operations.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseRepository(ABC):
    """
    Abstract base class for repository pattern.
    
    Provides common database operation patterns that can be implemented
    for specific databases (PostgreSQL, ClickHouse, MongoDB, etc.).
    """
    
    def __init__(self, client: Any, table_name: str):
        """
        Initialize repository.
        
        Args:
            client: Database client instance
            table_name: Name of the table/collection
        """
        self.client = client
        self.table_name = table_name
    
    @abstractmethod
    def insert(self, data: Dict[str, Any]) -> None:
        """Insert a single record."""
        pass
    
    @abstractmethod
    def insert_many(self, records: List[Dict[str, Any]]) -> None:
        """Insert multiple records."""
        pass
    
    @abstractmethod
    def get_by_id(self, record_id: Any) -> Optional[Dict[str, Any]]:
        """Get a record by ID."""
        pass
    
    @abstractmethod
    def query(self, conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query records matching conditions."""
        pass
    
    @abstractmethod
    def update(self, record_id: Any, data: Dict[str, Any]) -> None:
        """Update a record."""
        pass
    
    @abstractmethod
    def delete(self, record_id: Any) -> None:
        """Delete a record."""
        pass
    
    @abstractmethod
    def count(self, conditions: Optional[Dict[str, Any]] = None) -> int:
        """Count records matching conditions."""
        pass
    
    @abstractmethod
    def exists(self, record_id: Any) -> bool:
        """Check if record exists."""
        pass


class ClickHouseRepository(BaseRepository):
    """
    Example ClickHouse repository implementation.
    
    This is a template showing how to implement the base repository
    for ClickHouse. Adapt as needed for your use case.
    """
    
    def insert(self, data: Dict[str, Any]) -> None:
        """Insert a single record into ClickHouse."""
        query = f"INSERT INTO {self.table_name} (*) VALUES"
        self.client.execute(query, [data])
    
    def insert_many(self, records: List[Dict[str, Any]]) -> None:
        """Insert multiple records into ClickHouse."""
        if not records:
            return
        query = f"INSERT INTO {self.table_name} (*) VALUES"
        self.client.execute(query, records)
    
    def get_by_id(self, record_id: Any) -> Optional[Dict[str, Any]]:
        """Get record by ID from ClickHouse."""
        query = f"SELECT * FROM {self.table_name} WHERE id = %(id)s LIMIT 1"
        result = self.client.execute(query, {"id": record_id})
        return result[0] if result else None
    
    def query(self, conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query records from ClickHouse."""
        where_clause = " AND ".join([f"{k} = %({k})s" for k in conditions.keys()])
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause}"
        return self.client.execute(query, conditions)
    
    def update(self, record_id: Any, data: Dict[str, Any]) -> None:
        """
        Note: ClickHouse doesn't support traditional UPDATE.
        You typically insert new versions or use ALTER TABLE UPDATE.
        """
        raise NotImplementedError("ClickHouse doesn't support UPDATE. Use versioning or ALTER TABLE.")
    
    def delete(self, record_id: Any) -> None:
        """
        Note: ClickHouse doesn't support traditional DELETE.
        You typically use ALTER TABLE DELETE or mark as deleted.
        """
        raise NotImplementedError("ClickHouse doesn't support DELETE. Use ALTER TABLE or soft delete.")
    
    def count(self, conditions: Optional[Dict[str, Any]] = None) -> int:
        """Count records in ClickHouse."""
        if conditions:
            where_clause = " AND ".join([f"{k} = %({k})s" for k in conditions.keys()])
            query = f"SELECT count() FROM {self.table_name} WHERE {where_clause}"
            result = self.client.execute(query, conditions)
        else:
            query = f"SELECT count() FROM {self.table_name}"
            result = self.client.execute(query)
        return result[0][0] if result else 0
    
    def exists(self, record_id: Any) -> bool:
        """Check if record exists in ClickHouse."""
        query = f"SELECT 1 FROM {self.table_name} WHERE id = %(id)s LIMIT 1"
        result = self.client.execute(query, {"id": record_id})
        return len(result) > 0
