"""
This module provides a command-line interface (CLI) for a healthcare system. 
It allows users to register new accounts, log in, and perform various actions based on their roles 
(e.g., patient, medic, caregiver).
"""

import getpass
import re

from eth_utils import *
from eth_keys import *
from controllers.controller import Controller
from controllers.action_controller import ActionController
from session.session import Session
from db.db_operations import DatabaseOperations
from cli.utils import Utils


class CommandLineInterface:
    """
    This class represents the command-line interface (CLI) of a healthcare system. 
    It facilitates user interactions, such as registration, login, and navigation 
    through various functionalities based on user roles (patient, medic, caregiver).
    """
    def __init__(self, session: Session):
        """Initialize the CommandLineInterface with a session.

        Args:
            session (Session): An instance of the Session class representing the user's session.

        Attributes:
            controller (Controller): instance of the Controller class, responsible for handling the business logic and interfacing with the underlying system.
            act_controller (ActionController): instance of the ActionController class, managing actions related to smart contract deployment and entity registration.
            session (Session): instance of the Session class, managing user sessions and authentication states.
            ops (DatabaseOperations): instance of the DatabaseOperations class, handling database operations such as user registration and data retrieval.
            util (Utils): instance of the Utils class, providing utility functions for various tasks within the CLI.
            menu (dict): dictionary mapping menu option numbers to their corresponding descriptions.
        """

        self.controller = Controller(session)
        self.act_controller = ActionController()
        self.session = session
        self.ops = DatabaseOperations()
        self.util = Utils(session)

        self.menu = {
            1: 'Register New Account',
            2: 'Log In',
            3: 'Exit',
        }

    PAGE_SIZE = 3

    current_page = 0

    def print_menu(self):
        """
        This method prints the main menu options available to the user and prompts for 
        their choice. It then directs the user to the corresponding functionality based 
        on their selection. The method handles user input validation to ensure a valid 
        choice is made.
        """

        print(r""" ______     _____     __     ______     __  __     ______     __     __   __       
/\  __ \   /\  __-.  /\ \   /\  ___\   /\ \_\ \   /\  __ \   /\ \   /\ "-.\ \      
\ \  __ \  \ \ \/\ \ \ \ \  \ \ \____  \ \  __ \  \ \  __ \  \ \ \  \ \ \-.  \     
 \ \_\ \_\  \ \____-  \ \_\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_\  \ \_\\"\_\    
  \/_/\/_/   \/____/   \/_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_/   \/_/ \/_/   
            """)

        for key in self.menu.keys():
            print(key, '--' ,self.menu[key])

        try:
            choice = int(input('Enter your choice: '))

            if choice == 1:
                print('Proceed with the registration...')
                self.registration_menu()
            elif choice == 2:
                print('Proceed with the log in...')
                res_code = self.login_menu()
                if res_code == 0:
                    self.print_menu()
            elif choice == 3:
                print('Bye Bye!')
                exit()
            else:
                print('Wrong option. Please enter one of the options listed in the menu!')

        except ValueError:
            print('Wrong input. Please enter a number!\n')
            return

    def registration_menu(self):
        """
        This method prompts users to decide whether to proceed with deployment and 
        initialization of the smart contract. It then collects wallet credentials, 
        personal information, and role selection from the user for registration. 
        The method validates user inputs and interacts with the Controller to perform 
        registration actions.
        """

        while True:
            proceed = input("In order to register, you need to deploy. Do you want to proceed with deployment and initialization of the contract? (Y/n): ")
            if proceed.strip().upper() == "Y":
                self.act_controller.deploy_and_initialize('../../on_chain/HealthCareRecords.sol')
                break  # Exit the loop after deployment
            elif proceed.strip().upper() == "N":
                print("Deployment cancelled. Please deploy the contract when you are ready to register.")
                return  # Return from the function to cancel
            else:
                print('Wrong input, please insert Y or N!')

        print('Please, enter your wallet credentials.')
        attempts = 0
        while True:
            public_key = input('Public Key: ')
            private_key = input('Private Key: ')
            confirm_private_key = input('Confirm Private Key: ')
            
            if private_key == confirm_private_key:
                if self.controller.check_keys(public_key, private_key):
                    print('A wallet with these keys already exists. Please enter a unique set of keys.')
                    attempts += 1
                    if attempts >= 3:
                        print("Maximum retry attempts reached. Redeploying...")
                        self.act_controller.deploy_and_initialize('../../on_chain/HealthCareRecords.sol')
                        attempts = 0  # Reset attempts after deployment
                else:
                    try:
                        pk_bytes = decode_hex(private_key)
                        priv_key = keys.PrivateKey(pk_bytes)
                        pk = priv_key.public_key.to_checksum_address()
                        if pk.lower() != public_key.lower():
                            print('The provided keys do not match. Please check your entries.')
                        else:
                            break
                    except Exception:
                        print('Oops, there is no wallet with the matching public and private key provided.\n')
            else:
                print('Private key and confirmation do not match. Try again.\n')

        
        if is_address(public_key) and (public_key == pk):

            print('Enter your personal information.')

            while True:
                username = input('Username: ')
                if self.controller.check_username(username) == 0: break
                else: print('Your username has been taken.\n')

            while True:
                role = input("Insert your role: \n (C) if caregiver \n (M) if medic\n (P) if patient \n Your choice: ").strip().upper()
                if role == 'M':
                    user_role = 'MEDIC'
                    confirm = input("Do you confirm you're a Medic? (Y/n): ").strip().upper()
                    if confirm == 'Y':
                        break
                    else:
                        print("Role not confirmed. Retry\n")
                elif role == 'P':
                    user_role = 'PATIENT'
                    confirm = input("Do you confirm you're a Patient? (Y/n): ").strip().upper()
                    if confirm == 'Y':
                        break
                    else:
                        print("Role not confirmed. Retry\n")
                elif role == 'C':
                    user_role = 'CAREGIVER'
                    confirm = input("Do you confirm you're a Caregiver? (Y/n): ").strip().upper()
                    if confirm == 'Y':
                        break
                    else:
                        print("Role not confirmed. Retry\n")
                else:
                    print("You have to select a role between Caregiver (C), Medic (M) or Patient (P). Retry\n")
        
            while True:
                while True:
                    password = input('Password: ')
                    #password = getpass.getpass('Password: ')
                    passwd_regex = r'^.{8,50}$'
                    #passwd_regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,100}$'
                    if not re.fullmatch(passwd_regex, password):
                        print('Password must contain at least 8 characters, at least one digit, at least one uppercase letter, one lowercase letter, and at least one special character.\n')
                    else: break

                confirm_password = input('Confirm password: ')
                #confirm_password = getpass.getpass('Confirm Password: ')
                
                if password != confirm_password:
                    print('Password and confirmation do not match. Try again\n')
                else:
                    break

            reg_code = self.controller.registration(username, password, user_role, public_key, private_key)
            if reg_code == 0:
                print('You have succesfully registered!\n')
                if role == 'P':
                    self.insert_patient_info(username, user_role)
                elif role == 'M':
                    self.insert_medic_info(username, user_role)
                elif role == 'C':
                    self.insert_caregiver_info(username, user_role)
            elif reg_code == -1:
                print('Your username has been taken.\n')
        
        else:
            print('Sorry, but the provided public and private key do not match to any account\n')
            return 

    def insert_patient_info(self, username, role, autonomous_flag=1):
        """
        This method guides users through the process of providing personal information.
        It validates user inputs and ensures data integrity before inserting the 
        information into the system. Additionally, it registers the patient entity 
        on the blockchain.

        Args:
            username (str): The username of the patient.
            role (str): The role of the patient.
            autonomous_flag (bool): Flag indicating whether the patient is autonomous or not. Default set to 1.
        """

        print("Proceed with the insertion of a few personal information.")
        while True:
            name = input('Name: ')
            if self.controller.check_null_info(name): break
            else: print('Please insert information.')
        while True:
            lastname = input('Lastname: ')
            if self.controller.check_null_info(lastname): break
            else: print('Please insert information.')
        while True:
            birthday = input('Date of birth (YYYY-MM-DD): ')
            if self.controller.check_birthdate_format(birthday): break
            else: print("Invalid birthdate or incorrect format.")
        while True:
            birth_place = input('Birth place: ')
            if self.controller.check_null_info(birth_place): break
            else: print('Please insert information.')
        while True:
            residence = input('Place of residence: ')
            if self.controller.check_null_info(residence): break
            else: print('Please insert information.')
        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): 
                if self.controller.check_unique_phone_number(phone) == 0: break
                else: print("This phone number has already been inserted. \n")
            else: print("Invalid phone number format.\n")
        
        if autonomous_flag == 1:
            from_address_patient = self.controller.get_public_key_by_username(username)
            self.act_controller.register_entity('patient', name, lastname, autonomous_flag, from_address=from_address_patient)
        insert_code = self.controller.insert_patient_info(role, username, name, lastname, birthday, birth_place, residence, autonomous_flag, phone)
        if insert_code == 0:
            print('Information saved correctly!')
            if autonomous_flag == 1:
                self.patient_menu(username)
        elif insert_code == -1:
            print('Internal error!')

    def insert_medic_info(self, username, role):
        """
        This method assists medics in providing their personal information. It validates 
        user inputs and ensures data integrity before inserting the information into 
        the system. Additionally, it registers the medic entity on the blockchain.

        Args:
            username (str): The username of the medic.
            role (str): The role of the medic.
        """

        print("Proceed with the insertion of a few personal information.")
        while True:
            name = input('Name: ')
            if self.controller.check_null_info(name): break
            else: print('Please insert information.')
        while True:
            lastname = input('Lastname: ')
            if self.controller.check_null_info(lastname): break
            else: print('Please insert information.')
        while True:
            birthday = input('Date of birth (YYYY-MM-DD): ')
            if self.controller.check_birthdate_format(birthday): break
            else: print("Invalid birthdate or incorrect format.")
        while True:
            specialization = input('Specialization: ')
            if self.controller.check_null_info(specialization): break
            else: print('Please insert information.')
        while True:
            mail = input('E-mail: ')
            if self.controller.check_email_format(mail): 
                if self.controller.check_unique_email(mail) == 0: break
                else: print("This e-mail has already been inserted. \n")
            else: print("Invalid e-mail format.\n")

        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): 
                if self.controller.check_unique_phone_number(phone) == 0: break
                else: print("This phone number has already been inserted. \n")
            else: print("Invalid phone number format.\n")

        from_address_medic = self.controller.get_public_key_by_username(username)
        self.act_controller.register_entity('medic', name, lastname, specialization, from_address=from_address_medic)
        insert_code = self.controller.insert_medic_info(role, username, name, lastname, birthday, specialization, mail, phone)
        if insert_code == 0:
            print('Information saved correctly!')
            self.medic_menu(username)
        elif insert_code == -1:
            print('Internal error!')

    def insert_caregiver_info(self, username, role):
        """
        This method facilitates the process of caregivers providing their personal 
        information and the patient's information the are taking care of. It validates user inputs and ensures data 
        integrity before inserting the information into the system. Additionally, 
        it registers the caregiver entity on the blockchain.

        Args:
            username (str): The username of the caregiver.
            role (str): The role of the caregiver.
        """

        print("Proceed with the insertion of a few personal information.")
        while True:
            name = input('Name: ')
            if self.controller.check_null_info(name): break
            else: print('Please insert information.')
        while True:
            lastname = input('Lastname: ')
            if self.controller.check_null_info(lastname): break
            else: print('Please insert information.')
        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): 
                if self.controller.check_unique_phone_number(phone) == 0: break
                else: print("This phone number has already been inserted. \n")
            else: print("Invalid phone number format.\n")

        print('\nNow register patient information')
        while True:
            username_patient = input('Insert the patient username: ')
            if self.controller.check_username(username_patient) == 0: break
            else: print('Your username has been taken.\n')
        self.insert_patient_info(username_patient, "PATIENT", 0)

        while True:
            relationship = input('What kind of relationship there is between you and the patient: ')
            if self.controller.check_null_info(relationship): break
            else: print('Please insert information.')

        from_address_caregiver = self.controller.get_public_key_by_username(username)
        self.act_controller.register_entity('caregiver', name, lastname, from_address=from_address_caregiver)
        insert_code = self.controller.insert_caregiver_info(role, username, name, lastname, username_patient, relationship, phone)
        if insert_code == 0:
            print('Information saved correctly!\n')
            self.caregiver_menu(username)
        elif insert_code == -1:
            print('Internal error!')

    def login_menu(self):
        """
        This method prompts users to provide their credentials (public and private keys, 
        username, and password) for authentication. It verifies the credentials with 
        the Controller and grants access if authentication is successful. The method 
        handles authentication failures, including too many login attempts.

        Returns:
            int: An indicator of the login outcome (-1 for authentication failure, -2 for too many login attempts, 0 for successful login).
        """

        while True:
            if not self.controller.check_attempts() and self.session.get_timeout_left() < 0:
                self.session.reset_attempts()

            if self.session.get_timeout_left() <= 0 and self.controller.check_attempts():
                public_key = input('Insert public key: ')
                private_key = input('Insert private key: ')
                #private_key = getpass.getpass('Private Key: ')
                username = input('Insert username: ')
                passwd = input('Insert password: ')
                #passwd = getpass.getpass('Insert password: ')

                login_code, user_type = self.controller.login(username, passwd, public_key, private_key)

                if login_code == 0:
                    print('\nYou have succesfully logged in!\n')
                    if user_type == "MEDIC":
                        self.medic_menu(username)
                        return
                    elif user_type == "CAREGIVER":
                        self.caregiver_menu(username)
                        return
                    elif user_type == "PATIENT":
                        self.patient_menu(username)
                        return
                    else:
                        print("Error: User type is not recognized.")
                        return -1
                elif login_code == -1:
                    print('\nThe credentials you entered are wrong\n')
                elif login_code == -2:
                    print('\nToo many login attempts\n')
                    return -1
                
            else:
                print('\nMax number of attemps reached\n')
                print(f'You will be in timeout for: {int(self.session.get_timeout_left())} seconds\n')
                return -2

    #Homepages
    #Medic
    def medic_menu(self, username):
        """
        This method presents medics with a menu of options tailored to their role. 
        It allows medics to choose actions such as selecting a patient, viewing or 
        updating their profile, changing their password, or logging out. The method 
        handles user input validation and directs users to the corresponding functionality 
        based on their choice.

        Args:
            username (str): The username of the logged-in medic.
        """

        medic_options = {
            1: "Choose patient",
            2: "View profile",
            3: "Update profile",
            4: "Change password",
            5: "Log out"
        }

        while True:
            print("\nMENU")                           
            for key, value in medic_options.items():
                print(f"{key} -- {value}")
                                                
            try:                                    
                choice = int(input("Choose an option: "))
                if choice in medic_options:
                    if choice == 1:
                        self.util.display_records(username)

                    elif choice == 2:
                        self.view_medicview(username)

                    elif choice == 3:                           
                        self.util.update_profile(username, "Medic")
                
                    elif choice == 4:
                        self.util.change_passwd(username)

                    elif choice == 5:
                        confirm = input("\nDo you really want to leave? (Y/n): ").strip().upper()
                        if confirm == 'Y':
                            print("\nThank you for using the service!\n")
                            self.session.reset_session()
                            return
                        else:
                            print("Invalid choice! Please try again.")

            except ValueError:
                print("Invalid Input! Please enter a valid number.")

    #Caregiver
    def caregiver_menu(self, username):
        """
        This method presents caregivers with a menu of options tailored to their role. 
        It allows caregivers to choose actions such as consulting medical data, viewing 
        or updating their profile, viewing patient profiles, changing their password, 
        or logging out. The method handles user input validation and directs users 
        to the corresponding functionality based on their choice.

        Args:
            username (str): The username of the logged-in caregiver.
        """

        while True:
            caregiver = self.controller.get_user_by_username(username)
            patient_name = caregiver.get_username_patient()

            caregiver_options = {
                        1: "Consult {}{} medical data".format(patient_name, self.controller.possessive_suffix(patient_name)),
                        2: "View your profile",
                        3: "Update your profile",
                        4: "View {}{} profile".format(patient_name, self.controller.possessive_suffix(patient_name)),
                        5: "Update {}{} profile".format(patient_name, self.controller.possessive_suffix(patient_name)),
                        6: "Change password",
                        7: "Log out"
                    }

            print("\nMENU")                           
            for key, value in caregiver_options.items():
                print(f"{key} -- {value}")        

            try:                                    
                choice = int(input("Choose an option: "))
                
                if choice == 1:
                    self.util.patient_medical_data(patient_name)

                elif choice == 2:
                    self.view_caregiverview(username)

                elif choice == 3:
                    self.util.update_profile(username, "Caregiver")

                elif choice == 4:
                    self.view_patientview(patient_name)

                elif choice == 5:
                    self.util.update_profile(patient_name, "Patient")

                elif choice == 6:
                    self.util.change_passwd(username)
            
                elif choice == 7:                           
                    confirm = input("Do you really want to leave? (Y/n): ").strip().upper()
                    if confirm == 'Y':
                        print("Thank you for using the service!")
                        self.session.reset_session()
                        return
                    else:
                        print("Returning to the caregiver menu...")

                else:
                        print("Invalid choice! Please try again.")

            except ValueError:
                    print("Invalid Input! Please enter a valid number.")
            
    #Patient
    def patient_menu(self, username):
        """
        This method presents patients with a menu of options tailored to their role. 
        It allows patients to choose actions such as consulting medical data, viewing 
        or updating their profile, changing their password, or logging out. The method 
        handles user input validation and directs users to the corresponding functionality 
        based on their choice.

        Args:
            username (str): The username of the logged-in patient.
        """

        while True: 
            patient_options = {
                1: "Consult medic data",
                2: "View profile",
                3: "Update profile",
                4: "Change password",
                5: "Log out"
            }
            print("\nMENU")
            for key, value in patient_options.items():
                print(f"{key} -- {value}")

            try:
                choice = int(input('Enter your choice: '))

                if choice == 1:
                    self.util.patient_medical_data(username)
                    
                elif choice == 2:
                    self.view_patientview(username)

                elif choice == 3:
                    self.util.update_profile(username, "Patient") 

                elif choice == 4:
                    self.util.change_passwd(username)

                elif choice == 5:
                    print('Bye Bye!')
                    self.session.reset_session()
                    return
                else:
                    print('Wrong option. Please enter one of the options listed in the menu!')

            except ValueError:
                print('Wrong input. Please enter a number!')
    
    def view_patientview(self, username):
        """
        This method retrieves and displays the profile information of the patient 
        identified by the given username. It presents details such as username, name, 
        lastname, birthday, birth place, residence, autonomous status, and phone number.

        Args:
            username (str): The username of the patient whose profile is to be viewed.
        """

        patientview = self.controller.get_user_by_username(username)
        print("\nPATIENT INFO\n")
        print("Username: ", patientview.get_username())
        print("Name: ", patientview.get_name())
        print("Last Name: ", patientview.get_lastname())
        print("Birthday: ", patientview.get_birthday())
        print("Birth Place: ", patientview.get_birth_place())
        print("Residence: ", patientview.get_residence())
        print("Phone: ", patientview.get_phone())
        input("\nPress Enter to exit\n")

    def view_caregiverview(self, username):
        """
        This method retrieves and displays the profile information of the caregiver 
        identified by the given username. It presents details such as username, name, 
        lastname, associated patient's username, relationship with the patient, and 
        phone number.

        Args:
            username (str): The username of the caregiver whose profile is to be viewed.
        """

        caregiverview = self.controller.get_user_by_username(username)
        print("\nCAREGIVER INFO\n")
        print("Username: ", caregiverview.get_username())
        print("Name: ", caregiverview.get_name())
        print("Lastname: ", caregiverview.get_lastname())
        print("Patient Username: ", caregiverview.get_username_patient())
        print("Patient relationship: ", caregiverview.get_relationship())
        print("Phone: ", caregiverview.get_phone())
        input("\nPress Enter to exit\n")

    def view_medicview(self, username):
        """
        This method retrieves and displays the profile information of the medic 
        identified by the given username. It presents details such as username, name, 
        lastname, birthday, specialization, email, and phone number.

        Args:
            username (str): The username of the medic whose profile is to be viewed.
        """

        medicview = self.controller.get_user_by_username(username)
        print("\nMEDIC INFO\n")
        print("Username: ", medicview.get_username())
        print("Name: ", medicview.get_name())
        print("Lastname: ", medicview.get_lastname())
        print("Birthday: ", medicview.get_birthday())
        print("Specialization: ", medicview.get_specialization())
        print("E-mail: ", medicview.get_mail())
        print("Phone: ",medicview.get_phone())
        input("\nPress Enter to exit\n")
