from api.hydra import HydraChain, HydraWallet
import json


#implement your logic here
chain =  HydraChain()
wallet = HydraWallet()


nonce = chain.generate_nonce()
print(nonce)