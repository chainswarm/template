"""
Database utility functions.
"""
import re
from typing import Any, Dict, List


def sanitize_identifier(identifier: str) -> str:
    """
    Sanitize database identifier (table name, column name).
    
    Removes any characters that could be used for SQL injection.
    
    Args:
        identifier: The identifier to sanitize
    
    Returns:
        Sanitized identifier
    
    Raises:
        ValueError: If identifier contains invalid characters
    """
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
        raise ValueError(
            f"Invalid identifier '{identifier}'. "
            "Must start with letter or underscore and contain only letters, numbers, and underscores."
        )
    return identifier


def build_insert_query(table_name: str, data: Dict[str, Any], dialect: str = "clickhouse") -> str:
    """
    Build INSERT query for different SQL dialects.
    
    Args:
        table_name: Name of the table
        data: Dictionary of column -> value
        dialect: SQL dialect ("clickhouse", "postgres", "mysql")
    
    Returns:
        INSERT query string
    
    Example:
        >>> data = {"id": 1, "name": "test"}
        >>> build_insert_query("users", data)
        "INSERT INTO users (id, name) VALUES (%(id)s, %(name)s)"
    """
    sanitize_identifier(table_name)
    columns = ", ".join([sanitize_identifier(col) for col in data.keys()])
    
    if dialect == "clickhouse":
        # ClickHouse uses %(name)s placeholders
        values = ", ".join([f"%({col})s" for col in data.keys()])
    elif dialect in ("postgres", "postgresql"):
        # PostgreSQL uses %s placeholders
        values = ", ".join(["%s" for _ in data.keys()])
    elif dialect == "mysql":
        # MySQL uses %s placeholders
        values = ", ".join(["%s" for _ in data.keys()])
    else:
        raise ValueError(f"Unsupported dialect: {dialect}")
    
    return f"INSERT INTO {table_name} ({columns}) VALUES ({values})"


def build_select_query(
    table_name: str,
    columns: List[str],
    where: Dict[str, Any],
    limit: int = None,
    order_by: str = None,
    dialect: str = "clickhouse"
) -> str:
    """
    Build SELECT query.
    
    Args:
        table_name: Name of the table
        columns: List of columns to select
        where: WHERE conditions
        limit: Optional LIMIT
        order_by: Optional ORDER BY column
        dialect: SQL dialect
    
    Returns:
        SELECT query string
    """
    sanitize_identifier(table_name)
    
    if columns:
        cols = ", ".join([sanitize_identifier(col) for col in columns])
    else:
        cols = "*"
    
    query = f"SELECT {cols} FROM {table_name}"
    
    if where:
        conditions = []
        for col in where.keys():
            sanitize_identifier(col)
            if dialect == "clickhouse":
                conditions.append(f"{col} = %({col})s")
            else:
                conditions.append(f"{col} = %s")
        query += " WHERE " + " AND ".join(conditions)
    
    if order_by:
        sanitize_identifier(order_by)
        query += f" ORDER BY {order_by}"
    
    if limit:
        query += f" LIMIT {int(limit)}"
    
    return query


def build_batch_insert(table_name: str, records: List[Dict[str, Any]], dialect: str = "clickhouse") -> tuple:
    """
    Build batch INSERT for multiple records.
    
    Args:
        table_name: Name of the table
        records: List of record dictionaries
        dialect: SQL dialect
    
    Returns:
        Tuple of (query, parameters)
    
    Example:
        >>> records = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        >>> query, params = build_batch_insert("users", records)
    """
    if not records:
        return ("", [])
    
    sanitize_identifier(table_name)
    
    # All records should have the same columns
    columns = list(records[0].keys())
    for col in columns:
        sanitize_identifier(col)
    
    cols_str = ", ".join(columns)
    
    if dialect == "clickhouse":
        # ClickHouse can insert multiple dicts directly
        query = f"INSERT INTO {table_name} ({cols_str}) VALUES"
        return (query, records)
    else:
        # PostgreSQL/MySQL need placeholder values
        placeholders = ", ".join(["%s" for _ in columns])
        query = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"
        params = [[record[col] for col in columns] for record in records]
        return (query, params)
