from datetime import datetime
import re

from db.db_operations import DatabaseOperations
from session.session import Session
from models.credentials import Credentials


class Controller:

    def __init__(self, session: Session):
        self.db_ops = DatabaseOperations()
        self.session = session
        self.__n_attempts_limit = 5
        self.__timeout_timer = 180

    def registration(self, username: str, password: str, role: str, public_key: str, private_key: str):
        registration_code = self.db_ops.register_creds(username, password, role, public_key, private_key)

        return registration_code
    
    def login(self, username: str, password: str, public_key: str, private_key: str):
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
        insertion_code = self.db_ops.insert_patient(username, name, lastname, birthday, birth_place, residence, autonomous, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username) 
            self.session.set_user(user)
            print('DONE')

        return insertion_code
    
    def insert_medic_info(self, role: str, username: str, name: str, lastname: str, birthday: str, specialization: str, mail: str, phone: str):
        insertion_code = self.db_ops.insert_medic(username, name, lastname, birthday, specialization, mail, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username) 
            self.session.set_user(user)
            print('DONE')

        return insertion_code
    
    def insert_caregiver_info(self, role: str, username: str, name: str, lastname: str, username_patient: int, relationship: str, phone: str):
        insertion_code = self.db_ops.insert_caregiver(username, name, lastname, username_patient, relationship, phone)

        if insertion_code == 0:
            user = self.db_ops.get_user_by_username(username) 
            self.session.set_user(user)
            print('DONE')
        
        return insertion_code
    
    def insert_report(self, username_patient: str,  username_medic: str, analyses: str, diagnosis: str):
        insertion_code = self.db_ops.insert_report(username_patient, username_medic, analyses, diagnosis)

        if insertion_code == 0:
            print('Report inserted correctly.')

        return insertion_code
    
    def insert_treatment_plan(self, username_patient: str,  username_medic: str, description: str, start_date: str, end_date: str):
        insertion_code = self.db_ops.insert_treatment_plan(username_patient, username_medic, description, start_date, end_date)

        if insertion_code == 0:
            print('Treatment plan inserted correctly.')

        return insertion_code
    
    def update_treatment_plan(self, id_treatment_plan, updated_description, new_start_date, new_end_date):
        return self.db_ops.update_treatment_plan(id_treatment_plan, updated_description, new_start_date, new_end_date)

    def check_null_info(self, info):
        if info: return True
        else: return False
        
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

    def check_tpdate_format(self, date_string, check_today = 0):
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
        if phone_number.replace('-', '').replace(' ', '').isdigit():
            if 7 <= len(phone_number) <= 15:
                return True
        return False
    
    def check_email_format(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return True
        else:
            return False
        
    def possessive_suffix(self, name):
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
        if self.db_ops.check_passwd(username, old_pass):
            try:
                response = self.db_ops.change_passwd(username, old_pass, new_pass)
                return response
            except:
                return -2
    
    def get_user_by_username(self, username):
        return self.db_ops.get_user_by_username(username)
    
    def check_patient_by_username(self, username): #forse non serve
        return self.db_ops.check_patient_by_username(username)
    
    def check_attempts(self):
        if self.session.get_attempts() < self.__n_attempts_limit:
            return True
        else:
            return False
        
    def get_creds_by_username(self, username):
        return self.db_ops.get_creds_by_username(username)
    
    def get_public_key_by_username(self, username):
        return self.db_ops.get_public_key_by_username(username)

    def get_treatmentplan_by_username(self, username):
        return self.db_ops.get_treatmentplan_by_username(username)
    
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
    