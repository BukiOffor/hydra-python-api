import iop_python as iop
import requests
import json




async def send_transaction(phrase,receiver,amount, nonce):
    res = await iop.send_transaction_with_python(phrase,receiver,amount,nonce)
    return res


#password = "pass"
main_wallet = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"
seed = iop.generate_phrase()
password = "pass"
hyd_str = {"encryptedSeed": "uWhm03Ni8vETI_40xB1J3sMmJ6KACitSBfnw1BGS8qslKe5MbDFergj9s7_HDAZ7koMCZ5yETFocdRNW50zQM8bXH1n_SPZfn0WphgPA2BsBe7OEIcJNmak806-Zwd-viR93RHEE1A8Y","plugins": [{"pluginName": "Hydra","publicState":{"xpub":"hydmW128xSVMGShPybHckfg9To4y9tfjMNzZLiCQWEv4rJevyurx2FRTGk7v7wpDft37qtYSKdCeVdwnDSx2tDZQQbmax8XfboW4Li3aR6BA6iPL","receiveKeys":1,"changeKeys":0},"parameters":{"network":"HYD mainnet","account":0}}]}
morph = iop.get_morpheus_vault(seed,password)
hyd = iop.get_hyd_vault(seed, password, "mainnet")
#addr = iop.get_wallet(json.dumps(hyd_str),0,"mainnet")
addr = iop.get_wallet(hyd,0,"mainnet")

print(addr)





# print("mnemonic: ",seed)
# print("morpheus: ", morph)
# print("hyd:", hyd)

