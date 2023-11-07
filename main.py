import iop_python as iop

seedPhrase = iop.generate_phrase()
wallet = iop.get_wallet(seedPhrase)
print(wallet)
