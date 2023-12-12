from api.hydra import HydraWallet
import iop_python as iop
import json


wallets = HydraWallet()

data = wallets.load_wallets()

vault = data[0][0]
vault = json.dumps(vault)
new_wallet = iop.get_new_acc_on_vault(vault,"password")
print(new_wallet)