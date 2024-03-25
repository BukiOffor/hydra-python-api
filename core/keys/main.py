# -*- coding: utf-8 -*-
import rsa, os

def main():
    pass


def load_priv_key(path):
    """Load the private key."""
    try:
        with open(path, mode='rb') as privatefile:
            keydata = privatefile.read()
            privkey = rsa.PrivateKey.load_pkcs1(keydata)
            return privkey
    except FileNotFoundError as e:
        print(e)
        return None
    
def load_pub_key(path):
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)
    """Load the private key."""
    try:
        with open(path, mode='rb') as privatefile:
            keydata = privatefile.read()
            privkey = rsa.PublicKey.load_pkcs1(keydata)
            return privkey
    except FileNotFoundError as e:
        print(e)
        return None


if __name__ == '__main__':
    # Load the public and private keys. 
    main()

# pubkey = load_pub_key()
# privkey = load_priv_key()

# crypto = b"\x0e\xe4\xd8\x8a\x1b\x8e?0\x9a\xdf\xbc\x15h\x8aT\xaeN\x9a~v?\xc3\xc0D?\xc1\x8f\x83\xcfD\xf8j\x16\xa0\x0e\x8a\xeb\x19\x9d4O\xb0\x84\xa6B\tS}\\&C\xad\xbb\x9b\xd6U\x8bR\xad\x17\xde\x84\xbdU\xa8D\xc7\x85\x12\x93G=\xfb\x02\xb0|jI\xd1Z5\r\xe2\x8c\xf4\x8dN\x8c\x9e\xecF\xbft\x92{wKA\x10%p\xe27\x14\x9f\xca\xd3=\xed\xa2.'\xcc\xc0?\xca\xc3\x13XOn\xd9\xe6\x02\x12\xc0\xdf\xd8"

# message = rsa.decrypt(crypto, privkey)
# print(message.decode('utf8'))