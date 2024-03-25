"""
    This project implements a transaction where a user makes a request to a service.
    The request body contains a cipher encrypted with servers public key and the
    public key of the user making a request. The public key of the server is
    served in the `/key`route. The ciphers(request && response) are encoded in a hex
    format for easy json parsing while the message (decrypted payload) is in a binary format
"""

from pathlib import Path
import sys
from flask import Flask
import iop_python as iop
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from flask import Flask, request, send_file
from flask_cors import CORS
import rsa


app = Flask(__name__)
CORS(app)

def load_priv_key(path):
    """Load the private key."""
    with open(path, mode='rb') as privatefile:
        keydata = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)
        return privkey
    
def load_pub_key(path):
    """Load the bobs private key."""
    with open(path, mode='rb') as privatefile:
        keydata = privatefile.read()
        pubkey = rsa.PublicKey.load_pkcs1(keydata)
        return pubkey

# get keys 
def get_keys():
    return (load_priv_key("keys/private.pem"), load_pub_key("keys/public.pem"))

# decrypt a file
def decrypt_file(cipher):
    priv_key, pub_key = get_keys()
    data = rsa.decrypt(cipher, priv_key)
    return data

# encrypt a file
def encrypt_file(data, pub_key):
    cipher = rsa.encrypt(data, pub_key)
    return cipher



@app.route('/key')
def get_key():
    try:
        return send_file("keys/public.pem", mimetype='application/pem',
                      as_attachment=True, download_name=f'public.pem')
    except Exception as e:
        return f'An error occurred: {str(e)}', 500

@app.route('/phrase', methods=['POST'])
def get_phrase():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        # get the public key of a user
        kpub = payload['key']
        # load publickey of user into PK format
        pub_key = rsa.PublicKey.load_pkcs1(bytes.fromhex(kpub))
        phrase = iop.generate_phrase()
        # turn the phrase to bytes and encrypt it with the users private key
        cipher = encrypt_file(phrase.encode(),pub_key)
        # convert cipher(binary) to hex so it can be passed
        data = {
            "cipher": cipher.hex()        
        }
        return data


@app.route('/get_hyd_vault', methods=['POST'])
def get_hyd_vault():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        password_cipher = payload['password']
        phrase_cipher = payload['phrase']
        # decrypt password and phrase
        password = decrypt_file(bytes.fromhex(password_cipher))
        phrase = decrypt_file(bytes.fromhex(phrase_cipher))
        hyd_vault = iop.get_hyd_vault(phrase.decode("utf8"), password.decode("utf8"))
        # convert cipher(binary) to hex so it can be passed
        data = {
            "hyd_vault": hyd_vault        
        }
        return data



@app.route('/get_morpheus_vault', methods=['POST'])
def get_morpheus_vault():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        password_cipher = payload['password']
        phrase_cipher = payload['phrase']
        # decrypt password and phrase
        password = decrypt_file(bytes.fromhex(password_cipher))
        phrase = decrypt_file(bytes.fromhex(phrase_cipher))
        morpheus_vault = iop.get_morpheus_vault(phrase.decode("utf8"), password.decode("utf8"))
        data = {
            "morpheus_vault": morpheus_vault        
        }
        return data

@app.route('/get_new_acc_on_vault', methods=['POST'])
def get_new_account_on_vault():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        password_cipher = payload['password']
        vault = payload['vault']
        account = payload['account']
        # decrypt password and phrase
        password = decrypt_file(bytes.fromhex(password_cipher))
        vault = iop.get_new_acc_on_vault(vault,password.decode("utf8"), int(account))
        data = {
            "vault": vault        
        }
        return data

@app.route('/get_wallet', methods=['POST'])
def get_wallet():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        vault = payload['vault']
        account = payload['account']
        # decrypt password and phrase
        addr = iop.get_wallet(vault, int(account))
        return addr


@app.route('/generate_did_by_morpheus', methods=['POST'])
def generate_did_by_morpheus():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        password_cipher = payload['password']
        vault = payload['vault']
        # decrypt password and phrase
        password = decrypt_file(bytes.fromhex(password_cipher))
        did = iop.generate_did_by_morpheus(vault,password.decode("utf8"))
        return did




@app.route('/sign_witness_statement', methods=['POST'])
def sign_witness_statement():
    if request.method == "POST":
        try:
            # accesing the passed payload
            payload = request.get_json()
            password_cipher = payload['password']
            vault = payload['vault']
            data = (payload['data'])
            # decrypt password
            password = decrypt_file(bytes.fromhex(password_cipher))
            response = iop.sign_witness_statement(vault, password.decode("utf8"), data)
            data = {
                "signed" : response
            }
            return data
        except Exception as e:
                return f'An error occurred: {str(e)}', 500




@app.route('/sign_did_statement', methods=['POST'])
def sign_did_statement():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        password_cipher = payload['password']
        vault = payload['vault']
        dataInHex = payload['data']
        print(dataInHex)
        data = bytes.fromhex(dataInHex)
        # decrypt password
        password = decrypt_file(bytes.fromhex(password_cipher))
        response = iop.sign_did_statement(vault, password.decode("utf8"), data)
        data = {
            "signature": response[0],
            "public_key": response[1]
        }
        return data



@app.route('/nonce', methods=['GET'])
def get_nonce():
    response = iop.generate_nonce()
    return response


@app.route('/sign_transaction', methods=['POST'])
def sign_transaction():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        password_cipher = payload['password']
        vault = payload['vault']
        # decrypt password and phrase
        password = decrypt_file(bytes.fromhex(password_cipher))
        did = iop.generate_did_by_morpheus(vault,password.decode("utf8"))
        return did






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088, debug=True)