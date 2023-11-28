from hydra import HydraChain, HydraWallet
import json
#implement your logic here

data = {
  "claim": {
    "subject": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
    "content": {
        "userId": "5d5d9eda-d3a9-4347-b4ae-b176b75dcf51",
        "fullName": {
            "nonce": "u2YZQMQvNECwvyZOAzDkjCrNTYsH0kzyoLWvzTL6YfRbM",
            "value": "John Doe"
        },
        "address": {
            "nonce": "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw",
            "value": "6 Unter den Linden, Berlin, Germany"
        }
    }
  },
  "processId": "cjuQR3pDJeaiRv9oCZ-fBE7T8QWpUGfjP40sAXq0bLwr-8",
  "constraints": {
      "after": "",
      "before": "",
    "authority": "did:morpheus:ezbeWGSY2dqcUBqT8K7R14xr",
    "witness": "uVIc9J4UjKx8tRs6HUEDQElksBCtF9VnHb439boVmB9cw",
    "content": ""
  },
  "nonce": "uB8K6EPgZkeP8FVK0tU9RWqBFw3JM2lTaZFhMUWcKY9nh",
}

data = json.dumps(data)


phrase = HydraChain.sign_witness_statements(data)


#print(phrase)

