import iop_python as iop

phrase = iop.generate_phrase()
wallet = iop.test_wallet(phrase, "password")
print(wallet)