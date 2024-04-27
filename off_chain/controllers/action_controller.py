from controllers.deploy_controller import DeployController
from web3 import Web3
import os
import time
import json

class ActionController:
    def __init__(self, http_provider='http://127.0.0.1:8545'):
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
            else:
                print("Contract address or ABI not found. Please deploy the contract.")
        except FileNotFoundError:
            print("Contract files not found. Deploy contract first.")
            self.contract = None

    def deploy_and_initialize(self, contract_source_path='HealthCareRecords.sol'):
        controller = DeployController(self.http_provider)
        contract_source_path = os.path.join(os.path.dirname(__file__), contract_source_path)
        controller.compile_and_deploy(contract_source_path)
        self.contract = controller.contract
        with open('on_chain/contract_address.txt', 'w') as file:
            file.write(self.contract.address)
        with open('on_chain/contract_abi.json', 'w') as file:
            json.dump(self.contract.abi, file)

    def read_data(self, function_name, *args):
        function = self.contract.functions[function_name](*args)
        return function.call()

    def write_data(self, function_name, from_address, *args, gas=2000000, gas_price=None, nonce=None):
        if not from_address:
            raise ValueError("Invalid 'from_address' provided. It must be a non-empty string representing an Ethereum address.")
        tx_parameters = {
            'from': from_address,
            'gas': gas,
            'gasPrice': gas_price or self.w3.eth.gas_price,
            'nonce': nonce or self.w3.eth.get_transaction_count(from_address)
        }
        function = getattr(self.contract.functions, function_name)(*args)
        tx_hash = function.transact(tx_parameters)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def listen_to_event(self, event_name, callback):
        event_filter = self.contract.events[event_name].createFilter(fromBlock='latest')
        while True:
            for event in event_filter.get_new_entries():
                callback(event)
            time.sleep(10)

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

    def update_entity_status(self, entity_type, entity_id, new_status, from_address):
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
        return self.write_data(function_name, from_address, entity_id, new_status)

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
