from web3 import Web3
import solcx
from solcx import compile_source

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.eth.default_account = w3.eth.accounts[0]

# Compile contract
with open('contracts/Identity.sol', 'r') as file:
    contract_source = file.read()

compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'])
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# Deploy contract
Identity = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Identity.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

# Instantiate contract
identity_contract = w3.eth.contract(address=contract_address, abi=abi)

def register_identity(user_address, hash_data):
    tx_hash = identity_contract.functions.registerIdentity(hash_data).transact({'from': user_address})
    w3.eth.wait_for_transaction_receipt(tx_hash)

def verify_identity(user_address, hash_data):
    return identity_contract.functions.verifyIdentity(user_address, hash_data).call()