from datetime import date, timedelta, datetime
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Tuple
from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify
import sqlite3

from todo.database import DatabaseHandler

def to_date(s):
    return datetime.strptime(s, '%Y-%m-%d')

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class Todoer(Resource):
    def __init__(self, db_path: Path) -> None:
       self._db_handler = DatabaseHandler(db_path)
       
    def add(self, name: str, description: str, start_date:str = None, due_date:str = None, priority: int = 2, complete: int = 0, deleted: int = 0) -> dict:
        """Add a new to-do to the database.

        :param name: task name
        :type name: str
        :param description: task description
        :type description: str
        :param start_date: start date of the task, defaults to None
        :type start_date: str, optional
        :param due_date: due date of the task, defaults to None
        :type due_date: str, optional
        :param priority: priority level of the task,1-3, defaults to 2
        :type priority: int, optional
        :param complete: boolean for complete task, defaults to 0
        :type complete: int, optional
        :param deleted: boolean for deleted task, defaults to 0
        :type deleted: int, optional
        :return: returns the values last input to the database
        :rtype: dict
        """
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
    
    def get_todo_list(self, method:str, start:str, end:str, api:int) -> List[tuple]:
        """Get different types of to-do lists from the database

        :param method: type of to-do list
        :type method: str
        :param start: optional, start date to search 
        :type start: str
        :param end: optional, end date to search 
        :type end: str
        :return: returns the database rows as a list of tuples
        :rtype: list of tuples
        """
        # app = Flask(__name__)
        # with app.app_context():
        keys = ('ID','NAME','DESCRIPTION','TEXT','START_DATE','DUE_DATE',
                'PRIORITY','COMPLETE','DELETED')
        conn = sqlite3.connect("C:/Users/Connor/.Connor_todo.db")
        print("Opened database successfully")
        if method == "task_number":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                ORDER BY ID ASC
            """)
            if api==1:
                result = {"data": [dict(zip(tuple(keys), i))
                    for i in cursor]}
                return jsonify(result)
            else:
                result = [row for row in cursor]
                result = iter(result)
                return result
        elif method == "priority":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                ORDER BY PRIORITY DESC
            """) 
            if api==1:
                result = {"data": [dict(zip(tuple(keys), i))
                    for i in cursor]}
                return jsonify(result)
            else:
                result = [row for row in cursor]
                result = iter(result)
                return result
        elif method == "due_date":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                ORDER BY DUE_DATE DESC
            """)
            if api==1:
                result = {"data": [dict(zip(tuple(keys), i))
                    for i in cursor]}
                return jsonify(result)
            else:
                result = [row for row in cursor]
                result = iter(result)
                return result
        elif method == "closed_range":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                WHERE DUE_DATE BETWEEN '{to_date(start)}' AND '{to_date(end)}'
            """)
            if api==1:
                result = {"data": [dict(zip(tuple(keys), i))
                    for i in cursor]}
                return jsonify(result)
            else:
                result = [row for row in cursor]
                result = iter(result)
                return result
        elif method == "overdue":
            cursor = conn.execute(f"""
                SELECT *
                FROM TASKS 
                WHERE DATE(DUE_DATE) < {(datetime.now()).date()}
            """)
            if api==1:
                result = {"data": [dict(zip(tuple(keys), i))
                    for i in cursor]}
                return jsonify(result)
            else:
                result = [row for row in cursor]
                result = iter(result)
                return result
        else: 
            print('not an option')
            
    def set_done(self, todo_id: int) -> None:
        """Set a to-do as done 

        :param todo_id: to-do ID
        :type todo_id: str
        :return: None
        :rtype: None
        """
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        conn.execute(f"UPDATE TASKS set COMPLETE = 1 where ID = {todo_id}")
        conn.commit()
        conn.close()

    def rename(self, todo_id: int, new_name: str) -> None:
        """Rename a to-do
        
        :param todo_id: to-do ID
        :type todo_id: str
        :param new_name: new task name
        :type new_name: str
        :return: None
        :rtype: None
        """
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        conn.execute(f"UPDATE TASKS set NAME = '{new_name}' where ID = {todo_id}")
        conn.commit()
        conn.close()

    def redescribe(self, todo_id: int, new_description: str) -> None:
        """Update a description for a to-do
        
        :param todo_id: to-do ID
        :type todo_id: str
        :param new_description: new task description
        :type new_description: str
        :return: None
        :rtype: None
        """
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        conn.execute(f"UPDATE TASKS set DESCRIPTION = '{new_description}' where ID = {todo_id}")
        conn.commit()
        conn.close()

    def remove(self, todo_id: int) -> None:
        """Remove a to-do from the database using its id
        
        :param todo_id: to-do ID
        :type todo_id: str
        :return: None
        :rtype: None
        """
        conn = sqlite3.connect(f"{self._db_handler._db_path}")
        print("Opened database successfully")
        conn.execute(f"UPDATE TASKS set DELETED = 1 where ID = {todo_id};")
        conn.commit()
        conn.close()