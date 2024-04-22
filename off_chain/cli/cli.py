import getpass
import re

from eth_utils import *
from eth_keys import *
from controllers.controller import Controller
from session.session import Session
import re

class CommandLineInterface:
    def __init__(self, session: Session):

        self.controller = Controller(session)
        self.session = session

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
        public_key = input('Public Key: ')

        while True:
            private_key = input('Private Key: ')
            confirm_private_key = input('Confirm Private Key: ')
            #private_key = getpass.getpass('Private Key: ')
            #confirm_private_key = getpass.getpass('Confirm Private Key: ')
            if private_key == confirm_private_key:
                break
            else:
                print('Private key and confirmation do not match. Try again.\n')

        try:
            pk_bytes = decode_hex(private_key)
            priv_key = keys.PrivateKey(pk_bytes)
            pk = priv_key.public_key.to_checksum_address()
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
                role = input("Insert your role: \n (C) if caregiver \n (M) if medic\n (P) if patient \n ").strip().upper()
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
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        while True:
            birthday = input('Date of birth (YYYY-MM-DD): ')
            if self.controller.check_birthdate_format(birthday): break
            else: print("Invalid birthdate or incorrect format.")

        birth_place = input('Birth place: ')
        residence = input('Place of residence: ')
        #while True:
        #    autonomous_flag = int(input('Are you autonomous? (Digit "1" if you are autonomous, "0" if you are not)'))
        #    if autonomous_flag  in [0,1]:
        #        break
        #    else:
        #        print('Wrong value! Insert a valid value please.')
        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): break
            else: print("Invalid phone number format.")

        insert_code = self.controller.insert_patient_info(role, username, name, lastname, birthday, birth_place, residence, autonomous_flag, phone)
        if insert_code == 0:
            print('Information saved correctly!')
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

        insert_code = self.controller.insert_medic_info(role, username, name, lastname, birthday, specialization, mail, phone)
        if insert_code == 0:
            print('Information saved correctly!')
        elif insert_code == -1:
            print('Internal error!')

    def insert_caregiver_info(self, username, role):
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        while True:
                username_patient = input('Enter the username of the patient you are taking care of: ')
                if self.controller.check_patient_by_username(username_patient) == -1: break
                else:
                    print('A patient named ' + str(username_patient) + ' does not exist.')
                    confirm = input("Do you want to create a new Patient account? (Y/n): ").strip().upper()
                    if confirm == 'Y':
                        confirm = input("Do yu want to keep '{}' as the Patient's username? (Y/n): ".format(username_patient)).strip().upper()
                        if confirm != 'Y':
                            new_value = input("Insert the new username (press Enter to mantain '{}'): ".format(username_patient))
                            username_patient = new_value if new_value else username_patient
                        self.insert_patient_info(username_patient, "Patient", 0) 
                        print("Let's continue with your information.")
                        break

        relationship = input('What kind of relationship there is between you and the patient: ')

        while True:
            phone = input('Phone number: ')
            if self.controller.check_phone_number_format(phone): break
            else: print("Invalid phone number format.")

        insert_code = self.controller.insert_caregiver_info(role, username, name, lastname, username_patient, relationship, phone)
        if insert_code == 0:
            print('Information saved correctly!\n \n ')
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

            login_code = self.controller.login(username, passwd, public_key, private_key)

            if login_code == 0:
                print('\nYou have succesfully logged in!\n')
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
    def medic_menu(self):
        medic_options = {
            1: "Choose patient",
            2: "Update profile",
            3: "Exit"
        }

        while True:
            print("MENU")                           # Stampa il menù
            for key, value in medic_options.items():
                print(f"{key} -- {value}")
                                                
            try:                                    # Richiesta input e gestione errori
                choice = int(input("Choose an option: "))
                if choice in medic_options:
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Invalid Input! Please enter a valid number.")
                
        if choice == 1:
            print("Visualize medical data")         # Gestisce la scelta dell'utente
            self.controller.menu_one(self)
       
        elif choice == 2:                           # Inserisci qui il codice per la gestione dei pazienti
            print("Update profile function")
            self.controller.menu_two(self)
    
        elif choice == 3:                           # Inserisci qui il codice per l'aggiornamento del profilo
            confirm = input("Do you really want to leave? (Y/n): ").strip().upper()
            if confirm == 'Y':
                print("Thank you for using the service!")
                exit()

    #Caregiver (bozza)
    def caregiver_menu(self, username):
        while True:
            # GET USER BY USERNAME!
            caregiver = self.controller.get_user_by_username(username, "caregiver")
            print(caregiver)

            # Ottieni il nome del caregiver
            patient_name = caregiver[1]

            # Determina se il nome del caregiver termina con una lettera diversa da 's'
            if patient_name[-1].lower() != 's':
                possessive_suffix = "'s"
            else:
                possessive_suffix = "'"

            caregiver_options = {
                        1: "Choose patient",
                        2: "Update {}{} profile".format(patient_name, possessive_suffix),
                        #2: "Update patient profile",
                        3: "Exit"
                    }

            print("MENU")                           # Stampa il menù
            for key, value in caregiver_options.items():
                print(f"{key} -- {value}")

            try:                                    # Richiesta input e gestione errori
                choice = int(input("Choose an option: "))
                if choice in caregiver_options:
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Invalid Input! Please enter a valid number.")
                
        if choice == 1:
            print("Visualize medical data")         # Gestisce la scelta dell'utente
            self.controller.menu_one(self)
       
        elif choice == 2:                           # Inserisci qui il codice per la gestione dei pazienti
            print("Update profile function")
            self.controller.menu_two(self)
    
        elif choice == 3:                           # Inserisci qui il codice per l'aggiornamento del profilo
            confirm = input("Do you really want to leave? (Y/n): ").strip().upper()
            if confirm == 'Y':
                print("Thank you for using the service!")
                exit()
            
    #Patient (bozza)
    def patient_menu(self):

        while True: 

            patient_options = {
                1: "Consult medic data",
                2: "Updade profile",
                3: "Exit"
            }
            print("MENU")
            for key, value in patient_options.items():
                print(f"{key} -- {value}")

            try:
                choice = int(input('Enter your choice: '))

                if choice == 1:
                    print('Which type of data do you want to consult?')
                    print("1 -- Treatment plan")
                        # view treatment plan
                    print("2 -- Reports")
                        # view list and select report
                            # view report
                    print("3 -- Undo") 
                        # menu

                elif choice == 2:
                    print('Which type of data do you want to modify?')
                    print("1 -- Username")
                    print("2 -- Name")
                    print("3 -- Last name")
                    # other
                    # undo

                elif choice == 3:
                    print('Bye Bye!')
                    exit()
                else:
                    print('Wrong option. Please enter one of the options listed in the menu!')

            except ValueError:
                print('Wrong input. Please enter a number!\n')
                return



    # OPERATIONS 

    # Read_patient's_data
    # Write_patient's_data
    # Modify_patient's_data
    # Read_my_data
    # Write_my_data
    # Update_my_profile
    # Update_someone's_profile