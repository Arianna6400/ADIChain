from controllers.deploy_controller import DeployController
from web3 import Web3
import os
import time


class ActionController:
    def __init__(self, http_provider='http://ganache:8545'):
        #http://ganache:8545
        #http://127.0.0.1:8545
        # Initialize with a HTTP provider URL for the Ethereum node (Ganache for local testing).
        self.http_provider = http_provider
        # Connect to the Ethereum node using the Web3 library.
        self.w3 = Web3(Web3.HTTPProvider(self.http_provider))
        # Check if the connection is successful, otherwise raise an exception.
        assert self.w3.is_connected(), "Failed to connect to Ethereum node."
        # Initialize the contract attribute to None; it will be set after deployment.
        self.contract = None

    def deploy_and_initialize(self, contract_source_path='HealthCareRecords.sol'):
        # Create a DeployController instance for contract deployment.
        controller = DeployController(self.http_provider)
        # Resolve the path to the smart contract source code.
        contract_source_path = os.path.join(os.path.dirname(__file__), contract_source_path)
        # Compile the contract and deploy it to the blockchain.
        controller.compile_and_deploy(contract_source_path)
        # Assign the deployed contract to the instance attribute for further interaction.
        self.contract = controller.contract

    def read_data(self, function_name, *args):
        # Access a read-only function from the smart contract and return its result.
        function = self.contract.functions[function_name](*args)
        return function.call()

    def write_data(self, function_name, from_address, *args, gas=2000000, gas_price=None, nonce=None):
        # Set up transaction parameters for writing data to the blockchain.
        tx_parameters = {
            'from': from_address,
            'gas': gas,
            'gasPrice': gas_price or self.w3.eth.gas_price,
            'nonce': nonce or self.w3.eth.getTransactionCount(from_address)
        }
        # Execute the function on the blockchain and wait for the transaction receipt.
        function = self.contract.functions[function_name](*args)
        tx_hash = function.transact(tx_parameters)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def listen_to_event(self, event_name, callback):
        # Create a filter for listening to events emitted by the smart contract.
        event_filter = self.contract.events[event_name].createFilter(fromBlock='latest')
        # Continuously poll for new events and execute the callback function when events are found.
        while True:
            for event in event_filter.get_new_entries():
                callback(event)
            time.sleep(10)

    # The following methods interact with specific functions of the HealthCareRecords smart contract.
    # We use a dictionary to map different types of entities based on the solidity contract ones
    def register_entity(self, entity_type, *args, from_address):
        entity_functions = {
            'medic': self.contract.functions.registerMedic,
            'patient': self.contract.functions.registerPatient,
            'caregiver': self.contract.functions.registerCaregiver
        }
        return self.write_data(entity_functions[entity_type].__name__, from_address, *args)

    def update_entity_status(self, entity_type, entity_id, new_status, from_address):
        update_functions = {
            'medic': self.contract.functions.updateMedic,
            'patient': self.contract.functions.updatePatient,
            'caregiver': self.contract.functions.updateCaregiver
        }
        return self.write_data(update_functions[entity_type].__name__, from_address, entity_id, new_status)

    #Similar approach for reports and treatment plan, mapping different actions based on the solidity contract
    def manage_report(self, action, *args, from_address):
        report_functions = {
            'add': self.contract.functions.addReport,
            'update': self.contract.functions.updateReport
        }
        return self.write_data(report_functions[action].__name__, from_address, *args)

    def manage_treatment_plan(self, action, *args, from_address):
        treatment_plan_functions = {
            'add': self.contract.functions.addTreatmentPlan,
            'update': self.contract.functions.updateTreatmentPlan
        }
        return self.write_data(treatment_plan_functions[action].__name__, from_address, *args)
