'''
classes to manage the user status messages
'''
# pylint: disable=R0903
from sqlite3 import IntegrityError
from sqlite_db import socialnetwork_model
from sqlalchemy import create_engine
from loguru import logger

logger.add("out_{time:YYYY.MM.DD}.log", backtrace=True, diagnose=True)

class UserStatusCollection():
    '''
    Contains methods to interact with the StatusTable in twitter.db
    '''
    @logger.catch(message="error in UserStatusCollection __init__")
    def __init__(self):
        self.database = {}

    @logger.catch(message="error in UserStatusCollection.add_status() method")
    def add_status(self, status_id:str, user_id:str, status_text:str):
        '''
        add a new status message to the database
        '''
        try:
            new_status = socialnetwork_model.StatusTable(status_id=status_id, user_id=user_id,
                                status_text=status_text)
            new_status.save()
            return True
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False

    @logger.catch(message="error in UserStatusCollection.modify_status() method")
    def modify_status(self, status_id:str, user_id:str, status_text:str):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        try:
            row = socialnetwork_model.StatusTable.get(socialnetwork_model.StatusTable.user_id==status_id)
            row.user_id = user_id
            row.status_text = status_text

            row.save()
            return True
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False

    @logger.catch(message="error in UserStatusCollection.delete_status() method")
    def delete_status(self, status_id:str):
        '''
        deletes the status message with id, status_id
        '''
        try:
            qry = socialnetwork_model.StatusTable.delete().where (socialnetwork_model.StatusTable.status_id==status_id)
            qry.execute()
            # query = (socialnetwork_model.StatusTable
            #         .select(socialnetwork_model.StatusTable.status_id)
            #         .join(socialnetwork_model.UsersTable)
            #         .where(socialnetwork_model.StatusTable.status_id == status_id))
            # # for row in query:
            # #     temp_status_id = row.status_id
            # # temp_status_id.delete_instance()

            # socialnetwork_model.StatusTable.delete().where(socialnetwork_model.StatusTable.status_id << query)
            return True
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False

    @logger.catch(message="error in UserStatusCollection.search_status() method")
    def search_status(self, status_id:str):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        try:
            #row = socialnetwork_model.StatusTable.get(socialnetwork_model.StatusTable.user_id==status_id)
            query = (socialnetwork_model.StatusTable
                    .select(socialnetwork_model.StatusTable.user_id,
                            socialnetwork_model.StatusTable.status_id,
                            socialnetwork_model.StatusTable.status_text        
                    )
                    .join(socialnetwork_model.UsersTable)
                    .where(socialnetwork_model.StatusTable.status_id == status_id))
            for row in query:
                return row
            # return status
        except IntegrityError:
            logger.exception("NEW EXCEPTION")
            return False

    def search_all_status_updates(self, user_id):
        engine = create_engine("sqlite:///twitter.db", echo=True)
        with engine.connect() as sqlite_connection:
            execute = sqlite_connection.execute(f"""
                SELECT status_text 
                FROM statustable 
                WHERE user_id in ('{user_id}')
            """)
            result = sorted([row[0] for row in execute])
        return result

    def filter_status_by_string(self, status_string):
        engine = create_engine("sqlite:///twitter.db", echo=True)
        with engine.connect() as sqlite_connection:
            execute = sqlite_connection.execute(f"""
                SELECT STATUS_ID,USER_ID,STATUS_TEXT 
                FROM statustable 
                WHERE status_text like '%{status_string}%'
            """)
            result = sorted([row for row in execute])
            result = iter(result)
        return result
