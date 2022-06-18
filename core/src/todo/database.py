import configparser
from pathlib import Path
from flask import Flask
from flask_restful import Resource, Api
import sqlite3

from todo import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.cwd().joinpath(
    "." + Path.cwd().stem + "_todo.db"
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

class DatabaseHandler(Resource):
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path