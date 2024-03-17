import json
from flask import Flask, request, jsonify
import iop_python as iop

# Create a Flask app

app = Flask(__name__)

employees = [ { 'id': 1, 'name': 'Ashley' }, { 'id': 2, 'name': 'Kate' }, { 'id': 3, 'name': 'Joe' }]

@app.route('/', methods=['GET'])
def index():
    nonce = iop.generate_nonce()
    return jsonify(nonce)

if __name__ == '__main__':
    app.run(debug=True, port=5000)