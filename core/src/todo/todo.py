"""This module provides the RP To-Do model-controller."""
from datetime import date, timedelta, datetime
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Tuple
import sqlite3
from sqlalchemy import create_engine

from todo import DB_READ_ERROR, ID_ERROR
import todo
from todo.database import DatabaseHandler

def to_date(s):
    return datetime.strptime(s, '%Y-%m-%d')

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, name: str, description: str, start_date:str = None, due_date:str = None, priority: int = 2, complete: int = 0, deleted: int = 0) -> CurrentTodo:
        """Add a new to-do to the database."""
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        print("Opened database successfully")
        query = ('INSERT INTO TASKS (NAME,DESCRIPTION,START_DATE,DUE_DATE,PRIORITY,COMPLETE,DELETED) '
            'VALUES (:NAME, :DESCRIPTION, :START_DATE, :DUE_DATE, :PRIORITY, :COMPLETE, :DELETED );')
        
        params = {
            'NAME': name,
            'DESCRIPTION': description,
            'START_DATE': to_date(start_date), 
            'DUE_DATE': to_date(due_date),
            'PRIORITY': priority,
            'COMPLETE': complete,
            'DELETED': deleted 
        }
        conn.execute(query, params)
        conn.commit()
        print("Records created successfully")
        conn.close()

        return params

    def get_todo_list(self, method:str, start:str, end:str) -> List[Tuple[str, Any]]:
        """Return the current to-do list."""
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        print("Opened database successfully")
        if method is "task_number":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                ORDER BY ID ASC
            """)
            result = sorted([row for row in cursor])
            result = iter(result)
            return result
        if method is "priority":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                ORDER BY PRIORITY DESC
            """)
            result = sorted([row for row in cursor])
            result = iter(result)
            return result
        if method is "due_date":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                ORDER BY DUE_DATE DESC
            """)
            result = sorted([row for row in cursor])
            result = iter(result)
            return result
        if method is "closed_range":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                WHERE DATE(DUE_DATE) BETWEEN {to_date(start)} AND {to_date(end)}
            """)
            result = sorted([row for row in cursor])
            result = iter(result)
            return result
        if method is "overdue":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                WHERE DATE(DUE_DATE) < {to_date(date.today())}
            """)
            result = sorted([row for row in cursor])
            result = iter(result)
            return result
    def set_done(self, todo_id: int) -> CurrentTodo:
        """Set a to-do as done."""
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        conn.execute(f"UPDATE TASKS set COMPELTE = 1 where ID = {todo_id}")
        conn.commit()
        conn.close()

    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a to-do from the database using its id or index."""
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        conn.execute(f"DELETE from TASKS where ID = {todo_id};")
        conn.commit()
        conn.close()

    def remove_all(self) -> CurrentTodo:
        """Remove all to-dos from the database."""
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)