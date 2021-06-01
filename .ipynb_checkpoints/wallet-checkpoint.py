# Import dependencies
import subprocess
import json
import os
from dotenv import load_dotenv
from web3 import Web3
from bit import wif_to_key
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load and set environment variables
load_dotenv("api.env")
mnemonic=os.getenv("mnemonic")
private_key = os.getenv("PRIVATE_KEY")
private_key_BTC = os.getenv("BTC_PRIVATE")
key = wif_to_key(private_key_BTC)

#checking connection to w3
## Check balances of mining node (put mining node address)
w3.eth.getBalance(private_key)

## Convert to Ether
w3.fromWei(w3.eth.getBalance(private_key), 'ether')

#get transactions using bit
key.get_transactions()

# Import constants.py and necessary functions from bit and web3
from constants import *
 
# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {'BTC', 'ETH'}
    
# Create a function called `derive_wallets`
def derive_wallets(coins):
    command = './derive -g --mnemonic=mnemonic --cols=path,address,privkey,pubkey --format=json --coin --numderive' #command is for mac's
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, private_key):
    if coin == ETH:
        return Account.privateKeyToAccount(private_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(private_key)
    
# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin ==ETH:
        value = w3.toWei(amount, "ether")
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "from": account, "value": amount})
        return {
            "chainId": w3.eth.chain_id
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.generateGasPrice(),
            "gas": gasEstimate,
            "nonce":w3.eth.getTransactionCount(account.address),
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
    
# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    if coin == ETH:
        tx = create_tx(coin, account.address, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    if coin == BTCTEST:
        tx = create_tx(coin, account, recipient, amount)
        signed = account.sign_transaction(tx)
        return NetworkAPI.broadcast_tx_testnet(signed)
coins = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST),
}
        print(coins)

#getting transaction
w3.eth.getTransaction('0xbc0539a01ab1da702a87182228bbf9f8596dbdc41ad5977c4edb04c33c9d9354')
    
    
