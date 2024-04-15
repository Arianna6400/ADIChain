from web3 import Web3
from solcx import compile_standard, get_installed_solc_versions, install_solc

class OnChainController:
    def __init__(self, http_provider='http://127.0.0.1:8545', solc_version='0.8.0'):
        self.http_provider = http_provider
        self.solc_version = solc_version
        self.w3 = Web3(Web3.HTTPProvider(self.http_provider))
        assert self.w3.is_connected(), "Failed to connect to Ethereum node."
        self.contract = None

    def compile_and_deploy(self, contract_source_path):
        with open(contract_source_path, 'r') as file:
            source_code = file.read()
        self.compile_contract(source_code)
        self.deploy_contract()

    def compile_contract(self, solidity_source):
        if self.solc_version not in get_installed_solc_versions():
            install_solc(self.solc_version)
        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {"on_chain/on_chain.sol": {"content": solidity_source}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
        }, solc_version=self.solc_version)
        self.contract_id, self.contract_interface = next(iter(compiled_sol['contracts']['on_chain/on_chain.sol'].items()))
        self.abi = self.contract_interface['abi']
        self.bytecode = self.contract_interface['evm']['bytecode']['object']

    def deploy_contract(self):
        account = self.w3.eth.accounts[0]  # Utilizza il primo account disponibile
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.constructor().transact({'from': account})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)
        print(f'Contract deployed at {tx_receipt.contractAddress}')