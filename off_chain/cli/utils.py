import re
import click

from controllers.controller import Controller
from session.session import Session

class Utils:

    def __init__(self, session: Session):

        self.controller = Controller(session)

    def change_passwd(self, username):

        while True:
            confirmation = input("Do you want to change your password (Y/n): ").strip().upper()
            if confirmation == 'Y':
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
            else:
                print("Okay\n")
                return
            

            
    def update_profile(self, username, role):
        us = self.controller.get_user_by_username(username)

        if role == "Patient":

            us.set_name(click.prompt('Name ', default=us.get_name()))
            us.set_lastname(click.prompt('Lastname ', default=us.get_lastname())) 
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
  
            print("\nEnter your new Information...")
            us.set_name(click.prompt('Name ', default=us.get_name()))
            us.set_lastname(click.prompt('Lastname ', default=us.get_lastname()))
            while True:
                phone = click.prompt('Phone ', default=us.get_phone())
                if self.controller.check_phone_number_format(phone): 
                    us.set_phone(phone)
                    break
                else: print("Invalid phone number format.")


        elif role == "Medic":
            
            us.set_name(click.prompt('Name ', default=us.get_name()))
            us.set_lastname(click.prompt('Lastname ', default=us.get_lastname()))
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