from hydra import HydraChain, HydraWallet
import json

#implement your logic here
nonce = HydraChain.generate_nonce()
print(nonce)

data = {
  "claim": {
    "subject": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
    "content": {
        "userId": "5d5d9eda-d3a9-4347-b4ae-b176b75dcf51",
        "fullName": {
            "nonce": HydraChain.generate_nonce(),
            "value": "John Doe"
        },
        "address": {
            "nonce": HydraChain.generate_nonce(),
            "value": "6 Unter den Linden, Berlin, Germany"
        }
    }
  },
  "processId": "cjuQR3pDJeaiRv9oCZ-fBE7T8QWpUGfjP40sAXq0bLwr-8",
  "constraints": {
    "authority": HydraChain.generate_did(),
    "witness": "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw",
    "content": None
  },
  "nonce": HydraChain.generate_nonce(),
}



statement = HydraChain.sign_witness_statements(data)
#statement = {"signature":{"publicKey":"pezFfvvMUjavDvpw5JEv87BrRD44PRh8yXuSyK9zZuA1nMZ","bytes":"sezB6LaumdN3VXX2kuXkenMLWWQyTVsGTdUgMbdYTAXdyyUxFesnM2fM3kXhwjvyyNpHEXDCFdtHBaRk8Ab7gaVbvrJ"},"content":{"processId":"cjuQR3pDJeaiRv9oCZ-fBE7T8QWpUGfjP40sAXq0bLwr-8","claim":{"subject":"did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr","content":{"userId":"5d5d9eda-d3a9-4347-b4ae-b176b75dcf51","fullName":{"nonce":"u2YZQMQvNECwvyZOAzDkjCrNTYsH0kzyoLWvzTL6YfRbM","value":"John Doe"},"address":{"nonce":"uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw","value":"6 Unter den Linden, Berlin, Germany"}}},"constraints":{"after":None,"before":None,"witness":"uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw","authority":"did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr","content":None},"nonce":"uB8K6EPgZkeP8FVK0tU9RWqBFw3JM2lTaZFhMUWcKY9nh"}}
result = HydraChain.verify_signed_statement(statement)
print(result)

#did = HydraChain.generate_did()
