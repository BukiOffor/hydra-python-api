from api.hydra import HydraWallet
import iop_python as iop
import json
import requests

wallets = HydraWallet()

data = wallets.load_wallets()

addr = wallets.get_wallet_address(key=2)
print(addr)

