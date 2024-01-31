from src.enums import AuditAction
from src.models.base import DB


class AuditDB(DB):
    auditor_id: int
    table_name: str
    action: AuditAction
    updated_at: None = None
