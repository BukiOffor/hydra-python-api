from pathlib import Path
import sys
from flask import Flask
import iop_python as iop
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from keys.main import load_priv_key, load_pub_key

app = Flask(__name__)

@app.route('/')
def hello_world():
    priv_key = load_priv_key("keys/private.pem")
    pub_key = load_pub_key("keys/public.pem")
    print(priv_key)
    print(pub_key)
    return iop.generate_phrase()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)