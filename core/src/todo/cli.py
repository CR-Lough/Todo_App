from pathlib import Path
from typing import List, Optional
import sqlite3
from datetime import date, timedelta, datetime

import typer

from todo import ERRORS, __app_name__, __version__, config, database, todo

app = typer.Typer()

def to_date(s):
    return datetime.strptime(s, '%Y-%m-%d')

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the to-do database

    :param db_path: _description_, defaults to typer.Option( str(database.DEFAULT_DB_FILE_PATH), "--db-path", "-db", prompt="to-do database location?", )
    :type db_path: str, optional
    :raises typer.Exit: config directory error
    :raises typer.Exit: config directory error
    """
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)


def get_todoer() -> todo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return todo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def add(
    name: str = typer.Argument(...),
    description: str = typer.Argument(...),
    start_date: str = typer.Option(str((datetime.now()).date()), "--startdate", "-sd"),
    due_date: str = typer.Option(str((datetime.now()).date()), "--duedate", "-dd"),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
    complete: int = typer.Option(0, "--complete", "-c", min=0, max=1),
    deleted: int = typer.Option(0, "--deleted", "-d", min=0, max=1)
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    todoer = get_todoer()
    todo = todoer.add(name, description, start_date, due_date, priority, complete, deleted)
    return todo

@app.command(name="list")
def list_all(
    method: str = typer.Argument(...),
    start: str = typer.Option('', "--start", "-s"),
    end: str = typer.Option('', "--end", "-e")
) -> None:
    """List all to-dos."""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list(method,start,end)
    if not todo_list:
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Name         ",
        "| Description                ",
        "| Start Date         ",
        "| Due Date           ",
        "| Priority  ",
        "| Done  ",
        "| Deleted  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for todo in todo_list:
        id,name,desc,sd,dd,pr,done,deleted = list(todo)
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {name}{(len(columns[1]) - len(str(name)) - 2) * ' '}"
            f"| {desc}{(len(columns[2]) - len(str(desc)) - 2) * ' '}"
            f"| {sd}{(len(columns[3]) - len(str(sd)) - 2) * ' '}"
            f"| {dd}{(len(columns[4]) - len(str(dd)) - 2) * ' '}"
            f"| {pr}{(len(columns[5]) - len(str(pr)) - 2) * ' '}"
            f"| {done}{(len(columns[6]) - len(str(done)) - 2) * ' '}"
            f"| {deleted}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


@app.command(name="complete")
def set_done(todo_id: int = typer.Argument(...)) -> None:
    """Complete a to-do by setting it as done using its TODO_ID."""
    todoer = get_todoer()
    todo = todoer.set_done(todo_id)
    typer.secho(
        f"""to-do # {todo_id} completed!""",
        fg=typer.colors.GREEN,
    )

@app.command(name="rename")
def rename_task(
    todo_id: int = typer.Argument(...),
    new_name: str = typer.Argument(...)
) -> None:
    """Rename a to-do by giving its ID"""
    todoer = get_todoer()
    todo = todoer.rename(todo_id, new_name)
    typer.secho(
        f"""to-do # {todo_id} renamed to "{new_name}"!""",
        fg=typer.colors.GREEN,
    )

@app.command(name="redescribe")
def redescribe(
    todo_id: int = typer.Argument(...),
    new_description: str = typer.Argument(...)
) -> None:
    """Redescribe a to-do by giving its ID"""
    todoer = get_todoer()
    todo = todoer.redescribe(todo_id, new_description)
    typer.secho(
        f"""to-do # {todo_id} redescribed to "{new_description}"!""",
        fg=typer.colors.GREEN,
    )

@app.command()
def remove(
    todo_id: int = typer.Argument(...)
) -> None:
    """Remove a to-do using its TODO_ID."""
    todoer = get_todoer()

    def _remove():
        todo = todoer.remove(todo_id)
        typer.secho(
            f"""to-do # {todo_id}' was removed""",
            fg=typer.colors.GREEN,
        )

    delete = typer.confirm(
        f"Delete to-do # {todo_id}?"
    )
    if delete:
        _remove()
    else:
        typer.echo("Operation canceled")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return