from hydra import HydraChain, HydraWallet


#implement your logic here

phrase = HydraChain.generate_wallet("password")


print(phrase)