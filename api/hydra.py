#import iop_python as iop
import requests
import json
import os

#https://test.explorer.hydraledger.tech/wallets/tdXxhgZV8aAGLL9CCJ4ry9AzTQZzRKqJ97

# ---------------------------------------MileStone 2-----------------------------------------------------
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# |                                                                                                     |
# -------------------------------------------------------------------------------------------------------
api = "https://iop-server.onrender.com"


class HydraChain:

    home_directory = os.path.expanduser("~")
    file_path = home_directory+"/.hydra_wallet"
    def __init__(self) -> None:
        pass

    def verify_signed_statement(self,signed_statement):
        #result = iop.verify_signed_statement(signed_statement)
        result = requests.post(api+"/api/verify_signed_statement", json={"data":signed_statement}).json()
        return result
        
    def verify_statement_with_did(self, signed_statement):
        did = json.loads(signed_statement)['content']['claim']['subject']
        url = f"https://test.explorer.hydraledger.tech:4705/morpheus/v1/did/{did}/document"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            did_doc = json.dumps(data)
            result = requests.post(api+"/api/validate_statement_with_did", json={"data":signed_statement,"doc":did_doc}).json()
            return result
        

    def generate_nonce(self):
        nonce = requests.get(api+"/api/generate_nonce").json()
        return nonce
    
    def get_account_transactions(self,address):
        url = f"https://test.explorer.hydraledger.tech:4705/api/v2/wallets/{address}/transactions"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            return data['data']
        else:
            #print("Failed to fetch data. Status code:", response.status_code)
            return [] 



