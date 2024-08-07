# References for pycryptodome has be referred to from this site
# https://medium.com/coinmonks/rsa-encryption-and-decryption-with-pythons-pycryptodome-library-94f28a6a1816

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_keys():
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()