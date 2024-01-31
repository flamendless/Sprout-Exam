from enum import Enum
from functools import cache
from typing import Any

from pydantic import BaseModel

from src.db import new_conn


def tuple_to_pydantic(pydantic_class: BaseModel, data: tuple) -> BaseModel:
    return pydantic_class(
        **{
            k: v
            for k, v in zip(pydantic_class.__fields__.keys(), data)
        }
    )


@cache
def is_value_in_enum(enum_class: Enum, value: Any) -> bool:
    for e in enum_class:
        if e.value == value:
            return True
    return False


def get_filter_clause(filter_data: dict) -> str:
    sql = "WHERE\n"
    wheres: list[str] = [
        f"{k} = ?"
        for k in filter_data.keys()
    ]
    sql += " AND ".join(wheres)
    sql += "\n"
    return sql


def get_update_clause(update_data: dict) -> str:
    sql = "\nSET\n"
    updates: list[str] = [
        f"{k} = ?"
        for k in update_data.keys()
    ]
    sql += ", ".join(updates)
    sql += "\n"
    return sql


def create_audit(data: tuple) -> None:
    conn = new_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tbl_audit(
            auditor_id,
            table_name,
            action,
            message,
            created_at
        )
        VALUES(?, ?, ?, ?, ?)
    """, data)
    conn.commit()
