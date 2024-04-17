import getpass
import re

from eth_utils import *
from eth_keys import *
from controllers.controller import Controller
from session.session import Session

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
                self.login_menu()
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

            username = input('Username: ')

            while True:
                role = input('Role: ').upper()

                roles = ['MEDIC', 'PATIENT', 'CAREGIVER']

                if not role in roles:
                    print('You have to select a role between Medic, Patient or Caregiver')
                else:
                    break

            while True:
                password = input('Password: ')
                confirm_password = input('Confirm password: ')
                #password = getpass.getpass('Password: ')
                #confirm_password = getpass.getpass('Confirm Password: ')
                
                passwd_regex = r'^.{8,50}$'
                #passwd_regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,100}$'
                
                if not re.fullmatch(passwd_regex, password):
                    print('Password must contain at least 8 characters, at least one digit, at least one uppercase letter, one lowercase letter, and at least one special character.\n')
                elif password != confirm_password:
                    print('Password and confirmation do not match. Try again\n')
                else:
                    break

            reg_code = self.controller.registration(username, password, role, public_key, private_key)
            if reg_code == 0:
                print('You have succesfully registered!\n')
                if role == 'PATIENT':
                    self.insert_patient_info()
                elif role == 'MEDIC':
                    self.insert_medic_info()
                elif role == 'CAREGIVER':
                    self.insert_caregiver_info()
            elif reg_code == -1:
                print('Your username has been taken.\n')
            elif reg_code == -2:
                print('Internal error!')
        
        else:
            print('Sorry, but the provided public and private key do not match to any account\n')
            return

    def insert_patient_info(self):
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        birthday = input('Date of birth: ')
        birth_place = input('Birth place:')
        residence = input('Place of residence:')
        while True:
            autonomous_flag = int(input('Are you autonomous? (Digit "1" if you are autonomous, "0" if you are not)'))
            if autonomous_flag  in [0,1]:
                break
            else:
                print('Wrong value! Insert a valid value please.')
        phone = input('Phone number: ')

        insert_code = self.controller.insert_patient_info(name, lastname, birthday, birth_place, residence, autonomous_flag, phone)
        if insert_code == 0:
            print('Information saved correctly!')
        elif insert_code == -1:
            print('Internal error!')

    def insert_medic_info(self):
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        birthday = input('Date of birth: ')
        specialization = input('Specialization: ')
        mail = input('Mail: ')
        phone = input('Phone number: ')

        insert_code = self.controller.insert_medic_info(name, lastname, birthday, specialization, mail, phone)
        if insert_code == 0:
            print('Information saved correctly!')
        elif insert_code == -1:
            print('Internal error!')
 

    def insert_caregiver_info(self):
        print("Proceed with the insertion of a few personal information.")
        name = input('Name: ')
        lastname = input('Lastname: ')
        id_patient = int(input('Enter the ID of the patient you are taking care of: '))
        relationship = input('What kind of relationship there is between you and the patient: ')
        phone = input('Phone number: ')

        insert_code = self.controller.insert_caregiver_info(name, lastname, id_patient, relationship, phone)
        if insert_code == 0:
            print('Information saved correctly!')
        elif insert_code == -1:
            print('Internal error!')
       
    
    def login_menu(self):
        return