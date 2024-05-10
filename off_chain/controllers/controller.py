import re
from datetime import datetime
from db.db_operations import DatabaseOperations
from session.session import Session
from models.credentials import Credentials

class Controller:
    """
    Controller handles user and medical data interactions with the database.
    """
    def __init__(self, session: Session):
        """
        Initialize the Controller with a session object and set up the database operations.
        
        :param session: The session object to manage user sessions and login attempts.
        """
        self.db_ops = DatabaseOperations()
        self.session = session
        self.__n_attempts_limit = 5 # Maximum number of login attempts before lockout.
        self.__timeout_timer = 180 # Timeout duration in seconds.

    def registration(self, username: str, password: str, role: str, public_key: str, private_key: str):
        """
        Registers a new user in the database with the given credentials.
        
        :param username: The user's username.
        :param password: The user's password.
        :param role: The user's role in the system.
        :param public_key: The user's public key.
        :param private_key: The user's private key.
        :return: A registration code indicating success or failure.
        """
        registration_code = self.db_ops.register_creds(username, password, role, public_key, private_key)

        return registration_code
    
    def login(self, username: str, password: str, public_key: str, private_key: str):
        """
        Attempts to log a user in by validating credentials and handling session attempts.
        
        :param username: The user's username.
        :param password: The user's password.
        :param public_key: The user's public key.
        :param private_key: The user's private key.
        :return: Tuple containing a status code and the user's role, if successful.
        """
        if(self.check_attempts() and self.db_ops.check_credentials(username, password, public_key, private_key)):
            creds: Credentials = self.db_ops.get_creds_by_username(username)
            user_role = creds.get_role()
            user = self.db_ops.get_user_by_username(username)
            self.session.set_user(user)
            return 0, user_role
        elif self.check_attempts():
            self.session.increment_attempts()
            if self.session.get_attempts() == self.__n_attempts_limit:
                self.session.set_error_attempts_timeout(self.__timeout_timer)
            return -1, None
        else:
            return -2, None
    
    def insert_patient_info(self, role: str, username: str, name: str, lastname: str, birthday: str, birth_place: str, residence: str, autonomous: bool, phone: str):
        """
        Inserts patient information into the database.

        :param role: The role of the user (should be 'patient').
        :param username: The username of the patient.
        :param name: The first name of the patient.
        :param lastname: The last name of the patient.
        :param birthday: The birthday of the patient (format YYYY-MM-DD).
        :param birth_place: The place of birth of the patient.
        :param residence: The current residence of the patient.
        :param autonomous: A boolean indicating if the patient lives autonomously.
        :param phone: The phone number of the patient.
        :return: An insertion code indicating success (0) or failure.
        """
        insertion_code = self.db_ops.insert_patient(username, name, lastname, birthday, birth_place, residence, autonomous, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username) 
            self.session.set_user(user)
            print('DONE')

        return insertion_code
    
    def insert_medic_info(self, role: str, username: str, name: str, lastname: str, birthday: str, specialization: str, mail: str, phone: str):
        """
        Inserts medic information into the database.

        :param role: The role of the user (should be 'medic').
        :param username: The username of the medic.
        :param name: The first name of the medic.
        :param lastname: The last name of the medic.
        :param birthday: The birthday of the medic (format YYYY-MM-DD).
        :param specialization: The medical specialization of the medic.
        :return: An insertion code indicating success (0) or failure.
        """
        insertion_code = self.db_ops.insert_medic(username, name, lastname, birthday, specialization, mail, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username) 
            self.session.set_user(user)
            print('DONE')

        return insertion_code
    
    def insert_caregiver_info(self, role: str, username: str, name: str, lastname: str, username_patient: int, relationship: str, phone: str):
        """
        Inserts caregiver information into the database, associating the caregiver with a patient.

        :param role: The role of the user, expected to be 'caregiver'.
        :param username: The username of the caregiver.
        :param name: The first name of the caregiver.
        :param lastname: The last name of the caregiver.
        :param username_patient: The username or identifier of the patient for whom the caregiver is responsible.
        :param relationship: The relationship of the caregiver to the patient (e.g., parent, sibling, professional).
        :param phone: The phone number of the caregiver.
        :return: An insertion code indicating success (0) or failure of the operation. Success also triggers setting the user in the session and prints 'DONE'.
        """
        insertion_code = self.db_ops.insert_caregiver(username, name, lastname, username_patient, relationship, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username) 
            self.session.set_user(user)
            print('DONE')
        
        return insertion_code
    
    def insert_report(self, username_patient: str,  username_medic: str, analyses: str, diagnosis: str):
        """
        Inserts a medical report for a patient into the database, documented by a medic.

        :param username_patient: The username of the patient for whom the report is being created.
        :param username_medic: The username of the medic who is creating the report.
        :param analyses: Description or results of any analyses that were conducted.
        :param diagnosis: The diagnosis given by the medic based on the analyses.
        :return: An insertion code indicating the success (0) or failure of the operation. If successful, it prints a confirmation message.
        """
        insertion_code = self.db_ops.insert_report(username_patient, username_medic, analyses, diagnosis)

        if insertion_code == 0:
            print('Report inserted correctly.')

        return insertion_code
    
    def insert_treatment_plan(self, username_patient: str,  username_medic: str, description: str, start_date: str, end_date: str):
        """
        Inserts a treatment plan for a patient into the database, defined by a medic.

        :param username_patient: The username of the patient for whom the treatment plan is designed.
        :param username_medic: The username of the medic who is prescribing the treatment plan.
        :param description: A detailed description of the treatment plan.
        :param start_date: The start date of the treatment plan (format YYYY-MM-DD).
        :param end_date: The end date of the treatment plan (format YYYY-MM-DD).
        :return: An insertion code indicating the success (0) or failure of the operation. If successful, a message confirming the insertion is printed.
        """
        insertion_code = self.db_ops.insert_treatment_plan(username_patient, username_medic, description, start_date, end_date)

        if insertion_code == 0:
            print('Treatment plan inserted correctly.')

        return insertion_code

    def check_null_info(self, info):
        """
        Checks if the provided information is non-null (or truthy).

        :param info: The information to be checked. This can be any type, including strings, numbers, or other objects.
        :return: Returns True if the information is non-null/non-empty (truthy), False otherwise (falsy).
        """
        if info:
            return True
        else:
            return False
        
    def check_birthdate_format(self, date_string):
        """
        Validates that a provided date string is in the correct format ('YYYY-MM-DD') and is a date in the past.

        :param date_string: The date string to validate, expected to be in the format 'YYYY-MM-DD'.
        :return: Returns True if the date string is correctly formatted and represents a past date; 
        returns False if the date is not in the correct format or is in the future.
        """
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            current_date = datetime.now()
            if date < current_date:
                return True
            else:
                return False
        except ValueError:
            return False

    def check_tpdate_format(self, date_string, check_today = 0):
        """
        Validates that a provided date string is in the correct format ('YYYY-MM-DD') and optionally checks if the date is today or in the future.

        :param date_string: The date string to validate, which can be a string or a datetime object. If it is a datetime object, it is formatted to a string.
        :param check_today: A flag indicating the type of validation. If set to 0 (default), the function checks if the date is today or in the future. 
                            If set to any other value, the function simply checks the format without considering the date's relation to today.
        :return: Returns True if the date string is correctly formatted and, if check_today is 0, represents today's or a future date. 
                 Returns False if the date is not in the correct format, is in the past (when check_today is 0), or on any parsing failure.
        """
        try:
            if not isinstance(date_string, str):
                date_string = date_string.strftime('%Y-%m-%d')
            date = datetime.strptime(date_string, '%Y-%m-%d')
            current_date = datetime.now()
            if check_today == 0: 
                if date >= current_date: 
                    return True
                else:
                    return False
            else: return True
        except ValueError:
            return False
        
    def check_date_order(self, first_date_string, second_date_string):
        """
        Checks if the second date is chronologically after the first date.

        :param first_date_string: The first date as a string or a datetime object. If it is a datetime object, it will be formatted to a string.
        :param second_date_string: The second date as a string or a datetime object. If it is a datetime object, it will be formatted to a string.
        :return: Returns True if the second date is later than the first date. 
                 Returns False if either date is not in the correct 'YYYY-MM-DD' format or if the second date is not after the first date.
        """
        try:
            if not isinstance(first_date_string, str):
                first_date_string = first_date_string.strftime('%Y-%m-%d')
            if not isinstance(second_date_string, str):
                second_date_string = second_date_string.strftime('%Y-%m-%d')
            
            first_date = datetime.strptime(first_date_string, '%Y-%m-%d')
            second_date = datetime.strptime(second_date_string, '%Y-%m-%d')
            
            return second_date > first_date
        except ValueError:
            return False
       
    def check_phone_number_format(self, phone_number):
        """
        Validates that a given phone number is in a correct numerical format and within the expected length range.

        :param phone_number: The phone number string to validate. The number may contain spaces or hyphens.
        :return: Returns True if the phone number contains only digits (after removing spaces and hyphens) 
                 and if its length is between 7 and 15 characters. Returns False otherwise.
        """
        if phone_number.replace('-', '').replace(' ', '').isdigit():
            if 7 <= len(phone_number) <= 15:
                return True
        return False
    
    def check_email_format(self, email):
        """
        Validates that a given email address conforms to a standard email format.

        :param email: The email string to validate.
        :return: Returns True if the email matches the standard email format pattern.
                 Returns False if the email does not match this pattern.
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return True
        else:
            return False
        
    def possessive_suffix(self, name):
        """
        Determines the appropriate possessive suffix for a given name based on its final character.

        :param name: The name string to which the possessive suffix will be applied.
        :return: Returns "'s" if the last character of the name is not 's', otherwise returns "'" to form the possessive correctly.
        """
        if name[-1].lower() != 's':
            return"'s"
        else:
            return "'"

    def check_username(self, username):
        return self.db_ops.check_username(username)
    
    def check_keys(self, public_key, private_key):
        return self.db_ops.key_exists(public_key, private_key)
    
    def check_passwd(self, username, password):
        return self.db_ops.check_passwd(username, password)
    
    def check_unique_phone_number(self, phone):
        return self.db_ops.check_unique_phone_number(phone)
    
    def check_unique_email(self, mail):
        return self.db_ops.check_unique_email(mail)
    
    def change_passwd(self, username, old_pass, new_pass):
        """
        Changes a user's password in the database after verifying the old password.

        :param username: The username for which to change the password.
        :param old_pass: The current password to verify.
        :param new_pass: The new password to set.
        :return: A response code indicating the result of the operation; -2 if an error occurred.
        """
        if self.db_ops.check_passwd(username, old_pass):
            try:
                response = self.db_ops.change_passwd(username, old_pass, new_pass)
                return response
            except:
                return -2
    
    def get_user_by_username(self, username):
        return self.db_ops.get_user_by_username(username)
    
    def check_attempts(self):
        if self.session.get_attempts() < self.__n_attempts_limit:
            return True
        else:
            return False
        
    def get_creds_by_username(self, username):
        return self.db_ops.get_creds_by_username(username)
    
    def get_public_key_by_username(self, username):
        return self.db_ops.get_public_key_by_username(username)
    
    def get_medic_by_username(self, username):
        return self.db_ops.get_medic_by_username(username)
    
    def get_reports_list_by_username(self, username):
        return self.db_ops.get_reports_list_by_username(username)
    
    def get_treatplan_list_by_username(self, username):
        return self.db_ops.get_treatplan_list_by_username(username)
    
    def get_role_by_username(self, username):
        return self.db_ops.get_role_by_username(username)
    
    def get_patients(self):
        return self.db_ops.get_patients()
    