import time
from web3 import Web3
from controllers.deploy_controller import DeployController  # Import the OnChainController class

class TransactionController:
    def __init__(self, http_provider='http://ganache:8545'):
        #http://ganache:8545
        #http://127.0.0.1:8545
        self.http_provider = http_provider
        self.w3 = Web3(Web3.HTTPProvider(self.http_provider))
        assert self.w3.is_connected(), "Failed to connect to Ethereum node."
        self.contract = None

    #def deploy_and_initialize(self, contract_source_path='../on_chain/on_chain.sol'):
    def deploy_and_initialize(self, contract_source_path='./on_chain/on_chain.sol'):
        controller = DeployController(self.http_provider)
        controller.compile_and_deploy(contract_source_path)
        self.contract = controller.contract  # Retrieve the deployed contract to use in functions

    def read_data(self, function_name, *args):
        # Calls a read-only function on the contract. These functions do not modify blockchain state and require no gas.
        function = self.contract.functions[function_name](*args)
        return function.call()

    def write_data(self, function_name, from_address, *args, gas=2000000, gas_price=None, nonce=None):
        # Prepares the transaction parameters including from address, gas limit, gas price, and nonce.
        tx_parameters = {
            'from': from_address,
            'gas': gas,
            'gasPrice': gas_price or self.w3.eth.gas_price,
            'nonce': nonce or self.w3.eth.getTransactionCount(from_address)
        }
        # Calls a function that modifies the blockchain state, therefore a transaction is sent.
        function = self.contract.functions[function_name](*args)
        tx_hash = function.transact(tx_parameters)
        # Waits for the transaction to be mined and returns the receipt.
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def listen_to_event(self, event_name, callback):
        # Sets up a filter to listen for a specified event emitted by the contract.
        event_filter = self.contract.events[event_name].createFilter(fromBlock='latest')
        # Continuously polls for the event and calls the provided callback function when the event is detected.
        while True:
            for event in event_filter.get_new_entries():
                callback(event)
            time.sleep(10)  # Pause the loop to prevent spamming the network with requests.
