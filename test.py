import iop_python as iop
from api import hydra
import requests
import json


mywallet = hydra.HydraWallet()



phrase = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"
wallet = iop.get_morpheus_vault(phrase,"pass")



password="horse-staple-God"
data = iop.get_hyd_vault(phrase,password,"mainnet")
wallet = iop.get_wallet(data,0,"mainnet")
print(wallet) # hVKiVHyKFzsm2MdKR2NxBCs3K8EoKGz3Dq
comment = 'sending money'
fee = 1000000
response = iop.generate_transaction(data,"hbnPgtVbYkDQkcWA47nbdZNfbstYQUay9D",50000000,8,password,0,"mainnet",comment,fee) # send 0.5
print(response)
url = "http://explorer.hydraledger.tech:4703/api/v2/transactions"
# res = requests.post(url, json=json.loads(response))
# response = res.json()
# print(response)
