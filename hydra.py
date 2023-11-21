import iop_python as iop
import asyncio
import requests
import json
import sys


class HydraWallet:

    def __init__(self,phrase):
        self.phrase = phrase
   
    
    def get_wallet_address(self,password):
        addr = iop.get_wallet(self.phrase,password)
        return addr
    
    async def send_tx(phrase,receiver,amount, nonce):
        response = await iop.send_transaction_with_python(phrase,receiver,amount,nonce)
        return response
    
    #this function assumes that the wallet has made a transaction before
    async def send_transaction(self,receiver,amount):
        addr = self.get_wallet_address()
        url = f"https://test.explorer.hydraledger.io:4705/api/v2/wallets/{addr}"
        # Send a GET request to the URL
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            nonce = int(data['data']['nonce'])
            #balance = data['data']['balance']
            response = asyncio.run(self.send_tx(self.phrase,receiver,amount,nonce))
            res = json.loads(response)
            if len(res['data']['accept']) > 0:
                txhash = res['data']['accept'][0]
                return txhash
            else:
                print("Your transaction was not successfull")
                sys.exit()
        else:
            print("Failed to fetch data. Status code:", response.status_code)       


    def check_transaction(txhash):
        url = "https://test.explorer.hydraledger.io:4705/api/v2/transactions/{txhash}"
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






















