from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    BEARER = "bearer"
    REFRESH = "refresh"


class EmployeeType(str, Enum):
    ADMIN = "admin"
    REGULAR = "regular"
    CONTRACTUAL = "contractual"


class AuditAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
