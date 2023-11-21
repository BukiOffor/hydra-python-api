


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

`hydra.py` contains a module that interacts with the hydra testnet. To use the module, you can import the `HydraWallet` class from hydra.py.

```python
from hydra import HydraWallet
```

The `HydraWallet` contains methods that can be used to interacts with the chain, once instanciated with a seed phrase.

```python
password = "password"
myWallet = HydraWallet("blind market ability .....", password)
```
Then you can perform certain transactions like transferring tokens and checking the transaction status on the blockchain.

```python
receiver = "taQb8gfnetDt6KtRH3n11M3APMzrWiBhhg"
txHash = myWallet.send_transaction(receiver,"1000000")
```
