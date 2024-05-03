import math
import re
import click
from numpy import uint8

from controllers.controller import Controller
from controllers.action_controller import ActionController
from session.session import Session
from session.logging import log_error

class Utils:

    
    PAGE_SIZE = 3

    current_page = 0

    def __init__(self, session: Session):

        self.controller = Controller(session)
        self.act_controller = ActionController()

    def change_passwd(self, username, role):

        while True:
            confirmation = input("Do you want to change your password (Y/n): ").strip().upper()
            if confirmation == 'Y':
                while True:
                    old_pass = input('Old Password: ')
                    if not self.controller.check_passwd(username, old_pass):
                        print('\nYou entered the wrong old password.\n')
                        break
                    else:
                        while True:
                            new_passwd = input('New password: ')
                            new_confirm_password = input('Confirm new password: ')

                            passwd_regex = r'^.{8,50}$'
                            #passwd_regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,100}$'
                            if not re.fullmatch(passwd_regex, new_passwd):
                                print('Password must contain at least 8 characters, at least one digit, at least one uppercase letter, one lowercase letter, and at least one special character.\n')    
                            elif new_passwd != new_confirm_password:
                                print('Password and confirmation do not match. Try again\n')
                            else:
                                response = self.controller.change_passwd(username, old_pass, new_passwd)
                                if response == 0:
                                    print('\nPassword changed correctly!\n')
                                elif response == -1 or response == -2:
                                    print('\nSorry, something went wrong!\n')
                                break
                        break
            else:
                print("Okay\n")
            break
            
    def update_profile(self, username, role):
        
        us = self.controller.get_user_by_username(username)
        us.set_name(click.prompt('Name ', default=us.get_name()))
        us.set_lastname(click.prompt('Lastname ', default=us.get_lastname()))

        if role == "Patient":

            print("\nEnter your new Information...")
            while True:
                birthday = click.prompt('Date of birth (YYYY-MM-DD) ', default=us.get_birthday())
                if self.controller.check_birthdate_format(birthday): 
                    us.set_birthday(birthday)
                    break
                else: print("Invalid birthdate or incorrect format.")
            us.set_birth_place(click.prompt('Birth place ', default=us.get_birth_place()))
            us.set_residence(click.prompt('Residence ', default=us.get_residence()))
            while True:
                phone = click.prompt('Phone ', default=us.get_phone())
                if self.controller.check_phone_number_format(phone): 
                    us.set_phone(phone)
                    break
                else: print("Invalid phone number format.")

            autonomous_flag = int(us.get_autonomous())
            name = us.get_name()
            lastname = us.get_lastname()
            if autonomous_flag == 1:
                try:
                    from_address_patient = self.controller.get_public_key_by_username(username)
                    self.act_controller.update_entity('patient', name, lastname, autonomous_flag, from_address=from_address_patient)
                except Exception as e:
                    log_error(e)

        elif role == "Caregiver":
  
            print("\nEnter your new Information...")
            while True:
                phone = click.prompt('Phone ', default=us.get_phone())
                if self.controller.check_phone_number_format(phone): 
                    us.set_phone(phone)
                    break
                else: print("Invalid phone number format.")
            
            name = us.get_name()
            lastname = us.get_lastname()
            try:
                from_address_caregiver = self.controller.get_public_key_by_username(username)
                self.act_controller.update_entity('caregiver', name, lastname, from_address=from_address_caregiver)
            except Exception as e:
                log_error(e)

        elif role == "Medic":
            
            print("\nEnter your new Information...")
            while True:
                birthday = click.prompt('Date of birth (YYYY-MM-DD) ', default=us.get_birthday())
                if self.controller.check_birthdate_format(birthday): 
                    us.set_birthday(birthday)
                    break
                else: print("Invalid birthdate or incorrect format.")
            us.set_specialization(click.prompt('Specialization ', default=us.get_specialization()))
            while True:
                mail = click.prompt('Mail ', default=us.get_mail())
                if self.controller.check_email_format(mail): 
                    us.set_mail(mail)
                    break
                else: print("Invalid email format.")
            while True:
                phone = click.prompt('Phone ', default=us.get_phone())
                if self.controller.check_phone_number_format(phone): 
                    us.set_phone(phone)
                    break
                else: print("Invalid phone number format.")
            
            name = us.get_name()
            lastname = us.get_lastname()
            specialization = us.get_specialization()
            try:
                from_address_medic = self.controller.get_public_key_by_username(username)
                self.act_controller.update_entity('medic', name, lastname, specialization, from_address=from_address_medic)
            except Exception as e:
                log_error(e)

        us.save()


    '''
    -----------------------------------------------------
    Funzioni di gestione della visualizzazione del menù
    'Visualizzazione pazienti' del medico
    '''

    def get_page_records(self, page_index, patients):
        start_index = page_index * self.PAGE_SIZE
        end_index = start_index + self.PAGE_SIZE

        if not patients:
            print("\nThere are no patients in the system. \n")
            return
        print("\nList of patients: \n")
        return patients[start_index:end_index]

    def display_records(self, records):
        for i, patient in enumerate(records, start=1):
            print(f"{i}. Username: {patient['0']}, Name: {patient['1']}, Last name: {patient['2']}")

    def go_to_next_page(self, patients):

        total_pages = math.ceil(len(patients) / self.PAGE_SIZE)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.show_page(patients)

    def go_to_previous_page(self, patients):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(patients)

    def show_patient_details(self, patient):

        print("\nPatient Details:")
        print(f"Username: {patient['1']}")
        print(f"Name: {patient['2']}")
        print(f"Last Name: {patient['3']}")
        #print(f"Age: {patient['age']}")
        #print(f"Gender: {patient['gender']}")
        #print(f"Condition: {patient['condition']}")


    def handle_selection(self, patients):
        records = self.get_page_records(self.current_page, patients)
        print("\nSelect a patient's username to view details:")
        for i, patient in enumerate(records, start=1):
            print(f"{i}. {patient['1']}")
        selection = input("Enter patient number (or '0' to cancel): ")
        if selection.isdigit():
            selection_index = int(selection) - 1
            if 0 <= selection_index < len(records):
                self.show_patient_details(records[selection_index])

    def show_page(self, patients):
        records = self.get_page_records(self.current_page, patients)
        if records is not None:
            self.display_records(records)

    '''--------------------------------------------------'''