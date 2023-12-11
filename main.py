from api.hydra import HydraChain, HydraWallet
import json


#implement your logic here
chain =  HydraChain()
wallet = HydraWallet()

data = {
  "claim": {
    "subject": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
    "content": {
        "userId": "5d5d9eda-d3a9-4347-b4ae-b176b75dcf51",
        "fullName": {
            "nonce": chain.generate_nonce(),
            "value": "John Doe"
        },
        "address": {
            "nonce": chain.generate_nonce(),
            "value": "6 Unter den Linden, Berlin, Germany"
        }
    }
  },
  "processId": "cjuQR3pDJeaiRv9oCZ-fBE7T8QWpUGfjP40sAXq0bLwr-8",
  "constraints": {
    "authority": wallet.generate_did("password"),
    "witness": "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw",
    "content": None
  },
  "nonce": chain.generate_nonce(),
}


# sign a witness statement with your did key
signed_witness_statement = wallet.sign_witness_statement("password",json.dumps(data))
print(json.loads(signed_witness_statement))


# sign a did statement with your did key
contractStr = "A long legal document, e.g. a contract with all details"
did_statement = wallet.sign_did_statement(contractStr,"password")
print(did_statement)



