import iop_python as sdk

iop = sdk.IopPython()
try:
    phrase = iop.generate_phrase()
    vault = iop.get_hyd_vault(phrase, "password",'mainnet',1)
    address = iop.get_wallet_address(vault,9,0,'mainnet')
    print(address)
except Exception as err:
    if type(err).__name__ == 'PyIopError':
        print(err.args[0].message)
    else:
        print(err)







