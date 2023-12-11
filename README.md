


# Hydra-Python-API

Building a python Api for hydra-ledger blockchain using Maturin and Rust wasm


## Installation
### Prerequisite

* Rust
* Maturin

Enter the base directory of the project and activate the virtual environment with the following command and install the required python packages.

```bash
source env/bin/activate
pip install -r requirements.txt
```

To compile the code, you can run the following command. This command builds a python wheel for the rust code.
```bash
maturin develop
```

## Usage

`hydra.py` contains a module that interacts with the hydra testnet. To use the module, you can import the `HydraWallet` class from api/hydra.py.

```python
from hydra import HydraWallet, HydraChain
```
A example method that verifies a signed statement can be found in the module

```python
chain = HydraChain()
signed_statement =  {
    "signature": "00987890098776556667788976676787655"
    "claim": {
    "subject": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
    "content": {}...},    
    }
result = chain.verify_signed_statement(signed_statement)
print(result)
>>> True
```

## WALLET APPLICATION

To spin up the wallet application run the command below in the base directory

```bash
source env/bin/activate && python3 app/app.py
```
