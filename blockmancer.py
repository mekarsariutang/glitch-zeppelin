import requests
import time
import hashlib
from web3 import Web3

INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # замени на свой ключ
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

def is_suspicious(tx):
    if tx['value'] > web3.toWei(100, 'ether'):
        return True
    if tx['gasPrice'] > web3.toWei(300, 'gwei'):
        return True
    return False

def analyze_block(block_number):
    block = web3.eth.getBlock(block_number, full_transactions=True)
    suspicious = []
    for tx in block.transactions:
        if is_suspicious(tx):
            suspicious.append({
                'hash': tx['hash'].hex(),
                'from': tx['from'],
                'to': tx['to'],
                'value_eth': web3.fromWei(tx['value'], 'ether'),
                'gas_price_gwei': web3.fromWei(tx['gasPrice'], 'gwei')
            })
    return suspicious

def monitor():
    print("[+] Monitoring Ethereum mempool for potential front-running / flashbots...\\n")
    latest = web3.eth.blockNumber
    while True:
        current = web3.eth.blockNumber
        if current > latest:
            print(f"[Block {current}] Checking for suspicious activity...")
            alerts = analyze_block(current)
            for alert in alerts:
                print("\\n🚨 Suspicious Transaction Detected:")
                for key, value in alert.items():
                    print(f"  {key}: {value}")
            latest = current
        time.sleep(5)

if __name__ == "__main__":
    monitor()
