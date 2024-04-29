import getpass
import re

import click
from eth_utils import *
from eth_keys import *
from controllers.controller import Controller
from session.session import Session
from db.db_operations import DatabaseOperations
import re

class CommandLineInterface:
    def __init__(self, session: Session):

        self.controller = Controller(session)
        self.session = session
        self.ops = DatabaseOperations()

        self.menu = {
            1: 'Register New Account',
            2: 'Log In',
            3: 'Exit',
        }

    def print_menu(self):

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
        print('Please, enter your wallet credentials.')

        while True:
            public_key = input('Public Key: ')
            private_key = input('Private Key: ')
            confirm_private_key = input('Confirm Private Key: ')
            #private_key = getpass.getpass('Private Key: ')
            #confirm_private_key = getpass.getpass('Confirm Private Key: ')
            if private_key == confirm_private_key:
                if not self.controller.check_keys(public_key, private_key):
                    break
                else:
                    print('A wallet with these keys already exists. Please enter a unique set of keys.')
            else:
                print('Private key and confirmation do not match. Try again.\n')

        try:
            pk_bytes = decode_hex(private_key)
            priv_key = keys.PrivateKey(pk_bytes)
            pk = priv_key.public_key.to_checksum_address()
            if pk.lower() != public_key.lower():
                print('The provided keys do not match. Please check your entries.')
                return
        except Exception:
            print('Oops, there is no wallet with the matching public and private key provided.\n')
            return
        
        if is_address(public_key) and (public_key == pk):

            print('Enter your personal informations.')

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
                password = input('Password: ')
                #password = getpass.getpass('Password: ')
                passwd_regex = r'^.{8,50}$'
                #passwd_regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,100}$'
                if not re.fullmatch(passwd_regex, password):
                    print('Password must contain at least 8 characters, at least one digit, at least one uppercase letter, one lowercase letter, and at least one special character.\n')
                
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

        # if autonomous_flag == 0:
        #     print('Please, enter {}{} wallet credentials.'.format(username, self.possessive_suffix(username)))

        #     while True:
        #         public_key = input('Insert {}{} public Key: '.format(username, self.possessive_suffix(username)))
        #         private_key = input('Insert {}{} private Key: '.format(username, self.possessive_suffix(username)))
        #         confirm_private_key = input('Confirm {}{} private Key: '.format(username, self.possessive_suffix(username)))
        #         #private_key = getpass.getpass('Insert {}{} private Key: '.format(username, self.possessive_suffix(username)))
        #         #confirm_private_key = getpass.getpass('Confirm {}{} private Key: '.format(username, self.possessive_suffix(username)))
        #         if private_key == confirm_private_key:
        #             if not self.controller.check_keys(public_key, private_key):
        #                 break
        #             else:
        #                 print('A wallet with these keys already exists. Please enter a unique set of keys.')
        #         else:
        #             print('Private key and confirmation do not match. Try again.\n')
        #     try:
        #         pk_bytes = decode_hex(private_key)
        #         priv_key = keys.PrivateKey(pk_bytes)
        #         pk = priv_key.public_key.to_checksum_address()
        #         if pk.lower() != public_key.lower():
        #             print('The provided keys do not match. Please check your entries.')
        #             return
        #     except Exception:
        #         print('Oops, there is no wallet with the matching public and private key provided.\n')
        #         return
            
        #     if is_address(public_key) and (public_key == pk):
        #         while True:
        #             password = input('Insert {}{} password: '.format(username, self.possessive_suffix(username)))
        #             #password = getpass.getpass('Insert {}{} password: '.format(username, self.possessive_suffix(username)))
        #             passwd_regex = r'^.{8,50}$'
        #             #passwd_regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,100}$'
        #             if not re.fullmatch(passwd_regex, password):
        #                 print('Password must contain at least 8 characters, at least one digit, at least one uppercase letter, one lowercase letter, and at least one special character.\n')
                    
        #             confirm_password = input('Confirm {}{} password: '.format(username, self.possessive_suffix(username)))
        #             #confirm_password = getpass.getpass('Confirm {}{} password: '.format(username, self.possessive_suffix(username)))
                    
        #             if password != confirm_password:
        #                 print('Password and confirmation do not match. Try again\n')
        #             else:
        #                 break
                
        #         reg_code = self.controller.registration(username, password, role, public_key, private_key)

        #         if reg_code == 0:
        #             print('You have succesfully registered {}{} account!\n'.format(username, self.possessive_suffix(username)))
        #             print("Proceed with the insertion of a few {}{} personal information.".format(username, self.possessive_suffix(username)))
        # if autonomous_flag == 1:
        #     print("Proceed with the insertion of a few personal information.")
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        while True:
            birthday = input('Date of birth (YYYY-MM-DD): ')
            if self.controller.check_birthdate_format(birthday): break
            else: print("Invalid birthdate or incorrect format.")

        birth_place = input('Birth place: ')
        residence = input('Place of residence: ')
        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): break
            else: print("Invalid phone number format.")

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
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        while True:
            birthday = input('Date of birth (YYYY-MM-DD): ')
            if self.controller.check_birthdate_format(birthday): break
            else: print("Invalid birthdate or incorrect format.")

        specialization = input('Specialization: ')
        while True:
            mail = input('Mail: ')
            if self.controller.check_email_format(mail): break
            else: print("Invalid email format.")

        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): break
            else: print("Invalid phone number format.")

        from_address_medic = self.controller.get_public_key_by_username(username)
        self.act_controller.register_entity('medic', name, lastname, specialization, from_address=from_address_medic)
        insert_code = self.controller.insert_medic_info(role, username, name, lastname, birthday, specialization, mail, phone)
        if insert_code == 0:
            print('Information saved correctly!')
            self.medic_menu(username)
        elif insert_code == -1:
            print('Internal error!')

    def insert_caregiver_info(self, username, role):
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        # while True:
        #         username_patient = input('Enter the username of the patient you are taking care of: ')
        #         if self.controller.check_patient_by_username(username_patient) == -1: break
        #         else:
        #             print('A patient named ' + str(username_patient) + ' does not exist.')
        #             confirm = input("Do you want to create a new Patient account? (Y/n): ").strip().upper()
        #             if confirm == 'Y':
        #                 confirm = input("Do yu want to keep '{}' as the Patient's username? (Y/n): ".format(username_patient)).strip().upper()
        #                 if confirm != 'Y':
        #                     new_value = input("Insert the new username (press Enter to mantain '{}'): ".format(username_patient))
        #                     username_patient = new_value if new_value else username_patient

        #                 self.insert_patient_info(username_patient, "PATIENT", 0) 
        #                 print("Let's continue with your information.")
        #                 break

        relationship = input('What kind of relationship there is between you and the patient: ')

        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): break
            else: print("Invalid phone number format.")

        print('Now register patient information')
        while True:
            username_patient = input('Insert the patient username: ')
            if self.controller.check_username(username_patient) == 0: 
                break
            else: 
                print('Your username has been taken.\n')
            self.insert_patient_info(username_patient, "PATIENT", 0)

        from_address_caregiver = self.controller.get_public_key_by_username(username)
        self.act_controller.register_entity('caregiver', name, lastname, from_address=from_address_caregiver)
        insert_code = self.controller.insert_caregiver_info(role, username, name, lastname, username_patient, relationship, phone)
        if insert_code == 0:
            print('Information saved correctly!\n')
            self.caregiver_menu(username)
        elif insert_code == -1:
            print('Internal error!')
       
    def login_menu(self):

        if not self.controller.check_attempts() and self.session.get_timeout_left() < 0:
            self.session.reset_attempts()

        if self.session.get_timeout_left() <= 0 and self.controller.check_attempts():
            public_key = input('Insert public key:')
            private_key = input('Insert private key:')
            #private_key = getpass.getpass('Private Key: ')
            username = input('Insert username: ')
            passwd = input('Insert password: ')
            #passwd = getpass.getpass('Insert password: ')

            login_code, user_type = self.controller.login(username, passwd, public_key, private_key)

            if login_code == 0:
                print('\nYou have succesfully logged in!\n')
                if user_type == "MEDIC":
                    self.medic_menu(username)
                elif user_type == "CAREGIVER":
                    self.caregiver_menu(username)
                elif user_type == "PATIENT":
                    self.patient_menu()
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
        medic_options = {
            1: "Choose patient",
            2: "Update profile",
            3: "Change password",
            4: "Exit"
        }

        while True:
            print("MENU")                           
            for key, value in medic_options.items():
                print(f"{key} -- {value}")
                                                
            try:                                    
                choice = int(input("Choose an option: "))
                if choice in medic_options:
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Invalid Input! Please enter a valid number.")




        # RITORNA TUTTI I PAZIENTI DI QUEL DOTTORE;
        # SE VOGLIAMO CHE UN DOC POSSA VISUALIZZARE TUTTI I PAZIENTI, ELIMINARE ROBA RELATIVA A username
        if choice == 1:
            print("Choose patient: \n")
            #patients = self.controller.get_patients_for_doctor(username)
            patients = self.controller.get_patients()

            if not patients:
                print("There are no patients in the system.")
                return
            print("List of patients:")
            for patient in patients:
                print(f"{patient[1]} - {patient[2]} {patient[3]}")






        elif choice == 2:                           
            print("Update profile function")
            self.update_profile(username, "Medic")
    
        elif choice == 3:
            self.change_passwd(username)

        elif choice == 4:
            confirm = input("Do you really want to leave? (Y/n): ").strip().upper()
            if confirm == 'Y':
                print("Thank you for using the service!")
                exit()

    #Caregiver (bozza)
    def caregiver_menu(self, username):
        while True:
            caregiver = self.controller.get_user_by_username(username)

            # Ottieni il nome del caregiver
            patient_name = caregiver.get_username_patient()

            caregiver_options = {
                        1: "Consult {}{} medical data".format(patient_name, self.possessive_suffix(patient_name)),
                        2: "Update your profile",
                        3: "Update {}{} profile".format(patient_name, self.possessive_suffix(patient_name)),
                        4: "Change password",
                        5: "Exit"
                    }

            print("\nMENU")                           
            for key, value in caregiver_options.items():
                print(f"{key} -- {value}")        

            try:                                    
                choice = int(input("Choose an option: "))
                
                if choice == 1:
                    self.patient_medical_data(patient_name)

                elif choice == 2:
                    self.update_profile(username, "Caregiver")

                elif choice == 3:
                    self.update_profile(patient_name, "Patient")

                elif choice == 4:
                    self.change_passwd(username)
            
                elif choice == 5:                           
                    confirm = input("Do you really want to leave? (Y/n): ").strip().upper()
                    if confirm == 'Y':
                        print("Thank you for using the service!")
                        exit()
                    else:
                        print("Returning to the caregiver menu...")

                else:
                        print("Invalid choice! Please try again.")

            except ValueError:
                    print("Invalid Input! Please enter a valid number.")
            
    def patient_menu(self, username):
        user = self.session.get_user()

        while True: 
            patient_options = {
                1: "Consult medic data",
                2: "View profile",
                3: "Update profile",
                4: "Change password",
                5: "Exit"
            }
            print("\nMENU")
            for key, value in patient_options.items():
                print(f"{key} -- {value}")

            try:
                choice = int(input('Enter your choice: '))

                if choice == 1:
                    self.patient_medical_data(user.username)
                    
                elif choice == 2:
                    self.view_patientview(user.username)

                elif choice == 3:
                    self.update_profile(user.username, "Patient") 

                elif choice == 4:
                    self.change_passwd(user.username)

                elif choice == 5:
                    print('Bye Bye!')
                    exit()
                else:
                    print('Wrong option. Please enter one of the options listed in the menu!')

            except ValueError:
                print('Wrong input. Please enter a number!')
            

    def change_passwd(self, username):

        while True:
            confirmation = input('Do you want to change your password (Y/N)?')
            if confirmation == 'Y' or confirmation == 'y':
                old_pass = input('Old Password: ')

                if not self.controller.check_passwd(username, old_pass):
                    print('\nYou entered the wrong old password.\n')
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
                            break

                    response = self.controller.change_passwd(username, old_pass, new_passwd)
                    if response == 0:
                        print('\nPassword changed correctly!\n')
                    elif response == -1 or response == -2:
                        print('\nSorry, something went wrong!\n')
                return

    def update_profile(self, username, role):
        us = self.controller.get_user_by_username(username)
        # PAZIENTE
        if role == "Patient":
            
            # patient_info = self.controller.get_patient_info(username)
            # if not patient_info:
            #     print("user not found.")
            #     return

            us.set_name(click.prompt('Name ', default=us.get_name()))
            us.set_lastname(click.prompt('Lastname ', default=us.get_lastaname())) 
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

        elif role == "Caregiver":
            # caregiver_info = self.controller.get_caregiver_info(username)
            # if not caregiver_info:
            #     print("user not found.")
            #     return
            
            print("\nEnter your new informations...")
            us.set_name(click.prompt('Name ', default=us.get_name()))
            us.set_lastname(click.prompt('Lastname ', default=us.get_lastname()))
            while True:
                phone = click.prompt('Phone ', default=us.get_phone())
                if self.controller.check_phone_number_format(phone): 
                    us.set_phone(phone)
                    break
                else: print("Invalid phone number format.")


        elif role == "Medic":
            # medic_info = self.controller.get_medic_info(username)
            # if not medic_info:
            #     print("user not found.")
            #     return
            
            us.set_name(click.prompt('Name ', default=us.get_name()))
            us.set_lastname(click.prompt('Lastname ', default=us.get_lastaname()))
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
        us.save()

    def patient_medical_data(self, username):
        while True: 
            print("\nMEDICAL DATA")
            print('\nWhich type of data do you want to consult?')
            print("1 -- Treatment plan")
            print("2 -- Reports") 
            print("3 -- Undo") 
            
            try:
                choice = int(input('Enter your choice: '))

                if choice == 1:
                    self.view_treatmentplan(username)

                if choice == 2:
                    self.view_reportslist_patient(username) # finire

                if choice == 3:
                    return
                
                else:
                    print('Wrong option. Please enter one of the options listed in the menu!')

            except ValueError:
                print('Wrong input. Please enter a number!')

    def view_treatmentplan(self, username):     # checkare che esista il piano di cura
        treatmentplan = self.controller.get_treatmentplan_by_username(username)
        medic = self.controller.get_medic_by_id(treatmentplan.get_id_medic())
        print("\nTREATMENT PLAN\n")
        print("Start: ", treatmentplan.get_start_date())
        print("Finish: ", treatmentplan.get_end_date())
        print("Medic: ", medic.get_name(), " ", medic.get_lastname())
        print("Description: ", treatmentplan.get_description())
        input("\nPress Enter to exit\n")

    
    #Patient view
    def view_patientview(self, username):
        patientview = self.controller.get_user_by_username(username)
        print("\nPATIENT INFO\n")
        print("Username: ", patientview.get_username())
        print("Name: ", patientview.get_name())
        print("Last Name: ", patientview.get_lastaname())
        print("Birthday: ", patientview.get_birthday())
        print("Birth Place: ", patientview.get_birth_place())
        print("Residence: ", patientview.get_residence())
        print("Autonomous: ", patientview.get_autonomous())
        print("Phone: ", patientview.get_phone())
        input("\nPress Enter to exit\n")

    def view_caregiverview(self, username):
        caregiverview = self.controller.get_user_by_username(username)
        print("\nCAREGIVER INFO\n")
        print("Username: ", caregiverview.get_username())
        print("Name: ", caregiverview.get_name())
        print("Lastname: ", caregiverview.get_lastname())
        print("Patient Username: ", caregiverview.username_patient())
        print("Patient realltionship: ", caregiverview.get_patient_relationship())
        print("Caregiver phone: ", caregiverview.get_phone())
        input("\nPress Enter to exit\n")

    def view_medicview(self, username):
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
      
    #sviluppare visualizzazione

    def view_reportslist_patient(self, username):
        while True:

            reports_list = self.controller.get_reports_list_by_username(username)
            print("\nELENCO REPORTS\n")
            for i, report in enumerate(reports_list, 1):
                print(f"{i}. {report.get_analyses()}")
            print(f"{i+1}. Undo")
            try:
                choice = int(input("Chose an option: "))-1
                if choice in {indice for indice, _ in enumerate(reports_list)}:
                    print("\nREPORT")
                    print("\nAnalysis: ", reports_list[choice].get_analyses())
                    print("Diagnosis: ", reports_list[choice].get_diagnosis())
                    input("Press Enter to exit")
                elif choice==i:
                    return  
                else:
                    print('Wrong option. Please enter one of the options listed in the menu!')
            except ValueError:
                            print('Wrong input. Please enter a number!')

# Determina se il nome del caregiver termina con una lettera diversa da 's'
    def possessive_suffix(self, name):
        if name[-1].lower() != 's':
            return"'s"
        else:
            return "'"


    # OPERATIONS 

    # Read_patient's_data 
    # Write_patient's_data
    # Modify_patient's_data
    # Read_my_data
    # Write_my_data
    # Update_my_profile
    # Update_someone's_profile