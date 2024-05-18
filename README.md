


# Hydra-Python-API

Building a python Api for hydra-ledger blockchain using Maturin and Rust wasm


## Installation
### Prerequisite

* Rust
* Maturin
* Python > 3.8

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

This code snippet contains a python wrapper over several Rust functions that interact with the IOP SDK and perform various operations related to the IOP blockchain. Here is a brief description of some function:

```python
import iop_python as iop
```

- `get_hyd_vault`: Initializes a Hydra vault and returns the admin information as a JSON string.
```python
password = "horse-staple-battery"
network = "devnet"
hyd_vault = iop.get_hyd_vault(phrase,password,network)
```
- `get_morpheus_vault`: Initializes a Morpheus vault and returns the admin information as a JSON string.
```python
password = "horse-staple-battery"
morpheus_vault = iop.get_morpheus_vault(phrase,password)
```
- `generate_nonce`: Generates a random nonce and returns it as a string.
```python
phrase = iop.generate_nonce()
print(nonce)
>>> "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw"
```
- `generate_phrase`: Generates a random mnemonic phrase and returns it as a string.
```python
phrase = iop.generate_phrase()
print(phrase)
>>> "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"
```
- `generate_did_by_morpheus`: Generates a DID (Decentralized Identifier) using a Morpheus vault and returns it as a string.
 ```python
password = "horse-staple-battery"
morpheus_vault = iop.get_morpheus_vault(phrase,password)
did = iop.generate_did_by_morpheus(morpheus_vault)
print(did)
>>> did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr
 ```
- `sign_witness_statement`: Signs a witness statement using a Morpheus vault and returns the signed statement as a JSON string.
```python
# network can be mainnet, devnet or testnet
network = "devnet"
vault = iop.get_hyd_vault(phrase,password,network)
statement = {
    "name":"Buki Offor",
    "street": "Brick City Estate",
    "dob": "01/03/1980",
    "city": "Abuja",
    "country": "Nigeria",
    "zipcode": "987554",

}
signed_witness_statement = iop.sign_witness_statement(vault,statement,password)
print(json.loads(signed_witness_statement))
```
- `generate_transaction`: Builds a transaction to transfer a certain amount of tokens to a specified recipient using a Hydra vault and returns the transaction data as a JSON string. This transaction data can be sent to a node to validate and perform the transaction. 

```python
receiver = "taQb8gfnetDt6KtRH3n11M3APMzrWiBhhg"
amount = "100"
nonce = 1
key = 0
network = "devnet"
tx_data = iop.generate_transaction(vault,receiver,amount,nonce,password,key,network)
```

- `verify_signed_statement`: Verifies the signature of a signed witness statement and returns a boolean indicating whether the signature is valid.

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
- `validate_statement_with_did`: Validates a signed witness statement using a DID document and returns the validation result as a JSON string.
- `sign_did_statement`: Signs a data payload using a Morpheus vault and returns the signed data and the corresponding public key as strings.


These functions are intended to be used as Python module functions and can be imported and called from Python code.