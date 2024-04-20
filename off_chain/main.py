from cli.cli import CommandLineInterface
from controllers.action_controller import ActionController
from session.session import Session

if __name__ == "__main__":
    new_session = Session()
    controller = ActionController()  
    controller.deploy_and_initialize('../../on_chain/HealthCareRecords.sol')
    cli = CommandLineInterface(new_session)
    while True:
        cli.print_menu()