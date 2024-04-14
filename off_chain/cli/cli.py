import getpass
import re

from eth_utils import *
from eth_keys import *
from controllers.controller import Controller

class CommandLineInterface:
    def __init__(self):

        self.controller = Controller()

        self.menu = {
            1: 'Register New Account',
            2: 'Log In',
            3: 'Exit',
        }

    def print_menu(self):
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
            private_key = getpass.getpass('Private Key: ')
            confirm_private_key = getpass.getpass('Confirm Private Key: ')
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
                    role = input('Role: ').lower()

                    roles = ['medic', 'patient', 'caregiver']

                    if not role in roles:
                        print('You have to select a role between Medic, Patient or Caregiver')
                    else:
                        break

                while True:
                    password = getpass.getpass('Password: ')
                    confirm_password = getpass.getpass('Confirm Password: ')

                    passwd_regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,100}$'
                    
                    if not re.fullmatch(passwd_regex, password):
                        print('Password must contain at least 8 characters, at least one digit, at least one uppercase letter, one lowercase letter, and at least one special character.\n')
                    elif password != confirm_password:
                        print('Password and confirmation do not match. Try again\n')
                    else:
                        break

                    reg_code = self.controller.registration(username, password, role, public_key, private_key)
                    if reg_code == 0:
                        print('You have succesfully registered!\n')
                    elif reg_code == -1:
                        print('Your username has been taken.\n')
                    elif reg_code == -2:
                        print('Internal error!')
            
            else:
                print('Sorry, but the provided public and private key do not match to any account\n')
                return

                
    
    def login_menu(self):
        return