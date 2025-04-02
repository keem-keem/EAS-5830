from web3 import Web3
from eth_account.messages import encode_defunct
import eth_account
import os
from eth_account import Account

def sign_message(challenge, filename="secret_key.txt"):
    """
    challenge - byte string
    filename - filename of the file that contains your account secret key
    To pass the tests, your signature must verify, and the account you use
    must have testnet funds on both the bsc and avalanche test networks.
    """
    # This code will read your "sk.txt" file
    # If the file is empty, it will raise an exception
    with open(filename, "r") as f:
        key = f.readlines()
    assert(len(key) > 0), "Your account secret_key.txt is empty"
    
    key = key[0].strip()
    
    print(f'Key: {key}')
    print(f'Challenge: {challenge}')
    
    w3 = Web3()
    
    # TODO recover your account information for your private key and sign the given challenge
    # Use the code from the signatures assignment to sign the given challenge

    account = Account.from_key(key)
    eth_addr = account.address
    private_key = account.key

    # From signatures.py: sign the given message
    signed_message = account.sign_message(challenge, key)  # Sign the message
    assert account.Account.recover_message(message,signature=signed_message.signature.hex()) == eth_addr, f"Failed to sign message properly"

    #return signed_message, account associated with the private key
    return signed_message, eth_addr


if __name__ == "__main__":
    for i in range(4):
        challenge = os.urandom(64)
        sig, addr= sign_message(challenge=challenge)
        print( addr )
