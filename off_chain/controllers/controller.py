from datetime import datetime
import re

from db.db_operations import DatabaseOperations
from session.session import Session


class Controller:

    def __init__(self, session: Session):
        self.db_ops = DatabaseOperations()
        self.session = session
        self.__n_attempts_limit = 5
        self.__timeout_timer = 180        


    def registration(self, username: str, password: str, role: str, public_key: str, private_key: str):
        registration_code = self.db_ops.register_creds(username, password, role, public_key, private_key)

        return registration_code
    
    def insert_patient_info(self, role: str, username: str, name: str, lastname: str, birthday: str, birth_place: str, residence: str, autonomous: bool, phone: str):
        insertion_code = self.db_ops.insert_patient(username, name, lastname, birthday, birth_place, residence, autonomous, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username, role) 
            self.session.set_user(user)
            print('DONE')

        return insertion_code
    
    def insert_medic_info(self, role: str, username: str, name: str, lastname: str, birthday: str, specialization: str, mail: str, phone: str):
        insertion_code = self.db_ops.insert_medic(username, name, lastname, birthday, specialization, mail, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username, role) 
            self.session.set_user(user)
            print('DONE')

        return insertion_code
    
    def insert_caregiver_info(self, role: str, username: str, name: str, lastname: str, id_patient: int, relationship: str, phone: str):
        insertion_code = self.db_ops.insert_caregiver(username, name, lastname, id_patient, relationship, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username, role) 
            self.session.set_user(user)
            print('DONE')
        
        return insertion_code

    def check_birthdate_format(self, date_string):
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            current_date = datetime.now()
            if date < current_date:
                return True
            else:
                return False
        except ValueError:
            return False
        
    def check_phone_number_format(self, phone_number):
        # Check if the phone number contains only digits and optional hyphens or spaces
        if phone_number.replace('-', '').replace(' ', '').isdigit():
            # Check if the length of the phone number is between 7 and 15 characters
            if 7 <= len(phone_number) <= 15:
                return True
        return False
    
    def check_email_format(self, email):
        # Regular expression pattern for email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Use the re.match function to check if the email matches the pattern
        if re.match(email_pattern, email):
            return True
        else:
            return False