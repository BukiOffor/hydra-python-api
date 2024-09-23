# **Hydra-Python-API** 
![Rust](./core/wHyd.png)


A Python API for interacting with the Hydra-Ledger blockchain, built using **Rust** and **WASM** through **Maturin**.

## **Project Structure**

```bash
hydra-python-api
├── Cargo.lock
├── Cargo.toml
├── pyproject.toml
├── src
│   ├── api.rs
│   ├── lib.rs
│   ├── types.rs
│   └── main.rs
├── scripts
│   └── index.py
├── core
├── requirements.txt
├── README.md
└── Dockerfile
```

## **Features**
- **Fast and Safe:** Leveraging Rust's low-level control for optimal performance and memory safety to prevent vulnerabilities.
- **Transaction Management:** Easily create and sign transactions on the Hydra-Ledger blockchain.
- **Seamless Integration:** Designed for easy integration into Python-based blockchain projects with minimal setup.
- **Error Handling:** Graceful management of transaction failures with Python exceptions propagated from the Rust layer.

---

## **Building From Source**

### Prerequisites
- **Rust**
- **Maturin**
- **Python 3.8+**

### Steps to Build

1. Enter the project base directory and activate the virtual environment:
   ```bash
   source env/bin/activate
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the Python wheel for the Rust code:
   ```bash
   maturin develop
   ```

---

## **Installation**

Alternatively, install the package directly from `pip`:

```bash
pip install iop-python
```

---

## **Usage**

This API provides a Python wrapper over several Rust functions that interact with the IOP SDK to manage operations on the Hydra-Ledger blockchain.

### **Initializing the SDK**

```python
import iop_python as sdk
iop = sdk.IopPython()
```

### **Examples of Available Methods**

#### **1. `get_hyd_vault`**  
Initializes a Hydra vault and returns account information as a JSON string. This information includes an encrypted seed and derived public key

```python
phrase = "blind market ability shoot topple..."
password = "horse-staple-battery"
network = "devnet"
account = 0
hyd_vault = iop.get_hyd_vault(phrase, password, network, account)
```

#### **2. `get_morpheus_vault`**  
Initializes a Morpheus vault and returns admin information as a JSON string.

```python
phrase = "blind market ability shoot topple..."
password = "horse-staple-battery"
morpheus_vault = iop.get_morpheus_vault(phrase, password)
```

#### **3. `generate_nonce`**  
Generates a random nonce and returns it as a string.

```python
nonce = iop.generate_nonce()
print(nonce)
>>> "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw"
```

#### **4. `generate_phrase`**  
Generates a random mnemonic phrase and returns it as a string.

```python
phrase = iop.generate_phrase()
print(phrase)
>>> "blind market ability shoot topple..."
```

#### **5. `generate_did_by_morpheus`**  
Generates a Decentralized Identifier (DID) using a Morpheus vault.

```python
password = "horse-staple-battery"
idx = 0
morpheus_vault = iop.get_morpheus_vault(phrase, password)
did = iop.generate_did_by_morpheus(morpheus_vault, password, idx)
print(did)
>>> did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr
```

#### **6. `sign_witness_statement`**  
Signs a witness statement using a Hydra vault.

```python
network = "devnet"
account = 0
idx = 0
vault = iop.get_hyd_vault(phrase, password, network, account)

statement = {
    "name": "Buki Offor",
    "street": "Brick City Estate",
    "dob": "01/03/1980",
    "city": "Abuja",
    "country": "Nigeria",
    "zipcode": "987554",
}

signed_statement = iop.sign_witness_statement(vault, password, statement, idx)
print(json.loads(signed_statement))
```

#### **7. `sign_transaction`**  
Builds a transaction to transfer tokens using a Hydra vault.

```python
receiver = "taQb8gfnetDt6KtRH3n11M3APMzrWiBhhg"
amount = "100"
nonce = 1
account = 0
idx = 0
network = "testnet"
fee = 10000
comment = "sending money"

tx_data = iop.sign_transaction(vault, receiver, amount, nonce, password, account, idx, network, comment, fee)
```

#### **8. `verify_signed_statement`**  
Verifies the signature of a signed witness statement.

```python
signed_statement = {
    "signature": "00987890098776556667788976676787655",
    "claim": {
        "subject": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
        "content": {}
    }
}
result = iop.verify_signed_statement(signed_statement)
print(result)
>>> True
```

#### **9. `validate_statement_with_did`**  
Validates a signed witness statement using a DID document.

#### **10. `sign_did_statement`**  
Signs a data payload using a Morpheus vault, returning the signed data and corresponding public key.

---

# **Exceptions**
You can catch exceptions and log helpful messages during debugging.
```python
import iop_python as sdk
iop = sdk.IopPython()

try:
    phrase = iop.generate_phrase()
    vault = iop.get_hyd_vault(phrase, "password",'mainnet',0)
    address = iop.get_wallet_address(vault,9,0,'mainnet')
    print(address)
except Exception as err:
    if type(err).__name__ == 'PyIopError':
        print(err.args[0].message)
    else:
        print(err)
```



These functions are intended to be used as Python module functions and can be easily integrated into your Hydra-Ledger blockchain projects.
