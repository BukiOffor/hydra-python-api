from pathlib import Path
import sys
from flask import Flask
import iop_python as iop
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from keys.main import load_priv_key, load_pub_key
from flask import Flask, request, send_file
from flask_cors import CORS
import rsa


app = Flask(__name__)
CORS(app)

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

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        file_in_temp_mem = file.read()
        
        return send_file(zip_result, mimetype='application/zip', as_attachment=True, download_name=f'results_{dt_now}.zip')
    except KeyError:
        return 'No file uploaded.', 400

    except Exception as e:
        return f'An error occurred: {str(e)}', 500


"""
    This route simulates a transaction where a user makes a request to the service.
    The request body contains a cipher encrypted with servers public key and the
    public key of the user making a request. The public key of the server is
    served in the `/key`route. The ciphers(request && response) are encoded in a hex
    format for easy json parsing while the message (decrypted payload) is in a binary format
"""

@app.route('/simulate', methods=['POST'])
def decrypt():
    if request.method == "POST":
        # accesing the passed payload
        payload = request.get_json()
        cipher = payload['cipher']
        kpub = payload['key']
        
        # decrypting the file
        # a decrypted file will remain in binary format, so remeber to decryt
        # convert cipher back to bytes, because it was conveted to hex inorder to be parsed by json
        message = decrypt_file(bytes.fromhex(cipher)) 
        pub_key = rsa.PublicKey.load_pkcs1(bytes.fromhex(kpub))
        blob = encrypt_file(b"this is a test",pub_key )
        
        # convert encryped file to hex, so it can be json parsed
        # decode message to text, so it can be parsed
        data = {
            "message": message.decode(),
            "blob": blob.hex()
        
        }
        return data







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)