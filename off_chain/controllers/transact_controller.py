from web3 import Web3
import os
import time
from controllers.deploy_controller import DeployController  # Import the OnChainController class

class TransactionController:
    def __init__(self, http_provider='http://ganache:8545'):
        #http://ganache:8545
        #http://127.0.0.1:8545
        self.http_provider = http_provider
        self.w3 = Web3(Web3.HTTPProvider(self.http_provider))
        assert self.w3.is_connected(), "Failed to connect to Ethereum node."
        self.contract = None

    def deploy_and_initialize(self, contract_source_path='HealthCareRecords.sol'):
        controller = DeployController(self.http_provider)
        contract_source_path = os.path.join(os.path.dirname(__file__), contract_source_path)
        controller.compile_and_deploy(contract_source_path)
        self.contract = controller.contract

    def read_data(self, function_name, *args):
        function = self.contract.functions[function_name](*args)
        return function.call()

    def write_data(self, function_name, from_address, *args, gas=2000000, gas_price=None, nonce=None):
        tx_parameters = {
            'from': from_address,
            'gas': gas,
            'gasPrice': gas_price or self.w3.eth.gas_price,
            'nonce': nonce or self.w3.eth.getTransactionCount(from_address)
        }
        function = self.contract.functions[function_name](*args)
        tx_hash = function.transact(tx_parameters)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def listen_to_event(self, event_name, callback):
        event_filter = self.contract.events[event_name].createFilter(fromBlock='latest')
        while True:
            for event in event_filter.get_new_entries():
                callback(event)
            time.sleep(10)

    # HealthCareRecords Contract Interaction Methods
    def pause(self, tx_args):
        tx_hash = self.contract.functions.pause().transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def unpause(self, tx_args):
        tx_hash = self.contract.functions.unpause().transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def register_medic(self, _id, _name, _lastname, _specialization, tx_args):
        tx_hash = self.contract.functions.registerMedic(_id, _name, _lastname, _specialization).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def register_caregiver(self, _id, _name, _lastname, tx_args):
        tx_hash = self.contract.functions.registerCaregiver(_id, _name, _lastname).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def update_patient(self, _id, _condition, tx_args):
        tx_hash = self.contract.functions.updatePatient(_id, _condition).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def file_report(self, _reportId, _patientId, _medicId, _details, tx_args):
        tx_hash = self.contract.functions.fileReport(_reportId, _patientId, _medicId, _details).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def create_treatment_plan(self, _planId, _patientId, _medicId, _treatmentDetails, _medication, _startDate, _endDate, tx_args):
        tx_hash = self.contract.functions.createTreatmentPlan(_planId, _patientId, _medicId, _treatmentDetails, _medication, _startDate, _endDate).transact(tx_args)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

