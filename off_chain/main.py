from cli.cli import CommandLineInterface
from controllers.on_chain_controller import OnChainController
from session.session import Session

if __name__ == "__main__":
    new_session = Session()
    controller = OnChainController()  
    controller.compile_and_deploy('on_chain/on_chain.sol')
    cli = CommandLineInterface(new_session)
    while True:
        cli.print_menu()