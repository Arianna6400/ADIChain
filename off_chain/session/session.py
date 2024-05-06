import time

class Session:

    def __init__(self):
        self.__user = None
        self.__attempts = 0
        self.__login_error_timestamp = 0

    def get_user(self):        
        return self.__user
    

    def set_user(self, user):
        self.__user = user


    def get_attempts(self):
        return self.__attempts
    
    def increment_attempts(self):
        self.__attempts += 1

    def reset_attempts(self):
        self.__attempts = 0

    def set_error_attempts_timeout(self, timeout: int):
        self.__login_error_timestamp = time.time() + timeout

    def get_timeout_left(self):
        return self.__login_error_timestamp - time.time()

    def reset_session(self):
        self.__user = None
        self.__attempts = 0
        self.__login_error_timestamp = 0
        