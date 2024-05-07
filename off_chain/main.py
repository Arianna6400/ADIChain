"""
This module acts as the entry point for the application. 
It initializes a new session and command line interface,
and displays the menu to the user.
"""

from cli.cli import CommandLineInterface
from session.session import Session

if __name__ == "__main__":
    new_session = Session()
    cli = CommandLineInterface(new_session)
    while True:
        cli.print_menu()
