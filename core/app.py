from flask import Flask
import iop_python as iop

app = Flask(__name__)

@app.route('/')
def hello_world():
    return iop.generate_phrase()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)