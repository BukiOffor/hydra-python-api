


# Hydra-Python-API

Building a python Api for hydra-ledger blockchain using Maturin and Rust wasm


## Installation
### Prerequisite

* Rust
* virtualenv (optional)


Enter the base directory of the project and activate the virtual environment with the following command and install the required python packages.

```bash
source env/bin/activate
pip install iop-python
```

## Usage

`iop-python` contains a module that interacts with the hydraledger blockchain. The module contains methods that can be used to interact with the chain, once instanciated with a seed phrase.

```python
import iop-python as iop
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

## Milestone Two
### Using the DID persona on chain

This milestone uses the `HydraChain` class from the hydra module to achieve its aim.

To generate a 24 word phrase, we call the `generate_wallet()` method from our module. This function takes a password.
```python
from hydra import HydraChain
password = "horse-staple-attack"
vault = HydraChain.generate_wallet(password)
```
The above code will generate a 24 word phrase and stores it in a `.hydra_wallet` file in the home directory with a permission of `077`. 

To generate a persona did on chain, we use the method `generate_did()`. This function reads the `.hydra_wallet` file and generates a did persona with the seed phrase.

```python
from hydra import HydraWallet
password = "password"
myWallet = HydraWallet("blind market ability .....", password)
did = myWallet.generate_did()
print(did)
>>> did:morpheus:ez22Y8sKi9g18FU9ofVMbb2aD
```

To sign a witness statement, we use the `sign_witness_statements()` method. This method from  `HydraWallet` takes an object of the neccesary parameters and signs them using the users credential.

```python
from hydra import HydraWallet
password = "password"
myWallet = HydraWallet("blind market ability .....", password)
data = {"claim":"subject":{}...}
signed_statement = myWallet.sign_witness_statements(data)
```
A method that verifies a signed statement can also be found in the modules
```python
chain = HydraChain()
result = chain.verify_signed_statement(signed_statement)
print(result)
>>> True
```

## WALLET APPLICATION

To spin up the wallet application run the command below in the base directory

```bash
source env/bin/activate && python3 app.py
```
