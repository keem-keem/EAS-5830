from web3 import Web3
from eth_account.messages import encode_defunct
import random
import os
import json

# Connect to Avalanche Fuji
w3 = Web3(Web3.HTTPProvider("https://api.avax-test.network/ext/bc/C/rpc"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load the ABI (paste the full ABI in a JSON file)
with open("nft_abi.json", "r") as f:
    abi = json.load(f)

# Contract setup
contract_address = Web3.to_checksum_address("0x85ac2e065d4526FBeE6a2253389669a12318A412")
contract = w3.eth.contract(address=contract_address, abi=abi)

MAX_ID = 10000

def keccak256(val):
    return int.from_bytes(w3.keccak(val), 'big')

def find_unclaimed_nonce():
    while True:
        nonce_bytes = os.urandom(32)
        nonce_hex = "0x" + nonce_bytes.hex()
        token_id = keccak256(nonce_bytes) % MAX_ID

        try:
            contract.functions.ownerOf(token_id).call()
            print(f"TokenId {token_id} already claimed.")
        except:
            print(f"\n✅ Unclaimed token found!")
            print(f"Nonce (bytes32): {nonce_hex}")
            print(f"TokenId: {token_id}")
            return

find_unclaimed_nonce()


def sign_challenge( challenge ):

    w3 = Web3()

    """ To actually claim the NFT you need to write code in your own file, or use another claiming method
    Once you have claimed an NFT you can come back to this file, update the "sk" and submit to codio to 
    prove that you have claimed your NFT.
    
    This is the only line you need to modify in this file before you submit """
    sk = "0x3555c896c1e5c22f9df6e64de5eb2e33a0e54834c6e845b57a069ce5218c2e46"

    acct = w3.eth.account.from_key(sk)

    signed_message = w3.eth.account.sign_message( challenge, private_key = acct.key )

    return acct.address, signed_message.signature


def verify_sig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing 
    """
    
    challenge_bytes = random.randbytes(32)

    challenge = encode_defunct(challenge_bytes)
    address, sig = sign_challenge( challenge )

    w3 = Web3()

    return w3.eth.account.recover_message( challenge , signature=sig ) == address


if __name__ == '__main__':
    """
        Test your function
    """
    if verify_sig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )
