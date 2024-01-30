from datetime import datetime

from pydantic import BaseModel

from src.enums import AuditAction


class AuditDB(BaseModel):
    id: int
    auditor_id: int
    table_name: str
    action: AuditAction
    created_at: datetime
