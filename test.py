import iop_python as iop
import json

phrase = iop.generate_phrase()
wallet = iop.get_hyd_vault(phrase, "password")
#wallet = json.dumps(wallet)
#did = iop.generate_did_by_morpheus(wallet, "password")
addr = iop.get_wallet(wallet)
print(addr)
