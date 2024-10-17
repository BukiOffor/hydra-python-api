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

#### **11. `vote`**
Creates a vote transaction that empowers a delegate SecpPublicKey to validate blocks and earn rewards for doing so.
```python
nonce = 30
phrase = iop.generate_phrase()
vault = iop.get_hyd_vault(phrase, password,'mainnet',0)
vote = iop.vote(vault,nonce,password,0,0,'mainnet','039682767ffe835da2887c0fb948d32627af2e10c07c5c0cfc6b6162fc3ad2d914')
print(vote)
>>> {"transactions":[{"version":2,"network":100,"typeGroup":1,"type":3,"asset":{"votes":["+039682767ffe835da2887c0fb948d32627af2e10c07c5c0cfc6b6162fc3ad2d914"]},"nonce":"31","senderPublicKey":"02fe94408f81dec1f7172c4427b0a023b0973ce8e3dfb326352834c84ece2a46c1","fee":"100000000","amount":"0","id":"6701fd63af8f4d6216d9e9dcb43dd570eabbaae4e04158f6716f8aaae6a5c7c0","signature":"3045022100f08554468648dbe09f58a402957c63b7cc48a8c5be584f8cf08047495eec6be102206d4e5851832dcb142dcc558b824e0f7b6b33bf8e29caa76c7812324857d9a288"}]}
```

#### **12. `unvote`**
Creates an unvote transaction that revokes empowerment from a delegate {@SecpPublicKey} to validate blocks.
```python
nonce = 31
phrase = iop.generate_phrase()
vault = iop.get_hyd_vault(phrase, password,'mainnet',0)
unvote = iop.unvote(vault,nonce,password,0,0,'mainnet','039682767ffe835da2887c0fb948d32627af2e10c07c5c0cfc6b6162fc3ad2d914')
print(unvote)
>>> {"transactions":[{"version":2,"network":100,"typeGroup":1,"type":3,"asset":{"votes":["-039682767ffe835da2887c0fb948d32627af2e10c07c5c0cfc6b6162fc3ad2d914"]},"nonce":"32","senderPublicKey":"02fe94408f81dec1f7172c4427b0a023b0973ce8e3dfb326352834c84ece2a46c1","fee":"100000000","amount":"0","id":"f1171d41af02681f6a938e14ef5cab00436c05d75fdb89f131d7e521975c8520","signature":"304402200a8ce3b1ce634ed1262e1d3c2269c8a196cfa46860e6a2b4ff7ae7ffddea71be022043db63fa8ff8084e3f59caaf9b5571de96d4da0e8ec107dddba2b13be1df17c5"}]}
```

#### **13. `register_delegate`**
Creates a transaction that registers a delegate so it can validate blocks and earn rewards for doing so. If there is not enough balance on the delegate's address, other addresses can vote for the delegate with their own balance and if the sum of these are in the top 53 (or the limit on the actual network), they can validate blocks in the coming rounds.
```python
nonce = 32
phrase = iop.generate_phrase()
vault = iop.get_hyd_vault(phrase, password,'mainnet',0)
response = iop.register_delegate(vault,nonce,password,0,0,'mainnet','buki_the_goat')
print(response)
>>> {"transactions":[{"version":2,"network":100,"typeGroup":1,"type":2,"asset":{"delegate":{"username":"buki_the_goat"}},"nonce":"33","senderPublicKey":"02fe94408f81dec1f7172c4427b0a023b0973ce8e3dfb326352834c84ece2a46c1","fee":"2500000000","amount":"0","id":"7f86c2ff316cb53d16394c6aae5125f2ebf9eb6d991e593d1628fc805c6fa6ac","signature":"3045022100e069a70f977374311bf46c97b0eee26964d314dabda75e574bfe280746731fce02204e9da37c6e83db42b62253ad33d925aac324368ecc8d84df47c8ce49ea193505"}]}
```
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
