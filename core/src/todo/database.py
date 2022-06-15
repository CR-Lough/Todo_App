"""This module provides the RP To-Do database functionality."""

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import sqlite3

from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.db"
)


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    conn = None
    try:
        conn = sqlite3.connect(db_path) # Empty to-do database
        conn.execute("""CREATE TABLE TASKS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         NAME TEXT NOT NULL,
         DESCRIPTION TEXT NOT NULL,
         START_DATE DATE,
         DUE_DATE DATE,
         PRIORITY INT,
         COMPLETE INT,
         DELETED INT);""")
        print('sqlite3.version') 
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
    finally:
        if conn:
            conn.close()


class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(todo_list, DB_WRITE_ERROR)