# Import necessary libraries from Web3.py and the Solidity compiler (solc)
from web3 import Web3
from solcx import compile_standard, get_installed_solc_versions, install_solc

# Define a class to control on-chain operations
class DeployController:
    # Initialize the controller with a default Ethereum node address and Solidity compiler version
    def __init__(self, http_provider='http://127.0.0.1:8545', solc_version='0.8.0'):
        self.http_provider = http_provider
        self.solc_version = solc_version
        self.w3 = Web3(Web3.HTTPProvider(self.http_provider))  # Set up a Web3 connection
        assert self.w3.is_connected(), "Failed to connect to Ethereum node."  # Ensure the connection is successful
        self.contract = None  # Initialize a variable to store the contract object

    # Compile and deploy a smart contract using its source file path
    def compile_and_deploy(self, contract_source_path):
        with open(contract_source_path, 'r') as file:
            source_code = file.read()  # Read the contract source code
        self.compile_contract(source_code)  # Compile the smart contract
        self.deploy_contract()  # Deploy the compiled contract

    # Compile a smart contract from its source code
    def compile_contract(self, solidity_source):
        if self.solc_version not in get_installed_solc_versions():
            install_solc(self.solc_version)  # Install the specified version of solc if not already installed
        # Compile the smart contract using specified settings
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {"on_chain/on_chain.sol": {"content": solidity_source}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
        }, solc_version=self.solc_version)
        # Extract the contract ID and interface from the compiled output
        self.contract_id, self.contract_interface = next(iter(compiled_sol['contracts']['on_chain/on_chain.sol'].items()))
        self.abi = self.contract_interface['abi']  # Extract the ABI
        self.bytecode = self.contract_interface['evm']['bytecode']['object']  # Extract the bytecode

    # Deploy the compiled contract to the blockchain
    def deploy_contract(self):
        account = self.w3.eth.accounts[0]  # Use the first account available
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)  # Create a contract object
        tx_hash = contract.constructor().transact({'from': account})  # Send the contract creation transaction
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)  # Wait for the transaction to be mined
        self.contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)  # Update the contract object with the deployed address
        print(f'Contract deployed at {tx_receipt.contractAddress}')  # Print the deployment address
