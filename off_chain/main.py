from cli.cli import CommandLineInterface
from controllers.transact_controller import TransactionController
from session.session import Session

if __name__ == "__main__":
    new_session = Session()
    controller = TransactionController()  
    controller.deploy_and_initialize('../../on_chain/HealthCareRecords.sol')
    cli = CommandLineInterface(new_session)
    while True:
        cli.print_menu()