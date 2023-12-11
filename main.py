from hydra import HydraChain, HydraWallet
import iop_python as iop
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

print(data)

#wallet = chain.generate_wallet("password")
#print(wallet)

#wallets = chain.load_wallets()
#print(wallets[0][0]["encryptedSeed"])
# wallet = json.dumps(wallets[1])
# pk = iop.deserialize(wallet, "password")
# print(pk)

#wallet = HydraWallet()
# wallet.generate_wallet("password")
#phrase = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"
#vault = wallet.recover_wallet("password",phrase)

# res = wallet.send_transaction("taQb8gfnetDt6KtRH3n11M3APMzrWiBhhg",100,"password")
# print(res)

# res = wallet.check_transaction("60607b8ee666f9405815ea8f608610fa89bdd04b30190b2a204f31ac2f072183")
# print(res)
