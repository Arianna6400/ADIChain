import math
import re
import click
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table



from numpy import uint8

from controllers.controller import Controller
from controllers.action_controller import ActionController
from session.session import Session
from session.logging import log_error


class Utils:

    init(convert=True)

    
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
        return patients[start_index:end_index]

    def get_page_reports(self, page_index, username):
        start_index = page_index * self.PAGE_SIZE
        end_index = start_index + self.PAGE_SIZE

        reports = self.controller.get_reports_list_by_username(username)
        if not reports:
            print(f"\n{username} doesn't have reports yet.")
            while True:
                new_report = input("\nDo you want to add one? (Y/n) ").strip().upper()
                if new_report == 'Y':
                    analysis = input("\nInsert analysis: ")
                    diagnosis = input("\nInsert diagnosis: ")
                    self.controller.insert_report(username, "medico", analysis, diagnosis)
                    break
                return
        return reports[start_index:end_index]

    def display_records(self, records):

        table = Table(title="Patients")

        columns = ["Username", "Name", "Last Name", "Date of Birth", "Place of Birth","Residence"]

        for column in columns:
            table.add_column(column)

        for patient in records:
            row = [patient[0], patient[1], patient[2], patient[3], patient[4], patient[5]]
            table.add_row(*row, style = 'bright_green')

        console = Console()
        console.print(table)

    def display_reports(self, reports, username):

        possessive_suffix = self.controller.possessive_suffix(username)
        table = Table(title=f"{username}{possessive_suffix} reports")

        columns = ["id_report", "username_patient", "username_medic", "analysis", "diagnosis"]

        for column in columns:
            table.add_column(column)

        for report in reports:
            row = [str(report.get_id_report()), report.get_username_patient(), report.get_username_medic(), report.get_analyses(), report.get_diagnosis()]
            table.add_row(*row, style = 'bright_green')

        console = Console()
        console.print(table)

    def go_to_next_page(self, list):

        total_pages = math.ceil(len(list) / self.PAGE_SIZE)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.show_page(list)
        else:
            self.show_page(list)
            print(Fore.RED + "\nNo more patients in the system." + Style.RESET_ALL)
            return

    def go_to_previous_page(self, list):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(list)
        else:
            self.show_page(list)
            print(Fore.RED + "\nInvalid action!" + Style.RESET_ALL)

    def show_patient_details(self, patient):

        print("\nPatient Details:")
        print(f"Username: {patient[0]}")
        print(f"Name: {patient[1]}")
        print(f"Last Name: {patient[2]}")
        print(f"Age: {patient[3]}")
        print(f"Place of birth: {patient[4]}")
        print(f"Residence: {patient[5]}")

    def handle_selection(self, patients):
        #records = self.get_page_records(self.current_page, patients)
        print("\nSelect a patient's username to view details:")
        for i, patient in enumerate(patients, start=1):
            print(f"{i}. {patient[1]}")
        selection = input("Enter patient number (or '0' to cancel): ")
        if selection.isdigit():
            selection_index = int(selection) - 1
            if 0 <= selection_index < len(patients):
                self.show_patient_details(patients[selection_index])
                self.patient_medical_data(patients[selection_index][0], patients)
        
        # VISUALIZZA REPORTS E TREAT.PLAN come i pazienti

    def show_page(self, patients):
        records = self.get_page_records(self.current_page, patients)
        if records is not None:
            self.display_records(records)

    def patient_medical_data(self, username, patients):
        while True: 
            print("\nMEDICAL DATA")
            print('\nWhich type of data do you want to consult?')
            print("1 -- Reports ")
            print("2 -- Treatment plans") 
            print("3 -- Undo") 
            
            try:
                choice = int(input('Enter your choice: '))

                if choice == 1:
                    reports = self.get_page_reports(self.current_page, username)
                    if reports is not None:
                        self.display_reports(reports, username)
                        while len(reports) > 0:

                            action = input("\nEnter 'n' for next page, 'p' for previous page, 'a' to add a new report, or 'q' to quit: \n")

                            if action == "n" or action == "N":
                                self.go_to_next_page(reports)
                            elif action == "p" or action == "P":
                                self.go_to_previous_page(reports)
                            elif action == "a" or action == "A":
                                self.add_report(username)
                                self.display_reports(reports)
                            elif action == "q" or action == "Q":
                                print("Exiting...\n")
                                break
                            else:
                                print("Invalid input. Please try again. \n")
                        #self.medic_menu(username)

                    #self.view_treatmentplan(username)

                if choice == 2:
                    self.view_treatmentplan_patient(username) # finire

                if choice == 3:
                    self.show_page(patients)
                    return
                
                else:
                    print('Wrong option. Please enter one of the options listed in the menu!')

            except ValueError:
                print('Wrong input. Please enter a number!')


    def add_report(self, username):

        print("\nInsert the information regarding the new report...")
    
        analysis = input("\nInsert analysis: ")
        diagnosis = input("\nInsert diagnosis: ")
        result_code = self.controller.insert_report(username, "medico", analysis, diagnosis)

        if result_code == 0:
            print("\nNew report has been saved correctly.")
        else:
            print("\nInternal error!")



    '''--------------------------------------------------'''


