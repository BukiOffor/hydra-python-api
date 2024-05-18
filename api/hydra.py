import iop_python as iop
import requests
import json
import os

#https://dev.explorer.hydraledger.tech/wallets/tdXxhgZV8aAGLL9CCJ4ry9AzTQZzRKqJ97

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


class HydraChain:

    home_directory = os.path.expanduser("~")
    file_path = home_directory+"/.hydra_wallet"
    
    def __init__(self) -> None:
        pass

    def verify_signed_statement(self,signed_statement):
        result = iop.verify_signed_statement(signed_statement)
        return result
        
    def verify_statement_with_did(self, signed_statement):
        did = json.loads(signed_statement)['content']['claim']['subject']
        url = f"https://dev.explorer.hydraledger.tech:4705/morpheus/v1/did/{did}/document"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            did_doc = json.dumps(data)
            result = iop.validate_statement_with_did(signed_statement,did_doc)
            return result
        

    def generate_nonce(self):
        nonce = iop.generate_nonce()
        return nonce
    
    def get_account_transactions(self,address):
        url = f"https://dev.explorer.hydraledger.tech:4705/api/v2/wallets/{address}/transactions"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            return data['data']
        else:
            #print("Failed to fetch data. Status code:", response.status_code)
            return [] 



class HydraWallet:

    home_directory = os.path.expanduser("~")
    file_path = home_directory+"/.hydra_wallet"

    def __init__(self) -> None:
        pass

    def generate_phrase(self):
        phrase = iop.generate_phrase()
        return phrase
    
    @classmethod
    def load_wallets(cls):
        try:
            with open(cls.file_path, 'r') as json_file:
                wallets = json.load(json_file)
                return wallets
        except FileNotFoundError:
            print("user does not own any wallets")
            return []
        
    @classmethod
    def generate_wallet(cls, password,phrase,network="devnet"):
        hyd_vault = iop.get_hyd_vault(phrase, password,network)
        morpheus_vault = iop.get_morpheus_vault(phrase, password)
        h_vault = json.loads(hyd_vault)
        m_vault = json.loads(morpheus_vault)
        vaults = []
        vaults.append(h_vault) 
        vaults.append(m_vault)
        home_directory = os.path.expanduser("~")
        try:
            with open(cls.file_path, 'r') as file:
                data = json.load(file)
                data.append(vaults)
            with open(cls.file_path, 'w') as json_file:
                json.dump(data, json_file,indent=2)
            return phrase
        except FileNotFoundError:
            myvault = []
            myvault.append(vaults)
            f1 = os.open (cls.file_path, os.O_CREAT, 0o700)
            os.close (f1)
            with open(home_directory+'/.hydra_wallet', 'a') as json_file:                
                json.dump(myvault, json_file, indent=2)
            return phrase
    
    @classmethod
    def get_new_acc_on_vault(cls,password, account=0, network="devnet"):
        data = cls.load_wallets()
        if len(data) > 0:
            vault = data[account][0]
            new_account = vault['plugins'][-1]['parameters']['account']
            vault_data = json.dumps(vault)
            new_wallet = iop.get_new_acc_on_vault(vault_data,password,new_account+1,network)
            data[account][0] = json.loads(new_wallet)
            with open(cls.file_path, 'w') as json_file:                
                json.dump(data, json_file, indent=2)
            return new_wallet



    @classmethod
    def get_wallet_address(cls,account=0,key=0,network="devnet"):
        data = cls.load_wallets()
        if len(data) > 0:
            vault = data[account][0]
            _params = vault['plugins'][0]['parameters']
            data = json.dumps(vault)
            params = json.dumps(_params)
            addr = iop.get_wallet(data,key,network)
            return addr
    

    @classmethod
    def generate_did(cls,password,account=0):
        file_content = cls.load_wallets()
        if len(file_content) > 0:
            vault = file_content[account][1]
            vault = json.dumps(vault)
            did = iop.generate_did_by_morpheus(vault, password)
            return(did)


    def recover_wallet(cls,password,phrase,network='devnet'):
        vault = cls.generate_wallet(password,phrase,network)
        return vault

    @classmethod
    def sign_witness_statement(cls,password, data,account=0):
        file_content = cls.load_wallets()
        if len(file_content) > 0:
            vault = file_content[account][1]
            vault = json.dumps(vault)
            signed_statement = iop.sign_witness_statement(vault,password,data)
            return signed_statement      
    
    @classmethod
    def sign_did_statement(cls,statement,password,account=0):
        wallet = cls.load_wallets()
        vault = wallet[account][1]
        vault = json.dumps(vault)
        data = bytes(statement, "utf-8")
        signed_statement = iop.sign_did_statement(vault,password,data)
        details = {
            "content": statement,
            "publicKey": signed_statement[1],
            "signature": signed_statement[0]
        }
        return json.dumps({"Signed contract":details}, indent=4)


    def get_nonce(cls,key=0):
        addr = cls.get_wallet_address(key=key)
        url = f"https://dev.explorer.hydraledger.tech:4705/api/v2/wallets/{addr}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            nonce = int(data['data']['nonce'])
            return nonce
        else:
            print("Failed to fetch data. Status code:", response.status_code)   

            
    def sign_transaction(cls,receiver,amount,password,account,key,network):
        nonce = cls.get_nonce()
        vaults = cls.load_wallets()
        vault = vaults[account][0]
        _params = vault['plugins'][0]['parameters']
        data = json.dumps(vault)
        params = json.dumps(_params)
        response = iop.generate_transaction(data,receiver,amount,nonce,password,key,network)
        signed_txs = json.loads(response)
        return signed_txs    

    #this function assumes that the wallet has made a transaction before
    def send_transaction(self,receiver,amount,password,account=0,key=0,network="devnet"):
        # Send a GET request to the URL
        signed_txs = self.sign_transaction(receiver,amount,password,account,key,network)
        url = "https://dev.explorer.hydraledger.tech:4705/api/v2/transactions"
        res = requests.post(url, json=signed_txs)
        response = res.json()
        print(response)
        return response


    def check_transaction(self,txhash):
        url = f"https://dev.explorer.hydraledger.tech:4705/api/v2/transactions/{txhash}"
        res = requests.get(url)
        response = res.json()
        txid = response['data']['id']
        blockId = response['data']['blockId']
        fee = response['data']['fee']
        confirmations = response['data']['confirmations']
        time = response['data']['timestamp']['human']          
        return f"Transaction with id {txid} was sent successfully at {time} with a fee of {fee} Hyd and has {confirmations} confirmations"

    @classmethod   
    def display_address_balance(cls):
        addr = cls.get_wallet_address()
        if addr == None:
            return None
        response = requests.get(f"https://dev.explorer.hydraledger.tech:4705/api/v2/wallets/{addr}")
        if response.status_code == 200:
            data = response.json()
            balance = data['data']['balance']
            return balance
        else:
            #print("Failed to fetch data. Status code:", response.status_code) 
            return None 

    def get_account_transactions(cls):
        addr = cls.get_wallet_address()
        if addr == None:
            return None
        url = f"https://dev.explorer.hydraledger.tech:4705/api/v2/wallets/{addr}/transactions"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            return data['data']
        else:
            #print("Failed to fetch data. Status code:", response.status_code)
            return [] 
        

    @classmethod
    def delete_account(cls,index):
        wallets = cls.load_wallets()
        wallets.pop(int(index))
        with open(cls.file_path, 'w') as json_file:
            json.dump(wallets, json_file, indent=2)

    
    @classmethod
    def generate_statement(cls,statement,password):
        data = {
                "claim": {
                    "subject": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
                    "content": {
                        "userId": "5d5d9eda-d3a9-4347-b4ae-b176b75dcf51",
                        "fullName": {
                            "nonce": iop.generate_nonce(),
                            "value": statement['name']
                        },
                        "birthDate": {
                            "nonce": iop.generate_nonce(),
                            "value": statement["dob"]
                        },
                        "address": {
                            "nonce": iop.generate_nonce(),
                            "value": {
                                "country": {
                                    "nonce": iop.generate_nonce(),
                                    "value": statement["country"]
                                },
                                "city": {
                                    "nonce": iop.generate_nonce(),
                                    "value": statement["city"]
                                },
                                "street": {
                                    "nonce": iop.generate_nonce(),
                                    "value": statement["street"]
                                },
                                "zipcode": {
                                    "nonce": iop.generate_nonce(),
                                    "value": statement["zipcode"]
                                }
                            }
                        },
                        
                    }
                },
                "processId": "cjuQR3pDJeaiRv9oCZ-fBE7T8QWpUGfjP40sAXq0bLwr-8",
                "constraints": {
                    "authority": cls.generate_did(password),
                    "witness": "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw",
                    "content": None
                },
                "nonce": iop.generate_nonce(),
                }
        return data
            
    @classmethod
    def generate_and_sign_statement(cls,statement,password):
        data = cls.generate_statement(statement,password)
        signed_statement = cls.sign_witness_statement(password,json.dumps(data))
        home_directory = os.path.expanduser("~")
        try:
            with open(home_directory+'/.hydra_statements', 'r') as file:
                data = json.load(file)
                data.append(json.loads(signed_statement)) #here
            with open(home_directory+'/.hydra_statements', 'w') as json_file:
                json.dump(data, json_file,indent=2)
            return signed_statement
        except FileNotFoundError:
            my_statements = []
            my_statements.append(json.loads(signed_statement)) #here
            f1 = os.open (home_directory+"/.hydra_statements", os.O_CREAT, 0o700)
            os.close (f1)
            with open(home_directory+'/.hydra_statements', 'a') as json_file:                
                json.dump(my_statements, json_file, indent=2)
            return signed_statement
            
        
        





















