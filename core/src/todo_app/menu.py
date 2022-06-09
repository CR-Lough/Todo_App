'''
Provides a basic frontend
'''
import os
import sys

from sqlite_db import main
from peewee import *
from loguru import logger
from sqlite_db import socialnetwork_model
import pysnooper

logger.add("out_{time:YYYY.MM.DD}.log", backtrace=True, diagnose=True)

@pysnooper.snoop()
def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = 'accounts.csv'#input('Enter filename of user file: ')
    main.load_users(filename)

@pysnooper.snoop()
def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = 'status_updates.csv'#input('Enter filename for status file: ')
    main.load_statuses(filename)
   # main.load_statuses(filename)

@pysnooper.snoop()
def add_user():
    '''
    Adds a new user into the database
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    user_id = 'connor'#input('User ID: ')
    email = 'connor'#input('User email: ')
    user_name = 'connor'#input('User name: ')
    user_last_name = 'connor'#input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")

@pysnooper.snoop()
def update_user():
    '''
    Updates information for an existing user
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    user_id = 'connor'#input('User ID: ')
    email = 'connor'#input('User email: ')
    user_name = 'connor'#input('User name: ')
    user_last_name = 'connor'#input('User last name: ')
    # try:
    if not main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")
    # except TypeError:
    #   logger.exception("NEW EXCEPTION")
    #   pass

@pysnooper.snoop()
def search_user():
    '''
    Searches a user in the database
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    user_id = 'connor'#input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
 #   try:
    if not result:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Email: {result.user_email}")
        print(f"Name: {result.user_name}")
        print(f"Last name: {result.user_last_name}")
    # except AttributeError:
    #     logger.exception("NEW EXCEPTION")
    #     pass
@pysnooper.snoop()
def delete_user():
    '''
    Deletes user from the database
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    user_id = 'connor'#input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


@pysnooper.snoop()
def add_status():
    '''
    Adds a new status into the database
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    user_id = 'connor'#input('User ID: ')
    status_id = 'connor'#input('Status ID: ')
    status_text = 'connor'#input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")

@pysnooper.snoop()
def update_status():
    '''
    Updates information for an existing status
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    user_id = 'connor'#input('User ID: ')
    status_id = 'connor'#input('Status ID: ')
    status_text = 'connor'#input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")

@pysnooper.snoop()
def search_status():
    '''
    Searches a status in the database
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    status_id = 'connor'#input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if not result:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")

@pysnooper.snoop()
def delete_status():
    '''
    Deletes status from the database
    '''
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    status_id = 'connor'#input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")

@pysnooper.snoop()
def quit_program():
    '''
    Quits program
    '''
    sys.exit()

def setup():
    try:
        os.remove("twitter.db")
    except PermissionError:
        socialnetwork_model.db.close()
        os.remove("twitter.db")
    except FileNotFoundError:
        logger.info("twitter.db not detected. Creating new file in current directory")

    db = SqliteDatabase('twitter.db')
    db.connect()
    main.socialnetwork_model.create_tables(db)    

with logger.catch(message="Because we never know..."):
    if __name__ == '__main__':
        try:
            os.remove("twitter.db")
        except PermissionError:
            socialnetwork_model.db.close()
            os.remove("twitter.db")
        except FileNotFoundError:
            logger.info("twitter.db not detected. Creating new file in current directory")

        db = SqliteDatabase('twitter.db')
        db.connect()
        main.socialnetwork_model.create_tables(db)
        user_collection = main.init_user_collection()
        status_collection = main.init_status_collection()
        menu_options = {
            'A': load_users,
            'B': load_status_updates,
            'C': add_user,
            'D': update_user,
            'E': search_user,
            'F': delete_user,
            'G': add_status,
            'H': update_status,
            'I': search_status,
            'J': delete_status,
            'K': search_all_status_updates,
            'L': filter_status_by_string,
            'M': flagged_status_updates,
            'Q': quit_program
        }
        while True:
            user_selection = input("""
                                A: Load user database
                                B: Load status database
                                C: Add user
                                D: Update user
                                E: Search user
                                F: Delete user
                                G: Add status
                                H: Update status
                                I: Search status
                                J: Delete status
                                K: Search all status updates
                                L: Filter status by string
                                M: Flagged status updates
                                Q: Quit

                                Please enter your choice: """)
            if user_selection.upper() in menu_options:
                try:
                    menu_options[user_selection.upper()]()
                except KeyError:
                    logger.exception("NEW EXCEPTION")
            else:
                print("Invalid option")
