from cli.cli import CommandLineInterface
from session.session import Session

if __name__ == "__main__":
    new_session = Session()
    cli = CommandLineInterface(new_session)
    while True:
        cli.print_menu()