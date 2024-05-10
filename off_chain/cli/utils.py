"""
This module provides various utility functions for handling user input, updating profiles, changing passwords, 
displaying data, managing reports and treatment plans, and navigating through pages of patient records, reports, 
and treatment plans. It also includes functions for adding new reports and treatment plans.
"""

import datetime
import math
import re
import click
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table

from controllers.controller import Controller
from controllers.action_controller import ActionController
from session.session import Session
from session.logging import log_error


class Utils:
    """
    This class provides various utility methods for handling user input, updating profiles, changing passwords, 
    displaying data, managing reports and treatment plans, and navigating through pages of patient records, reports, 
    and treatment plans. It also includes methods for adding new reports and treatment plans.

    Attributes:
        PAGE_SIZE (int): The number of items to display per page.
        current_page (int): The index of the current page being displayed.

    """

    init(convert=True)

    PAGE_SIZE = 3
    current_page = 0
    
    def __init__(self, session: Session):

        """
        Initializes the Utils class with a session object.

        Parameters:
            session (Session): The session object containing user information.

        Attributes:
            session (Session): The session object containing user information.
            controller (Controller): An instance of the Controller class for database interaction.
            act_controller (ActionController): An instance of the ActionController class for managing actions.
            today_date (str): The current date in string format.
        """

        self.session = session
        self.controller = Controller(session)
        self.act_controller = ActionController()
        self.today_date = str(datetime.date.today())

    def change_passwd(self, username):
        """
        Allows the user to change their password.

        Args:
            username (str): The username of the user whose password is being changed.

        Returns:
            None
        """

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
        """
        Updates the profile information of a user.

        Parameters:
            username (str): The username of the user whose profile is being updated.
            role (str): The role of the user (e.g., "Patient", "Caregiver", "Medic").

        Returns:
            None
        """
     
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


    def get_page_records(self, page_index, patients):

        """
        Retrieves a subset of patient records for a specific page.

        Parameters:
            page_index (int): The index of the page to retrieve.
            patients (list): A list of patient records.

        Returns:
            list: A subset of patient records for the specified page.
        """

        start_index = page_index * self.PAGE_SIZE
        end_index = start_index + self.PAGE_SIZE

        if not patients:
            print("\nThere are no patients in the system. \n")
            return
        return patients[start_index:end_index]

    def get_page_reports(self, page_index, username):

        """
        Retrieves a subset of reports for a specific page belonging to a particular user.

        Parameters:
            page_index (int): The index of the page to retrieve.
            username (str): The username of the user whose reports are to be fetched.

        Returns:
            list: A subset of reports for the specified page.
        """

        user_auth = self.session.get_user()
        username_auth = user_auth.get_username()

        start_index = page_index * self.PAGE_SIZE
        end_index = start_index + self.PAGE_SIZE

        reports = self.controller.get_reports_list_by_username(username)
        if not reports:
            print(f"\n{username} doesn't have reports yet.")
            if self.controller.get_role_by_username(username_auth) == "MEDIC": 
                while True:
                    new_report = input("\nDo you want to add one? (Y/n) ").strip().upper()
                    if new_report == 'Y':
                        self.add_report(username)
                        return self.controller.get_reports_list_by_username(username)
                    elif new_report == 'N': return
                    else: print("Invalid choice!")
                    #return
        else: return reports[start_index:end_index]
    
    def get_page_treatplan(self, page_index, username):

        """
        Retrieves a subset of treatment plans for a specific page belonging to a particular user.

        Args:
            page_index (int): The index of the page to retrieve.
            username (str): The username of the user whose treatment plans are to be fetched.

        Returns:
            list: A subset of treatment plans for the specified page.
        """

        user_auth = self.session.get_user()
        username_auth = user_auth.get_username()

        start_index = page_index * self.PAGE_SIZE
        end_index = start_index + self.PAGE_SIZE

        treats = self.controller.get_treatplan_list_by_username(username)
        if not treats:
            print(f"\n{username} doesn't have any treatment plan yet.")
            if self.controller.get_role_by_username(username_auth) == "MEDIC":
                while True:
                    new_treat = input("\nDo you want to add one? (Y/n) ").strip().upper()
                    if new_treat == 'Y':
                        self.add_treatment_plan(username)
                        return self.controller.get_treatplan_list_by_username(username)
                    elif new_treat == 'N': return
                    else: print("Invalid choice!")
                    #return
        else: return treats[start_index:end_index]

    def display_records(self, records):

        """
        Displays the records (patients) in a tabular format.

        Args:
            records (list): A list of patient records to be displayed.
        """

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
        """
        Displays the reports of a specific user in a tabular format.

        Args:
            reports (list): A list of report objects to be displayed.
            username (str): The username of the user whose reports are being displayed.
        """

        possessive_suffix = self.controller.possessive_suffix(username)
        table = Table(title=f"{username}{possessive_suffix} reports")

        columns = ["id_report", "date", "username_medic", "analysis", "diagnosis"]

        for column in columns:
            table.add_column(column)

        for i, report in enumerate(reports, start=1):
            row = [str(i), report.get_date(), report.get_username_medic(), report.get_analyses(), report.get_diagnosis()]
            table.add_row(*row, style = 'bright_green')

        console = Console()
        console.print(table)

    def display_treats(self, treats, username):

        """
        Displays the treatment plans of a specific user in a tabular format.

        Args:
            treats (list): A list of treatment plan objects to be displayed.
            username (str): The username of the user whose treatment plans are being displayed.
        """

        possessive_suffix = self.controller.possessive_suffix(username)
        table = Table(title=f"{username}{possessive_suffix} treatment plans")

        columns = ["id_treatment_plan", "date", "username_medic", "description", "start_date", "end_date"]
        
        for column in columns:
            table.add_column(column)

        for i, treat in enumerate(treats, start=1):
            row = [str(i), treat.get_date(), treat.get_username_medic(), treat.get_description(), treat.get_start_date(), treat.get_end_date()]
            table.add_row(*row, style = 'bright_green')

        console = Console()
        console.print(table)

    def view_reports(self, reports):
        """
        Allows the user to select and view details of a specific report from a list of reports.

        Args:
            reports (list): A list of report objects to choose from.
        """

        while True:
            print("\nSelect the number of the report you'd like to visualize:")
            i = 1
            for i, report in enumerate(reports, start = i):
                print(f"- {i}")
            try:
                selection = int(input("Enter report number (or '0' to cancel): "))
                if 0 < selection <= i:
                    selection_index = int(selection) - 1
                    if 0 <= selection_index < len(reports):
                        self.show_report_details(reports[selection_index])
                        #break
                elif selection == 0: break
                else: print("\nInvalid input, try again!")
            except: print("Invalid input!")

    def view_treatment_plan(self, treats):
        """
        Allows the user to select and view details of a specific treatment plan from a list of treatment plans.

        Args:
            treats (list): A list of treatment plan objects to choose from.
        """

        while True:
            print("\nSelect the number of the treatment plan you'd like to visualize:")
            i = 1
            for i, treat in enumerate(treats, start = i):
                print(f"- {i}")
            try:
                selection = int(input("Enter treatment plan number (or '0' to cancel): "))
                if 0 < selection <= i:
                    selection_index = int(selection) - 1
                    if 0 <= selection_index < len(treats):
                        self.show_treatment_plan_details(treats[selection_index])
                        #break
                elif selection == 0: break
                else: print("\nInvalid input, try again!")
            except: print("Invalid input!")

    def go_to_next_page(self, list, flag, username):
        """
        Displays the next page of records based on the current page index.

        Args:
            list (list): The list of records to paginate through.
            flag (int): A flag indicating the type of records (0 for general records, 1 for reports, 2 for treatment plans).
            username (str): The username associated with the records.

        Returns:
            None
        """

        total_pages = math.ceil(len(list) / self.PAGE_SIZE)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.show_page(list, flag, username)
        else:
            self.show_page(list, flag, username)
            print(Fore.RED + "\nNo more results found." + Style.RESET_ALL)
            return

    def go_to_previous_page(self, list, flag, username):
        """
        Displays the previous page of records based on the current page index.

        Args:
            list (list): The list of records to paginate through.
            flag (int): A flag indicating the type of records (0 for general records, 1 for reports, 2 for treatment plans).
            username (str): The username associated with the records.

        Returns:
            None
        """

        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(list, flag, username)
        else:
            self.show_page(list, flag, username)
            print(Fore.RED + "\nInvalid action!" + Style.RESET_ALL)

    def show_patient_details(self, patient):

        """
        Display details of a patient.

        Args:
            patient (tuple): Tuple containing patient details (username, name, last name, age, place of birth, residence).
        """

        print("\nPatient Details:")
        print(f"Username: {patient[0]}")
        print(f"Name: {patient[1]}")
        print(f"Last Name: {patient[2]}")
        print(f"Age: {patient[3]}")
        print(f"Place of birth: {patient[4]}")
        print(f"Residence: {patient[5]}")

    def show_report_details(self, report):

        """
        Display details of a medical report.

        Args:
            report (Report): The medical report object containing the report details.
        """

        print(f"\nReport issued on {report.get_date()} by the medic {report.get_username_medic()}:")
        print(f"\nAnalyses: {report.get_analyses()}")
        print(f"\nDiagnosis: {report.get_diagnosis()}")
        input("\nPress Enter to exit\n")

    def show_treatment_plan_details(self, treat):

        """
        Display details of a treatment plan.

        Args:
            treat (TreatmentPlan): The treatment plan object containing the plan details.
        """

        user = self.session.get_user()
        username_med = user.get_username()
        role = self.controller.get_role_by_username(username_med)

        while True:
            print(f"\nTreatment plan issued on {treat.get_date()} by the medic {treat.get_username_medic()}:")
            print(f"\nDescription: {treat.get_description()}")
            print(f"\nTreatment plan's start: {treat.get_start_date()}")
            print(f"\nTreatment plan's end: {treat.get_end_date()}")
            if role == "MEDIC":
                action = input("\nEnter 'u' to update, or 'q' to quit: \n")
                if action == "u" or action == "U":
                    self.update_treat(treat, username_med)
                elif action == "q" or action == "Q":
                    print("Going back...\n")
                    break
                else:
                    print("Invalid input. Please try again. \n")
            else:
                input("\nPress Enter to exit\n") 
                break

    def update_treat(self, treat, medic_username):
        """
        Update a treatment plan.

        Args:
            treat (TreatmentPlan): The treatment plan object to be updated.
            medic_username (str): The username of the medic updating the treatment plan.
        """

        print("\nEnter new treatment plan details (click Enter to keep current values):")
        new_description = input(f"Description ({treat.get_description()}): ").strip() or treat.get_description()
        while True:
            new_start_date = input(f"Start date ({treat.get_start_date()}): ").strip() or str(treat.get_start_date())
            if self.controller.check_tpdate_format(new_start_date, 1): break
            else: print("Invalid date or incorrect format.")
            
        while True:
            new_end_date = input(f"End date ({treat.get_end_date()}): ").strip() or str(treat.get_end_date())
            if self.controller.check_tpdate_format(new_end_date, 1): 
                if self.controller.check_date_order(new_start_date, new_end_date): break
                else: print("\nThe second date cannot come before the first date!")
            else: print("Invalid date or incorrect format.")

        if new_description != treat.get_description() or new_start_date != treat.get_start_date() or new_end_date != treat.get_end_date():
            updated_description = f"{treat.get_description()}. \nDescription updated on {self.today_date} by the medic {medic_username}: {new_description}"
            treat.set_description(updated_description)
            treat.set_start_date(new_start_date)
            treat.set_end_date(new_end_date)
            treat.save()
            try:
                try:
                    from_address_medic = self.controller.get_public_key_by_username(medic_username)
                    self.act_controller.manage_treatment_plan('update', treat.get_id_treatment_plan(),
                                                                updated_description, new_start_date,
                                                                new_end_date, from_address=from_address_medic)
                except Exception as e:
                    log_error(e)
                self.controller.update_treatment_plan(treat.get_id_treatment_plan(), updated_description, new_start_date, new_end_date)
                print("Treatment plan updated successfully.")
            except Exception as e:
                print("An error occurred while updating the treatment plan:", e)
        else:
            print("No changes made to the treatment plan.")

    def handle_selection(self, patients):
        """
        Handle the selection of a patient for viewing details.

        Args:
            patients (list): A list of patient records.

        Returns:
            None
        """

        while True:
            print("\nSelect a patient's username to view details:")
            i = 1
            for i, patient in enumerate(patients, start = i):
                print(f"{i}. {patient[0]}")
            try:
                selection = int(input("Enter patient number (or '0' to cancel): "))
                if 0 < selection <= i:
                    selection_index = int(selection) - 1
                    if 0 <= selection_index < len(patients):
                        self.show_patient_details(patients[selection_index])
                        self.patient_medical_data(patients[selection_index][0])
                        break
                elif selection == 0: break
                else: print("\nInvalid input, try again!")
            except: print("Invalid input!")
      
    def show_page(self, list, flag, username):
        """
        Display a page of records based on the flag.

        Args:
            list (list): The list of records to display.
            flag (int): An integer flag indicating the type of records (0 for general records, 1 for reports, 2 for treatment plans).
            username (str): The username associated with the records.

        Returns:
            None
        """

        if flag == 0:
            records = self.get_page_records(self.current_page, list)
        elif flag == 1:
            records = self.get_page_reports(self.current_page, username)
        elif flag == 2:
            records = self.get_page_treatplan(self.current_page, username)
        if records is not None and flag == 0:
            self.display_records(records)

    def patient_medical_data(self, username):
        """
        Display medical data for a given patient.

        Args:
            username (str): The username of the patient.

        Returns:
            None
        """

        while True: 
            print("\nMEDICAL DATA")
            print('\nWhich type of data do you want to consult?')
            print("1 -- Reports ")
            print("2 -- Treatment plans") 
            print("3 -- Undo")
            
            user_auth = self.session.get_user()
            role = self.controller.get_role_by_username(user_auth.get_username())

            try:
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    while True:
                        reports = self.controller.get_reports_list_by_username(username)
                        pagereports = self.get_page_reports(self.current_page, username)
                        if pagereports:
                            self.display_reports(pagereports, username)

                            if role == "MEDIC":
                                action = input("\nEnter 'n' for next page, 'p' for previous page, 'a' to add a new report, 'v' to visualize one, or 'q' to quit: \n")
                            else:
                                # lele ti amo
                                action = input("\nEnter 'n' for next page, 'p' for previous page, 'v' to visualize one, or 'q' to quit: \n")

                            if action == "n" or action == "N":
                                self.go_to_next_page(reports, 1, username)
                            elif action == "p" or action == "P":
                                self.go_to_previous_page(reports, 1, username)
                            elif (action == "a" or action == "A") and role == "MEDIC":
                                self.add_report(username)
                            elif action == "v" or action == "V":
                                self.view_reports(pagereports)
                            elif action == "q" or action == "Q":
                                print("Exiting...\n")
                                break
                            else:
                                print("Invalid input. Please try again. \n")
                        else: break

                elif choice == 2:
                    while True:
                        treats = self.controller.get_treatplan_list_by_username(username)
                        pagetreats = self.get_page_treatplan(self.current_page, username)
                        if pagetreats:
                            self.display_treats(pagetreats, username)

                            if role == "MEDIC":
                                action = input("\nEnter 'n' for next page, 'p' for previous page, 'a' to add a new treatment plan, 'v' to visualize one, or 'q' to quit: \n")
                            else:
                                action = input("\nEnter 'n' for next page, 'p' for previous page, 'v' to visualize one, or 'q' to quit: \n")

                            if action == "n" or action == "N":
                                self.go_to_next_page(treats, 2, username)
                            elif action == "p" or action == "P":
                                self.go_to_previous_page(treats, 2, username)
                            elif (action == "a" or action == "A") and role == "MEDIC":
                                self.add_treatment_plan(username)
                            elif action == "v" or action == "V":
                                self.view_treatment_plan(pagetreats)
                            elif action == "q" or action == "Q":
                                print("Exiting...\n")
                                break
                            else:
                                print("Invalid input. Please try again. \n")
                        else: break

                elif choice == 3:
                    break
                
                else:
                    print('Wrong option. Please enter one of the options listed in the menu!')

            except ValueError:
                print('Wrong input. Please enter a number!')

    def add_report(self, username):
        """
        Add a new report for a given patient.

        Args:
            username (str): The username of the patient.

        Returns:
            None
        """

        user = self.session.get_user()
        username_med = user.get_username()

        print("\nInsert the information regarding the new report...")
    
        analysis = input("\nInsert analysis: ")
        diagnosis = input("\nInsert diagnosis: ")

        try:
            from_address_medic = self.controller.get_public_key_by_username(username_med)
            self.act_controller.manage_report('add', analysis, diagnosis, from_address=from_address_medic)
        except Exception as e:
            log_error(e)
        result_code = self.controller.insert_report(username, username_med, analysis, diagnosis)
        
        if result_code == 0:
            print("\nNew report has been saved correctly.")
        else:
            print("\nInternal error!")

    def add_treatment_plan(self, username):
        """
        Add a new treatment plan for a given patient.

        Args:
            username (str): The username of the patient.

        Returns:
            None
        """

        user = self.session.get_user()
        username_med = user.get_username()

        print("\nInsert the information regarding the new treatment plan...")
    
        description = input("\nInsert description: ")
        while True:
            quest = input("\nDoes the patient have to start the plan today? (Y/n) ").strip().upper()
            if quest == "Y": 
                start_date = self.today_date
                break
            elif quest == "N": 
                while True:
                    start_date = input("\nEnter the starting date (YYYY-MM-DD): ")
                    if self.controller.check_tpdate_format(start_date): break
                    else: print("Invalid date or incorrect format.")
                break
            else: print("invalid input!") 
        while True:
            end_date = input("\nEnter the ending date (YYYY-MM-DD): ")
            if self.controller.check_tpdate_format(end_date):
                if self.controller.check_date_order(start_date, end_date): break
                else: print("\nThe second date cannot come before the first date!")
            else: print("Invalid date or incorrect format.")
        
        try:
            from_address_medic= self.controller.get_public_key_by_username(username_med)
            self.act_controller.manage_treatment_plan('add', description, start_date, end_date, from_address=from_address_medic)
        except Exception as e:
            log_error(e)
        result_code = self.controller.insert_treatment_plan(username, username_med, description, start_date, end_date)

        if result_code == 0:
            print("\nNew treatment plan has been saved correctly.")
        else:
            print("\nInternal error!")