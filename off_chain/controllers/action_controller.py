from controllers.deploy_controller import DeployController
from session.logging import log_msg, log_error
from web3 import Web3
import os
import time
import json

class ActionController:
    def __init__(self, http_provider='http://127.0.0.1:8545'):
        #http://ganache:8545
        #http://127.0.0.1:8545
        self.http_provider = http_provider
        self.w3 = Web3(Web3.HTTPProvider(self.http_provider))
        assert self.w3.is_connected(), "Failed to connect to Ethereum node."
        self.load_contract()

    def load_contract(self):
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
            print("Contract files not found. Deploy contract first.")
            self.contract = None

    def deploy_and_initialize(self, contract_source_path='HealthCareRecords.sol'):
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
            print("An error occurred during deployment.")
        
    def read_data(self, function_name, *args):
        try:
            result = self.contract.functions[function_name](*args).call()
            log_msg(f"Data read from {function_name}: {result}")
            return result
        except Exception as e:
            log_error(f"Failed to read data from {function_name}: {str(e)}")
            raise e

    def write_data(self, function_name, from_address, *args, gas=2000000, gas_price=None, nonce=None):
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
        event_filter = self.contract.events.ActionLogged.create_filter(fromBlock='latest')
        while True:
            entries = event_filter.get_new_entries()
            for event in entries:
                self.handle_action_logged(event)
            time.sleep(10)

    def handle_action_logged(self, event):
        log_msg(f"New Action Logged: {event['args']}")

    def register_entity(self, entity_type, *args, from_address):
        if not from_address:
            raise ValueError("A valid Ethereum address must be provided as 'from_address'.")
        entity_functions = {
            'medic': 'addMedic',
            'patient': 'addPatient',
            'caregiver': 'addCaregiver'
        }
        function_name = entity_functions.get(entity_type)
        if not function_name:
            raise ValueError(f"No function available for entity type {entity_type}")
        return self.write_data(function_name, from_address, *args)

    def update_entity(self, entity_type, *args, from_address):
        if not from_address:
            raise ValueError("A valid Ethereum address must be provided as 'from_address'.")
        update_functions = {
            'medic': 'updateMedic',
            'patient': 'updatePatient',
            'caregiver': 'updateCaregiver'
        }
        function_name = update_functions.get(entity_type)
        if not function_name:
            raise ValueError(f"No function available for entity type {entity_type}")
        return self.write_data(function_name, from_address, *args)

    def manage_report(self, action, *args, from_address):
        if not from_address:
            raise ValueError("A valid Ethereum address must be provided as 'from_address'.")
        report_functions = {
            'add': 'addReport',
            'update': 'updateReport'
        }
        function_name = report_functions.get(action)
        if not function_name:
            raise ValueError(f"No function available for action {action}")
        return self.write_data(function_name, from_address, *args)

    def manage_treatment_plan(self, action, *args, from_address):
        if not from_address:
            raise ValueError("A valid Ethereum address must be provided as 'from_address'.")
        treatment_plan_functions = {
            'add': 'addTreatmentPlan',
            'update': 'updateTreatmentPlan'
        }
        function_name = treatment_plan_functions.get(action)
        if not function_name:
            raise ValueError(f"No function available for action {action}")
        return self.write_data(function_name, from_address, *args)
