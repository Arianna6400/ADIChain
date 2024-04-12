from db.db_operations import DatabaseOperations


class Controller:

    def __init__(self):
        self.db_ops = DatabaseOperations()


    def registration(self, username: str, password: str, role: str, public_key: str, private_key: str):
        registration_code = self.db_ops.register(username, password, role, public_key, private_key)

        if registration_code == 0:
           print("Done") 
        
        return registration_code

    