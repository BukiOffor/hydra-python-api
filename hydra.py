import iop_python as iop
import asyncio
import requests
import json
import sys


class HydraWallet:

    def __init__(self,phrase,password):
        self.phrase = phrase
        self.password = password
   
    
    def get_wallet_address(self):
        addr = iop.get_wallet(self.phrase,self.password)
        return addr
    
    async def send_tx(phrase, receiver, amount, nonce, password):
        response = await iop.send_transaction_with_python(phrase,receiver,amount,nonce,password)
        return response
    
    def get_nonce(self):
        addr = self.get_wallet_address()
        url = f"https://test.explorer.hydraledger.io:4705/api/v2/wallets/{addr}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            nonce = int(data['data']['nonce'])
            return nonce
        else:
            print("Failed to fetch data. Status code:", response.status_code)   

    def sign_transaction(self,receiver,amount):
        nonce = self.get_nonce()
        response = iop.generate_transaction(self.phrase,receiver,amount,nonce,self.password)
        signed_txs = json.loads(response)
        return signed_txs    

    #this function assumes that the wallet has made a transaction before
    def send_transaction(self,receiver,amount):
        # Send a GET request to the URL
        signed_txs = self.sign_transaction(receiver,amount)
        url = "https://test.explorer.hydraledger.io:4705/api/v2/transactions"
        res = requests.post(url, json=signed_txs)
        response = res.json()
        return response


    def check_transaction(self,txhash):
        url = f"https://test.explorer.hydraledger.io:4705/api/v2/transactions/{txhash}"
        res = requests.get(url)
        response = res.json()
        txid = response['data']['id']
        blockId = response['data']['blockId']
        fee = response['data']['fee']
        confirmations = response['data']['confirmations']
        time = response['data']['timestamp']['human']          
        return f"Transaction with id {txid} was sent successfully at {time} with a fee of {fee} Hyd and has {confirmations} confirmations"

        
    def display_address_balance(self):
        addr = self.get_wallet_address()
        response = requests.get(f"https://test.explorer.hydraledger.io:4705/api/v2/wallets/{addr}")
        if response.status_code == 200:
            data = response.json()
            balance = data['data']['balance']
            return balance
        else:
            print("Failed to fetch data. Status code:", response.status_code)  

        

class HydraChain:

    def __init__(self) -> None:
        pass

    def generate_phrase():
        phrase = iop.generate_phrase()
        return phrase
    
    def generate_wallet(self, unlock_password):
        pass






















