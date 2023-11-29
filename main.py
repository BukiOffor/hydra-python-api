from hydra import HydraChain, HydraWallet
import json

#implement your logic here
chain =  HydraChain()
nonce = chain.generate_nonce()
print(nonce)

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
    "authority": chain.generate_did(),
    "witness": "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw",
    "content": None
  },
  "nonce": chain.generate_nonce(),
}



chain = HydraChain()
data = chain.get_account_transactions("tdXxhgZV8aAGLL9CCJ4ry9AzTQZzRKqJ97")
#print(data)
for item in data:
  sender = item['sender']
  print(sender)
