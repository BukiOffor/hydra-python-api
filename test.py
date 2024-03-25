from api.hydra import HydraChain, HydraWallet
import json


#implement your logic here
chain =  HydraChain()
wallet = HydraWallet("/Users/mac/.hydra")


phrase = wallet.generate_phrase()
seed = wallet.get_new_acc_on_vault("password") 
print(seed)