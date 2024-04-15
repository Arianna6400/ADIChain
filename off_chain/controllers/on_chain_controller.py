import solcx
from web3 import Web3
from solcx import compile_standard, get_installed_solc_versions, install_solc

class OnChainController:
    #Setting up the web3 provider
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        assert self.w3.is_connected(), "Failed to connect to Ethereum node."
        self.contract = None

    #Function used to compile the contract
    def compile_contract(self, solidity_source, solc_version='0.8.0'):
        if solc_version not in get_installed_solc_versions():
            install_solc(solc_version)
        try:
            compiled_sol = compile_standard({
                "language": "Solidity",
                "sources": {"on_chain.sol": {"content": solidity_source}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    }
                }
            }, solc_version=solc_version)
            self.contract_id, self.contract_interface = next(iter(compiled_sol['contracts']['on_chain.sol'].items()))
            self.abi = self.contract_interface['abi']
            self.bytecode = self.contract_interface['evm']['bytecode']['object']
        except Exception as e:
            print(f"An error occurred during compilation: {e}")

    #Function used to deploy the contract and estimate gas for the deployment
    def deploy_contract(self, account):
        contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)

        estimated_gas = contract.constructor().estimateGas({'from': account})
        gas_price = self.w3.eth.gas_price

        # Deploy the contract with estimated gas and a specified gas price
        try:
            tx_hash = contract.constructor().transact({
                'from': account,
                'gas': estimated_gas,
                'gasPrice': gas_price
            })
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            self.contract = self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)
            return tx_receipt.contractAddress
        except Exception as e:
            print(f"An error occurred during deployment: {e}")
            return None
