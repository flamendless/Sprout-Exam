from pydantic import BaseModel

from src.db import new_conn


def tuple_to_pydantic(pydantic_class: BaseModel, data: tuple) -> BaseModel:
    return pydantic_class(
        **{
            k: v
            for k, v in zip(pydantic_class.__fields__.keys(), data)
        }
    )


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
