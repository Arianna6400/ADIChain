from db.db_operations import DatabaseOperations
#from session.session import Session


class Controller:

    def __init__(self):
        self.db_ops = DatabaseOperations()
        #self.session = session
        self.__n_attempts_limit = 5
        self.__timeout_timer = 180        


    def registration(self, username: str, password: str, role: str, public_key: str, private_key: str):
        registration_code = self.db_ops.register(username, password, role, public_key, private_key)

        if registration_code == 0:
           print("Done") 
        
        return registration_code

    