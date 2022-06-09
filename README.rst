.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/todo_app.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/todo_app
    .. image:: https://readthedocs.org/projects/todo_app/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://todo_app.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/todo_app/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/todo_app
    .. image:: https://img.shields.io/pypi/v/todo_app.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/todo_app/
    .. image:: https://img.shields.io/conda/vn/conda-forge/todo_app.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/todo_app
    .. image:: https://pepy.tech/badge/todo_app/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/todo_app
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/todo_app

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

========
todo_app
========


    Python to-do application for personal use. It will keep track of tasks and report upon them.


Part 1
The app will be driven by the command line. Thus, you will use simple terminal IO (input and print) as a user interface for now. It will support the following commands:

add new task
list tasks
set a start date for the task
set a due date for the task
mark the task as completed
delete a task
change task name
change task description
All tasks will be stored in a database. You can use sqlite, mongodb, or any other database of your choice.

The following data is kept for each task:

Task number (not editable after adding)
Task name
Task descrption
Task start date
Task due date
Task priority
Task name and task description are mandatory when adding a new task. All other fields are optional, and can be added via the command line.

The task app must produce the following lists:

List all tasks sorted by task number
List all tasks sorted by priority
List all open tasks sorted by due date
List all closed tasks between specified dates
List all overdue tasks
All lists must be correctly formatted for display in a terminal.

You should develop extensive automated tests as part of building this system.

Part 2 (after week 9 lesson):
Build an API to the task app, using curl to enter commands, and returning the results as json structures.

Your application must be built so that you can either use the terminal or curl interface.

More news on part 2 in weeks 8 & 9

 

Here is what you need to do:

Use pyscaffold to develop a robust project structure. Use a virtual environment and git.

Use automated testing to validate the system behaves as intended.
Develop the data capture functionality.
Make sure the data is validated, so data entry errors can be prevented as much as possible.
Ensure each task has a unique id.
Make use of formatting techniques to ensure that information reported to the screen is well laid out and easy to understand.
Be sure task is stored in the database. "Deleted" tasks are not to be removed; rather, they are marked as deleted.
Be sure to commit to local git frequently and use a virtual environment.



.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.1.4. For details and usage
information on PyScaffold see https://pyscaffold.org/.
