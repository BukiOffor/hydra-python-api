import iop_python as sdk
#import requests
import json

iop = sdk.IopPython()
mainnet_phrase="effort alarm inject boss spin ramp barely evolve expand across hawk capital village traffic sure trap basic cross volume keep fantasy bulk diesel cool"
password="horse-staple-God"
hyd = iop.get_hyd_vault(mainnet_phrase,password,"mainnet",0)
nonce = 30

try:
    phrase = iop.generate_phrase()
    vault = iop.get_hyd_vault(mainnet_phrase, password,'mainnet',0)
    vote = iop.register_delegate(vault,nonce,password,0,0,'mainnet','buki_the_goat')
    print(vote)
except Exception as err:
    if type(err).__name__ == 'PyIopError':
        print(err.args[0].message)
    else:
        print(err)







