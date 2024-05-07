"""
This module contains the Session class which manages user sessions, including login attempts,
timeouts, and user session data.
"""
import time

class Session:
    """
    A Session class to handle the state of a user session, including the current user,
    login attempts, and timeout handling.
    """

    def __init__(self):
        """
        Initializes a new session with no user, no login attempts, 
        and no login error timestamp.
        """
        self.__user = None
        self.__attempts = 0
        self.__login_error_timestamp = 0

    def get_user(self):
        """
        Returns the current user of the session.
        """
        return self.__user
    
    def set_user(self, user):
        """
        Sets the user for the session.
        """
        self.__user = user

    def get_attempts(self):
        """
        Returns the number of login attempts.
        """
        return self.__attempts
    
    def increment_attempts(self):
        """
        Increments the number of login attempts by one.
        """
        self.__attempts += 1

    def reset_attempts(self):
        """
        Resets the number of login attempts to zero.
        """
        self.__attempts = 0

    def set_error_attempts_timeout(self, timeout: int):
        """
        Sets a timeout after a failed login attempt, 
        using the current time plus the specified timeout.
        """
        self.__login_error_timestamp = time.time() + timeout

    def get_timeout_left(self):
        """
        Returns the remaining time until the session timeout is lifted.
        """
        return max(0, self.__login_error_timestamp - time.time())

    def reset_session(self):
        """
        Resets the session to its initial state with no user, 
        no login attempts, and no timeout.
        """
        self.__user = None
        self.__attempts = 0
        self.__login_error_timestamp = 0