class HydraWallet:

    # home_directory = os.path.expanduser("~")
    # file_path = home_directory+"/.hydra_wallet"

    def __init__(self, path):
        self.file_path = path

    def generate_nonce(self):
        nonce = requests.get(api+"/api/generate_nonce").json()
        return nonce

    def generate_phrase(self):
       phrase = requests.get(api+"/api/generate_phrase").json()
       return phrase
    
    def load_wallets(self):
        try:
            with open(self.file_path, 'r') as json_file:
                wallets = json.load(json_file)
                return wallets
        except FileNotFoundError:
            print("user does not own any wallets")
            return []
        
    def generate_wallet(self, password,phrase):
        hyd_vault = requests.post(api+"/api/get_hyd_vault", json={"password":password,"phrase":phrase}).json()
        morpheus_vault = requests.post(api+"/api/get_morpheus_vault", json={"password":password,"phrase":phrase}).json()
        h_vault = json.loads(hyd_vault)
        m_vault = json.loads(morpheus_vault)
        vaults = []
        vaults.append(h_vault) 
        vaults.append(m_vault)
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                data.append(vaults)
            with open(self.file_path, 'w') as json_file:
                json.dump(data, json_file,indent=2)
            return phrase
        except FileNotFoundError:
            myvault = []
            myvault.append(vaults)
            #f1 = os.open (self.file_path, os.O_CREAT, 0o700)
            #os.close (f1)
            with open(self.file_path, 'a') as json_file:                
                json.dump(myvault, json_file, indent=2)
            return phrase
    
    def get_new_acc_on_vault(self,password, account=0):
        data = self.load_wallets()
        if len(data) > 0:
            vault = data[account][0]
            new_account = vault['plugins'][-1]['parameters']['account']
            vault_data = json.dumps(vault)
            new_wallet = requests.post(api+"/api/get_new_acc_on_vault", json={"vault":vault_data,"password":password,"account": new_account+1}).json()
            data[account][0] = json.loads(new_wallet)
            with open(self.file_path, 'w') as json_file:                
                json.dump(data, json_file, indent=2)
            return new_wallet



    def get_wallet_address(self,account=0,key=0):
        data = self.load_wallets()
        if len(data) > 0:
            vault = data[account][0]
            _params = vault['plugins'][0]['parameters']
            data = json.dumps(vault)
            params = json.dumps(_params)
            #print(data)
            addr = requests.post(api+"/api/get_wallet", json={"data":data,"account":str(key)}).json()
            return addr
    

    def generate_did(self,password,account=0):
        file_content = self.load_wallets()
        if len(file_content) > 0:
            vault = file_content[account][1]
            vault = json.dumps(vault)
            #did = iop.generate_did_by_morpheus(vault, password)
            did = requests.post(api+"/api/generate_did_by_morpheus", json={"vault": vault, "password": password}).json()
            return(did)


    def recover_wallet(self,password,phrase):
        vault = self.generate_wallet(password,phrase)
        return vault

    def sign_witness_statement(self,password, data,account=0):
        file_content = self.load_wallets()
        if len(file_content) > 0:
            vault = file_content[account][1]
            vault = json.dumps(vault)
            #signed_statement = iop.sign_witness_statement(vault,password,data)
            signed_statement = requests.post(api+"/api/sign_witness_statement", json={"vault":vault, "password":password, "data":data}).json()
            return signed_statement      
    
    def sign_did_statement(self,statement,password,account=0):
        wallet = self.load_wallets()
        vault = wallet[account][1]
        vault = json.dumps(vault)
        data = bytes(statement, "utf-8")
        #signed_statement = iop.sign_did_statement(vault,password,data)
        signed_statement = requests.post(api+"/api/sign_did_statement", json={"vault":vault,"password":password,"data":data}).json()
        details = {
            "content": statement,
            "publicKey": signed_statement["public_key"],
            "signature": signed_statement["signature"]
        }
        return json.dumps({"Signed contract":details}, indent=4)


    def get_nonce(self,key=0):
        addr = self.get_wallet_address(key=key)
        url = f"https://test.explorer.hydraledger.tech:4705/api/v2/wallets/{addr}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            nonce = int(data['data']['nonce'])
            return nonce
        else:
            print("Failed to fetch data. Status code:", response.status_code)   

            
    def sign_transaction(self,receiver,amount,password,account,key):
        nonce = self.get_nonce()
        vaults = self.load_wallets()
        vault = vaults[account][0]
        _params = vault['plugins'][0]['parameters']
        data = json.dumps(vault)
        params = json.dumps(_params)
        #response = iop.generate_transaction(data,receiver,amount,nonce,password,key)
        tx = {"data":data,"receiver":receiver,"amount":amount,"nonce":nonce, "password":password, "account":key}
        response = requests.post(api+"/api/generate_transcation", json=tx)
        signed_txs = json.loads(response)
        return signed_txs    

    #this function assumes that the wallet has made a transaction before
    def send_transaction(self,receiver,amount,password,account=0,key=0):
        # Send a GET request to the URL
        signed_txs = self.sign_transaction(receiver,amount,password,account,key)
        url = "https://test.explorer.hydraledger.tech:4705/api/v2/transactions"
        res = requests.post(url, json=signed_txs)
        response = res.json()
        #print(response)
        return response


    def check_transaction(self,txhash):
        url = f"https://test.explorer.hydraledger.tech:4705/api/v2/transactions/{txhash}"
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
        if addr == None:
            return None
        response = requests.get(f"https://test.explorer.hydraledger.tech:4705/api/v2/wallets/{addr}")
        if response.status_code == 200:
            data = response.json()
            balance = data['data']['balance']
            return balance
        else:
            #print("Failed to fetch data. Status code:", response.status_code) 
            return None 

    def get_account_transactions(self):
        addr = self.get_wallet_address()
        if addr == None:
            return None
        url = f"https://test.explorer.hydraledger.tech:4705/api/v2/wallets/{addr}/transactions"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            return data['data']
        else:
            #print("Failed to fetch data. Status code:", response.status_code)
            return [] 
        

    def delete_account(self,index):
        wallets = self.load_wallets()
        wallets.pop(int(index))
        with open(self.file_path, 'w') as json_file:
            json.dump(wallets, json_file, indent=2)

    
    @classmethod
    def generate_statement(self,statement,password):
        data = {
                "claim": {
                    "subject": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
                    "content": {
                        "userId": "5d5d9eda-d3a9-4347-b4ae-b176b75dcf51",
                        "fullName": {
                            "nonce": self.generate_nonce(),
                            "value": statement['name']
                        },
                        "birthDate": {
                            "nonce": self.generate_nonce(),
                            "value": statement["dob"]
                        },
                        "address": {
                            "nonce": self.generate_nonce(),
                            "value": {
                                "country": {
                                    "nonce": self.generate_nonce(),
                                    "value": statement["country"]
                                },
                                "city": {
                                    "nonce": self.generate_nonce(),
                                    "value": statement["city"]
                                },
                                "street": {
                                    "nonce": self.generate_nonce(),
                                    "value": statement["street"]
                                },
                                "zipcode": {
                                    "nonce": self.generate_nonce(),
                                    "value": statement["zipcode"]
                                }
                            }
                        },
                        
                    }
                },
                "processId": "cjuQR3pDJeaiRv9oCZ-fBE7T8QWpUGfjP40sAXq0bLwr-8",
                "constraints": {
                    "authority": self.generate_did(password),
                    "witness": "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw",
                    "content": None
                },
                "nonce": self.generate_nonce(),
                }
        return data
            
    @classmethod
    def generate_and_sign_statement(self,statement,password):
        data = self.generate_statement(statement,password)
        signed_statement = self.sign_witness_statement(password,json.dumps(data))
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                data.append(json.loads(signed_statement)) #here
            with open(self.file_path, 'w') as json_file:
                json.dump(data, json_file,indent=2)
            return signed_statement
        except FileNotFoundError:
            my_statements = []
            my_statements.append(json.loads(signed_statement)) #here
            f1 = os.open (self.file_path, os.O_CREAT, 0o700)
            os.close (f1)
            with open(self.file_path, 'a') as json_file:                
                json.dump(my_statements, json_file, indent=2)
            return signed_statement
            
        
        





















