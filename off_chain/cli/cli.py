class CommandLineInterface:
    
    def __init__(self):
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
        return 
    
    def login_menu(self):
        return