from cli.cli import CommandLineInterface
from controllers.on_chain_controller import OnChainController

if __name__ == "__main__":
    controller = OnChainController()  
    controller.compile_and_deploy('on_chain/on_chain.sol')
    cli = CommandLineInterface()
    while True:
        cli.print_menu()