from web3 import Web3
import os
import time
from controllers.deploy_controller import DeployController  # Import the DeployController class

class TransactionController:
    def __init__(self, http_provider='http://ganache:8545'):
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

    def pause(self, tx_args):
        # Pause operations on the smart contract.
        tx_hash = self.contract.functions.pause().transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def unpause(self, tx_args):
        # Resume operations on the smart contract.
        tx_hash = self.contract.functions.unpause().transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def register_medic(self, _id, _name, _lastname, _specialization, tx_args):
        # Register a medic on the smart contract.
        tx_hash = self.contract.functions.registerMedic(_id, _name, _lastname, _specialization).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def register_caregiver(self, _id, _name, _lastname, tx_args):
        # Register a caregiver on the smart contract.
        tx_hash = self.contract.functions.registerCaregiver(_id, _name, _lastname).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_patient(self, _id, _condition, tx_args):
        # Update patient information in the smart contract.
        tx_hash = self.contract.functions.updatePatient(_id, _condition).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def file_report(self, _reportId, _patientId, _medicId, _details, tx_args):
        # File a medical report for a patient by a medic.
        tx_hash = self.contract.functions.fileReport(_reportId, _patientId, _medicId, _details).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def create_treatment_plan(self, _planId, _patientId, _medicId, _treatmentDetails, _medication, _startDate, _endDate, tx_args):
        # Create a treatment plan for a patient.
        tx_hash = self.contract.functions.createTreatmentPlan(_planId, _patientId, _medicId, _treatmentDetails, _medication, _startDate, _endDate).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
