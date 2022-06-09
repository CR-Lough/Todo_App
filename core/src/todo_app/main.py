'''
main driver for a simple social network project
'''
import time
from sqlite_db import users
from sqlite_db import user_status
from sqlite_db import socialnetwork_model
import pandas as pd
from loguru import logger

logger.add("out_{time:YYYY.MM.DD}.log", backtrace=True, diagnose=True)
def init_user_collection():
    '''
    Creates and returns a new instance of UserCollection
    '''
    user = users.UserCollection()
    return user


def init_status_collection():
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    status = user_status.UserStatusCollection()
    return status

def load_users(filename: str):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    try:
        load_dict = (pd.read_csv(filename)).to_dict(orient='records')
        for row in load_dict:
            new_user=socialnetwork_model.UsersTable(user_id=row['USER_ID'], user_name=row['NAME'],
                                    user_last_name=row['LASTNAME'], user_email=row['EMAIL'])
            new_user.save()
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"SQLite ran 'load_users()' in {run_time:.4f} secs")
        return load_dict
    except FileNotFoundError:
        logger.exception("NEW EXCEPTION")
        return False

def load_statuses(filename: str):
    '''
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    try:
        load_dict = pd.read_csv(filename)
        load_dict.columns = load_dict.columns.str.lower()
        load_dict = load_dict.to_dict(orient='records')

        with socialnetwork_model.db.atomic():
            for idx in range(0, len(load_dict), 100):
                socialnetwork_model.StatusTable.insert_many(load_dict[idx:idx+100]).execute()
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"SQLite ran 'load_statuses()' in {run_time:.4f} secs")
        return load_dict
    except FileNotFoundError:
        logger.exception("NEW EXCEPTION")
        return False

def add_user(user_id:str, email:str, user_name:str, user_last_name:str, user_collection:object):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    new_user = user_collection.add_user(user_id,email,user_name,user_last_name)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'add_user()' in {run_time:.4f} secs")   
    return new_user


def update_user(user_id:str, email:str, user_name:str, user_last_name:str, user_collection:object):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    updated_user = user_collection.modify_user(user_id, email, user_name, user_last_name)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'update_user()' in {run_time:.4f} secs")      
    return updated_user


def delete_user(user_id: str, user_collection: object):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    purge_id = user_collection.delete_user(user_id)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'delete_user()' in {run_time:.4f} secs")   
    return purge_id

def search_user(user_id: str, user_collection: object):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    start_time = time.perf_counter()
    find_user = user_collection.search_user(user_id)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'search_user()' in {run_time:.4f} secs")   
    return find_user


def add_status(user_id: str, status_id: str, status_text: str, status_collection: object):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    new_status = status_collection.add_status(user_id, status_id, status_text)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'add_status()' in {run_time:.4f} secs")       
    return new_status


def update_status(status_id: str, user_id: str, status_text: str, status_collection: object):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    modify_status = status_collection.modify_status(user_id, status_id, status_text)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'update_status()' in {run_time:.4f} secs")       
    return modify_status


def delete_status(status_id: str, status_collection: object):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    start_time = time.perf_counter()
    purge_id = status_collection.delete_status(status_id)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'delete_status()' in {run_time:.4f} secs")    
    return purge_id


def search_status(status_id: str, status_collection: object):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    # query = (socialnetwork_model.StatusTable
    #      .select(socialnetwork_model.StatusTable)
    #      .where(socialnetwork_model.StatusTable.status_id == status_id))
    start_time = time.perf_counter()
    find_status = status_collection.search_status(status_id)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    logger.info(f"SQLite ran 'search_status()' in {run_time:.4f} secs")       
    return find_status