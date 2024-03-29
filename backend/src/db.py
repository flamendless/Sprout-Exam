import logging
import sqlite3

from datetime import UTC, datetime
from sqlite3 import Connection

from src.const import DB_NAME
from src.context import pwd
from src.enums import EmployeeType

logger = logging.getLogger(__name__)


def _get_db():
    return sqlite3.connect(DB_NAME)


def new_conn() -> Connection:
    return _get_db()


def setup_db() -> None:
    conn = new_conn()
    cur = conn.cursor()
    logger.info("Setting up database...")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        tbl_benefit(
            id          INTEGER PRIMARY KEY,
            name        TEXT UNIQUE,
            description TEXT,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        tbl_project(
            id          INTEGER PRIMARY KEY,
            name        TEXT UNIQUE,
            description TEXT,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        tbl_employee(
            id                INTEGER PRIMARY KEY,
            email             TEXT NOT NULL UNIQUE,
            password          TEXT NOT NULL,
            first_name        TEXT NOT NULL,
            last_name         TEXT NOT NULL,
            type              TEXT CHECK( type IN ('regular', 'contractual', 'admin') ),
            number_of_leaves  INTEGER,
            contract_end_date TEXT,
            created_at        TEXT NOT NULL,
            updated_at        TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        tbl_employee_benefit(
            id          INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            benefit_id  INTEGER NOT NULL,
            UNIQUE(employee_id, benefit_id) ON CONFLICT IGNORE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        tbl_employee_project(
            id          INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            project_id  INTEGER NOT NULL,
            UNIQUE(employee_id, project_id) ON CONFLICT IGNORE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        tbl_audit(
            id         INTEGER PRIMARY KEY,
            auditor_id INTEGER NOT NULL,
            table_name TEXT NOT NULL,
            action     TEXT CHECK( action IN ('create', 'read', 'update', 'delete') ),
            message    TEXT,
            created_at TEXT NOT NULL
        );
    """)

    create_admin()
    create_index()


def create_admin() -> None:
    conn = new_conn()
    cur = conn.cursor()
    res = cur.execute(
        "SELECT id FROM tbl_employee WHERE type = ?;",
        (EmployeeType.ADMIN.value,),
    )
    res: tuple[int | None, ...] = res.fetchone()
    if res is None:
        logger.info("Creating admin account...")
        data: tuple = (
            "admin@admin.com",
            pwd.hash("admin"),
            "admin",
            "admin",
            EmployeeType.ADMIN.value,
            datetime.now(tz=UTC),
            datetime.now(tz=UTC),
        )
        cur.execute("""
            INSERT INTO tbl_employee(
                email,
                password,
                first_name,
                last_name,
                type,
                created_at,
                updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()


def create_index() -> None:
    logger.info("Creating db index...")
    conn = new_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE INDEX IF NOT EXISTS
        "tbl_employee_idx_type" ON "tbl_employee" (
            "type"	ASC
        );
    """)
    conn.commit()
