import os
import time
import json
from colorama import Fore, Style, init
from controllers.deploy_controller import DeployController
from session.logging import log_msg, log_error
from web3 import Web3

class ActionController:
    """
    ActionController interacts with the Ethereum blockchain through methods defined in the contract.
    Connection with provider is established thanks to DeployController and Web3.
    """

    init(convert=True)

    def __init__(self, http_provider='http://127.0.0.1:8545'):
        """
        Initialize the ActionController to interact with an Ethereum blockchain.

        Args:
            http_provider (str): The HTTP URL to connect to an Ethereum node.
        """
        #http://ganache:8545
        #http://127.0.0.1:8545
        self.http_provider = http_provider
        self.w3 = Web3(Web3.HTTPProvider(self.http_provider))
        assert self.w3.is_connected(), Fore.RED + "Failed to connect to Ethereum node." + Style.RESET_ALL
        self.load_contract()

    def load_contract(self):
        """
        Load the contract using the ABI and address from specified files.
        Logs error if files are missing or contents are invalid.
        """
        try:
            with open('on_chain/contract_address.txt', 'r') as file:
                contract_address = file.read().strip()
            with open('on_chain/contract_abi.json', 'r') as file:
                contract_abi = json.load(file)
            if contract_address and contract_abi:
                self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
                log_msg(f"Contract loaded with address: {contract_address}")
            else:
                log_error("Contract address or ABI not found. Please deploy the contract.")
        except FileNotFoundError:
            log_error("Contract files not found. Deploy contract first.")
            print(Fore.RED + "Contract files not found. Deploy contract first." + Style.RESET_ALL)
            self.contract = None

    def deploy_and_initialize(self, contract_source_path='HealthCareRecords.sol'):
        """
        Deploys and initializes a smart contract.

        Args:
            contract_source_path (str): Relative path to the Solidity contract source file.
        """
        try:
            controller = DeployController(self.http_provider)
            contract_source_path = os.path.join(os.path.dirname(__file__), contract_source_path)
            controller.compile_and_deploy(contract_source_path)
            self.contract = controller.contract
            with open('on_chain/contract_address.txt', 'w') as file:
                file.write(self.contract.address)
            with open('on_chain/contract_abi.json', 'w') as file:
                json.dump(self.contract.abi, file)
            log_msg(f"Contract deployed at {self.contract.address} and initialized.")
        except Exception as e:
            log_error(str(e))
            print(Fore.RED + "An error occurred during deployment." + Style.RESET_ALL)
        
    def read_data(self, function_name, *args):
        """
        Reads data from a contract's function.

        Args:
            function_name (str): The name of the function to call.
            *args: Arguments required by the contract function.

        Returns:
            The result returned by the contract function.
        """
        try:
            result = self.contract.functions[function_name](*args).call()
            log_msg(f"Data read from {function_name}: {result}")
            return result
        except Exception as e:
            log_error(f"Failed to read data from {function_name}: {str(e)}")
            raise e

    def write_data(self, function_name, from_address, *args, gas=2000000, gas_price=None, nonce=None):
        """
        Writes data to a contract's function.

        Args:
            function_name (str): The function name to call on the contract.
            from_address (str): The Ethereum address to send the transaction from.
            *args: Arguments required by the function.
            gas (int): The gas limit for the transaction.
            gas_price (int): The gas price for the transaction.
            nonce (int): The nonce for the transaction.

        Returns:
            The transaction receipt object.
        """
        if not from_address:
            raise ValueError("Invalid 'from_address' provided. It must be a non-empty string representing an Ethereum address.")
        tx_parameters = {
            'from': from_address,
            'gas': gas,
            'gasPrice': gas_price or self.w3.eth.gas_price,
            'nonce': nonce or self.w3.eth.get_transaction_count(from_address)
        }
        try:
            function = getattr(self.contract.functions, function_name)(*args)
            tx_hash = function.transact(tx_parameters)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            log_msg(f"Transaction {function_name} executed. From: {from_address}, Tx Hash: {tx_hash.hex()}, Gas: {gas}, Gas Price: {tx_parameters['gasPrice']}")
            return receipt

        except Exception as e:
            log_error(f"Error executing {function_name} from {from_address}. Error: {str(e)}")
            raise e

    def listen_to_event(self):
        """
        Listens to a specific event from the smart contract indefinitely.
        """
        event_filter = self.contract.events.ActionLogged.create_filter(fromBlock='latest')
        while True:
            entries = event_filter.get_new_entries()
            for event in entries:
                self.handle_action_logged(event)
            time.sleep(10)

    def handle_action_logged(self, event):
        """
        Handles events by logging a message when an event is caught.

        Args:
            event (dict): The event data returned by the blockchain.
        """
        log_msg(f"New Action Logged: {event['args']}")

    def register_entity(self, entity_type, *args, from_address):
        """
        Registers a new entity of a specified type in the contract.

        Args:
            entity_type (str): Type of the entity to register, e.g., 'medic', 'patient', 'caregiver'.
            *args: Additional arguments required by the contract function.
            from_address (str): The Ethereum address to send the transaction from.

        Returns:
            The transaction receipt object.
        
        Raises:
            ValueError: If no function is available for the specified entity type or the from_address is invalid.
        """
        if not from_address:
            raise ValueError(Fore.RED + "A valid Ethereum address must be provided as 'from_address'." + Style.RESET_ALL)
        entity_functions = {
            'medic': 'addMedic',
            'patient': 'addPatient',
            'caregiver': 'addCaregiver'
        }
        function_name = entity_functions.get(entity_type)
        if not function_name:
            raise ValueError(Fore.RED + f"No function available for entity type {entity_type}" + Style.RESET_ALL)
        return self.write_data(function_name, from_address, *args)

    def update_entity(self, entity_type, *args, from_address):
        """
        Updates an existing entity of a specified type in the contract.

        Args:
            entity_type (str): Type of the entity to update, e.g., 'medic', 'patient', 'caregiver'.
            *args: Additional arguments required by the contract function.
            from_address (str): The Ethereum address to send the transaction from.

        Returns:
            The transaction receipt object.

        Raises:
            ValueError: If no function is available for the specified entity type or the from_address is invalid.
        """
        if not from_address:
            raise ValueError(Fore.RED + "A valid Ethereum address must be provided as 'from_address'." + Style.RESET_ALL)
        update_functions = {
            'medic': 'updateMedic',
            'patient': 'updatePatient',
            'caregiver': 'updateCaregiver'
        }
        function_name = update_functions.get(entity_type)
        if not function_name:
            raise ValueError(Fore.RED + f"No function available for entity type {entity_type}" + Style.RESET_ALL)
        return self.write_data(function_name, from_address, *args)

    def manage_report(self, action, *args, from_address):
        """
        Manages reports by adding new reports.

        Args:
            action (str): The action to be performed, currently only 'add' is supported.
            *args: Additional arguments required by the contract function.
            from_address (str): The Ethereum address to send the transaction from.

        Returns:
            The transaction receipt object.

        Raises:
            ValueError: If no function is available for the specified action or the from_address is invalid.
        """
        if not from_address:
            raise ValueError(Fore.RED + "A valid Ethereum address must be provided as 'from_address'." + Style.RESET_ALL)
        report_functions = {
            'add': 'addReport',
        }
        function_name = report_functions.get(action)
        if not function_name:
            raise ValueError(Fore.RED + f"No function available for action {action}" + Style.RESET_ALL)
        return self.write_data(function_name, from_address, *args)

    def manage_treatment_plan(self, action, *args, from_address):
        """
        Manages treatment plans by adding or updating them.

        Args:
            action (str): The action to be performed, such as 'add' or 'update'.
            *args: Additional arguments required by the contract function.
            from_address (str): The Ethereum address to send the transaction from.

        Returns:
            The transaction receipt object.

        Raises:
            ValueError: If no function is available for the specified action or the from_address is invalid.
        """
        if not from_address:
            raise ValueError(Fore.RED + "A valid Ethereum address must be provided as 'from_address'." + Style.RESET_ALL)
        treatment_plan_functions = {
            'add': 'addTreatmentPlan',
            'update': 'updateTreatmentPlan'
        }
        function_name = treatment_plan_functions.get(action)
        if not function_name:
            raise ValueError(Fore.RED + f"No function available for action {action}" + Style.RESET_ALL)
        return self.write_data(function_name, from_address, *args)
