#import iop_python as iop
import requests
import json
import os
import rsa

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
#api = "https://iop-server.onrender.com"
api = 'http://127.0.0.1:8088'
host = "http://127.0.0.1:8088"
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
        url = f"https://dev.explorer.hydraledger.tech:4705/morpheus/v1/did/{did}/document"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            did_doc = json.dumps(data)
            result = requests.post(api+"/api/validate_statement_with_did", json={"data":signed_statement,"doc":did_doc}).json()
            return result
        

    def generate_nonce(self):
        nonce = requests.get(api+"/nonce").json()
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

    # home_directory = os.path.expanduser("~")
    # file_path = home_directory+"/.hydra_wallet"

    def __init__(self, path):
        self.file_path = path

    def generate_nonce(self):
        nonce = requests.get(api+"/nonce").text
        return nonce

    def get_server_pkey(self):
        pem_key = requests.get(f"{api}/key").content
        pubkey = rsa.PublicKey.load_pkcs1(pem_key)
        return pubkey

    def generate_phrase(self):
       self.generate_key()
       pubkey = self.load_pub_key()
       data = {"key": pubkey.save_pkcs1().hex()}
       response = requests.post(api+"/phrase", json=data).json()
       cipher = response['cipher']
       phrase =  rsa.decrypt(bytes.fromhex(cipher), self.load_priv_key())
       return (phrase.decode("utf8"))

    
    def load_wallets(self):
        try:
            with open(f"{self.file_path}/.hydra_wallet", 'r') as json_file:
                wallets = json.load(json_file)
                return wallets
        except FileNotFoundError:
            print("user does not own any wallets")
            return []


    def generate_key(self):
        if not os.path.exists(f"{self.file_path}/private.pem" and f"{self.file_path}/public.pem"):
            (pubkey, privkey) = rsa.newkeys(2048)
            # Write public key to file
            pub = pubkey.save_pkcs1()
            pubfile = open(f'{self.file_path}/public.pem', 'wb')
            pubfile.write(pub)
            pubfile.close()

            # Write private Key to file
            pri = privkey.save_pkcs1()
            prifile = open(f'{self.file_path}/private.pem', 'wb')
            prifile.write(pri)
            prifile.close()  

    def load_priv_key(self):
        """Load the private key."""
        with open(f'{self.file_path}/private.pem', mode='rb') as privatefile:
            keydata = privatefile.read()
            privkey = rsa.PrivateKey.load_pkcs1(keydata)
            return privkey
    
    def load_pub_key(self):
        """Load the public key."""
        with open(f'{self.file_path}/public.pem', mode='rb') as privatefile:
            keydata = privatefile.read()
            pubkey = rsa.PublicKey.load_pkcs1(keydata)
            return pubkey


    def generate_wallet(self, password,phrase):
        self.generate_key()
        phrase_copy = phrase
        pubkey = self.get_server_pkey()
        password = rsa.encrypt(password.encode("utf8"), pubkey)
        phrase = rsa.encrypt(phrase.encode("utf8"), pubkey)
        response = requests.post(api+"/get_hyd_vault", json={"password":password.hex(),"phrase":phrase.hex()})
        result = requests.post(api+"/get_morpheus_vault", json={"password":password.hex(),"phrase":phrase.hex()})
        if result.status_code != 200 and response.status_code != 200:
            print("Error:", result.text)
            print("Error:", response.text)
            return None            
        response = response.json()
        result = result.json()
        h_vault = json.loads(response['hyd_vault'])
        m_vault = json.loads(result['morpheus_vault'])
        vaults = []
        vaults.append(h_vault) 
        vaults.append(m_vault)
        # Check if the file does not exist

        try:
            with open(f"{self.file_path}/.hydra_wallet", 'r') as file:
                data = json.load(file)
                data.append(vaults)
            with open(f"{self.file_path}/.hydra_wallet", 'w') as json_file:
                json.dump(data, json_file,indent=2)
            return phrase_copy
        except FileNotFoundError:
            myvault = []
            myvault.append(vaults)
            # f1 = os.open (f"{self.file_path}/.hydra_wallet", os.O_CREAT, 0o700)
            # os.close (f1)
            with open(f"{self.file_path}/.hydra_wallet", 'a') as json_file:                
                json.dump(myvault, json_file, indent=2)
            return phrase_copy
    
    def get_new_acc_on_vault(self,password, account=0):
        data = self.load_wallets()
        if len(data) > 0:
            vault = data[account][0]
            new_account = vault['plugins'][-1]['parameters']['account']
            vault_data = json.dumps(vault)
            pubkey = self.get_server_pkey()
            password = rsa.encrypt(password.encode("utf8"), pubkey)
            response = requests.post(api+"/get_new_acc_on_vault", json={"vault":vault_data,"password":password.hex(),"account": new_account+1})
            if response.status_code != 200:
                print("Error:", response.text)
                return None 
            wallet = response.json()
            data[account][0] = json.loads(wallet["vault"])
            with open(f"{self.file_path}/.hydra_wallet", 'w') as json_file:                
                json.dump(data, json_file, indent=2)
            return wallet["vault"]


    def get_wallet_address(self,account=0,key=0):
        data = self.load_wallets()
        if len(data) > 0:
            vault = data[account][0]
            _params = vault['plugins'][0]['parameters']
            data = json.dumps(vault)
            params = json.dumps(_params)
            response = requests.post(api+"/get_wallet", json={"vault":data,"account":str(key)})
            if response.status_code != 200:
                print("Error:", response.text)
                return None 
            addr = response.text
            return addr
    

    def generate_did(self,password,account=0):
        file_content = self.load_wallets()
        if len(file_content) > 0:
            vault = file_content[account][1]
            vault = json.dumps(vault)
            pubkey = self.get_server_pkey()
            password = rsa.encrypt(password.encode("utf8"), pubkey)
            #did = iop.generate_did_by_morpheus(vault, password)
            response = requests.post(api+"/generate_did_by_morpheus", json={"vault": vault, "password": password.hex()})
            if response.status_code != 200:
                print("Error:", response.text)
                return None 
            did = response.text
            return did


    def recover_wallet(self,password,phrase):
        vault = self.generate_wallet(password,phrase)
        return vault

    def sign_witness_statement(self,password, data,account=0):
        file_content = self.load_wallets()
        if len(file_content) > 0:
            vault = file_content[account][1]
            vault = json.dumps(vault)
            #signed_statement = iop.sign_witness_statement(vault,password,data)
            pubkey = self.get_server_pkey()
            password = rsa.encrypt(password.encode("utf8"), pubkey)
            response = requests.post(api+"/sign_witness_statement", json={"vault":vault, "password":password.hex(), "data":data})
            if response.status_code != 200:
                print("Error:", response.text)
                return None 
            signed_statement = response.json() 
            return signed_statement["signed"]      
    
    def sign_did_statement(self,statement,password,account=0):
        wallet = self.load_wallets()
        vault = wallet[account][1]
        vault = json.dumps(vault)
        data = bytes(statement, "utf-8")
        pubkey = self.get_server_pkey()
        password = rsa.encrypt(password.encode("utf8"), pubkey)
        #signed_statement = iop.sign_did_statement(vault,password,data)
        response = requests.post(api+"/sign_did_statement", json={"vault":vault,"password":password.hex(),"data":data.hex()})
        if response.status_code != 200:
                print("Error:", response.text)
                return None 
        signed_statement = response.json() 
        details = {
            "content": statement,
            "publicKey": signed_statement["public_key"],
            "signature": signed_statement["signature"]
        }
        return json.dumps({"Signed contract":details}, indent=4)


    def get_nonce(self,key=0):
        addr = self.get_wallet_address(key=key)
        url = f"https://dev.explorer.hydraledger.tech:4705/api/v2/wallets/{addr}"
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
        salt = self.generate_nonce()
        message = receiver+amount+nonce+key+salt+password
        hash = rsa.compute_hash(message, 'SHA-1')
        #response = iop.generate_transaction(data,receiver,amount,nonce,password,key)
        pubkey = self.get_server_pkey()
        password = rsa.encrypt(password.encode("utf8"), pubkey)
        tx = { 
              "data":data,"receiver":receiver,"amount":amount,
              "nonce":nonce, "password":password.hex(), 
              "account":key, "salt":salt, "hash": hash.hex()
            }
        response = requests.post(api+"/sign_transaction", json=tx)
        if response.status_code != 200:
            return None

        signed_txs = response.json()
        #signed_txs = json.loads(response)
        return signed_txs    

    #this function assumes that the wallet has made a transaction before
    def send_transaction(self,receiver,amount,password,account=0,key=0):
        # Send a GET request to the URL
        signed_txs = self.sign_transaction(receiver,amount,password,account,key)
        url = "https://dev.explorer.hydraledger.tech:4705/api/v2/transactions"
        res = requests.post(url, json=signed_txs)
        response = res.json()
        #print(response)
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

    def display_address_balance(self):
        addr = self.get_wallet_address()
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

    def get_account_transactions(self):
        addr = self.get_wallet_address()
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
        

    def delete_account(self,index):
        wallets = self.load_wallets()
        wallets.pop(int(index))
        with open(f"{self.file_path}/.hydra_wallet", 'w') as json_file:
            json.dump(wallets, json_file, indent=2)

    
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
            
    def generate_and_sign_statement(self,statement,password):
        data = self.generate_statement(statement,password)
        signed_statement = self.sign_witness_statement(password,json.dumps(data))
        try:
            with open(f"{self.file_path}/.statements", 'r') as file:
                data = json.load(file)
                data.append(json.loads(signed_statement)) #here
            with open(f"{self.file_path}/.statements", 'w') as json_file:
                json.dump(data, json_file,indent=2)
            return signed_statement
        except FileNotFoundError:
            my_statements = []
            my_statements.append(json.loads(signed_statement)) #here
            f1 = os.open (f"{self.file_path}/.statements", os.O_CREAT, 0o700)
            os.close (f1)
            with open(f"{self.file_path}/.statements", 'a') as json_file:                
                json.dump(my_statements, json_file, indent=2)
            return signed_statement
            
        
        





















