'''
Classes for user information for the social network project
'''
# pylint: disable=R0903
from sqlite3 import IntegrityError
from sqlite_db import socialnetwork_model
from loguru import logger

logger.add("out_{time:YYYY.MM.DD}.log", backtrace=True, diagnose=True)

class UserCollection():
    '''
    Contains methods to interact with the UserTable in twitter.db
    '''
    @logger.catch(message="error in UserCollection __init__")
    def __init__(self):
        self.database = {}

    @logger.catch(message="error in UserCollection.add_user() method")
    def add_user(self, user_id:str, email:str, user_name:str, user_last_name:str):
        '''
        Adds a new user to the database
        '''
        try:
            new_user = socialnetwork_model.UsersTable(user_id=user_id, user_email=email,
                                                    user_name=user_name,
                                                    user_last_name=user_last_name)
            new_user.save()
            return True
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False

    @logger.catch(message="error in UserCollection.modify_user() method")
    def modify_user(self, user_id:str, email:str, user_name:str, user_last_name:str):
        '''
        Modifies an existing user
        '''
        try:
            row = socialnetwork_model.UsersTable.get(
                socialnetwork_model.UsersTable.user_id==user_id
            )
            row.user_email = email
            row.user_name = user_name
            row.user_last_name = user_last_name

            row.save()
            return True
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False

    @logger.catch(message="error in UserCollection.delete_user() method")
    def delete_user(self, user_id:str):
        '''
        Deletes an existing user
        '''
        try:
            row = socialnetwork_model.UsersTable.get(
                socialnetwork_model.UsersTable.user_id==user_id
            )
            row.delete_instance()
            return True
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False

    @logger.catch(message="error in UserCollection.search_user() method")
    def search_user(self, user_id:str):
        '''
        Searches for user data
        '''
        try:
            row = socialnetwork_model.UsersTable.get(
                socialnetwork_model.UsersTable.user_id==user_id
            )
            return row
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False
