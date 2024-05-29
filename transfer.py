from bip_utils import Bip39SeedGenerator, Bip32, Bip44, Bip44Coins
from solana.account import Account
from solana.rpc.api import Client

def generate_keypair_from_mnemonic(mnemonic):
    """Generate a keypair (public and private key) from a given mnemonic phrase.

    Args:
        mnemonic (str): The mnemonic phrase.

    Returns:
        bytes, bytes: A tuple containing the private key and the public key bytes.
    """
    # Generate a seed from the mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    # Derive a keypair from the seed
    root_key = Bip32.FromSeed(seed_bytes)
    # Derive a Solana account path
    solana_acc_path = Bip44.FromCoin(Bip44Coins.SOLANA).DeriveAccount(root_key)
    # Get the private key bytes
    private_key = solana_acc_path.PrivateKey().Raw().ToBytes()
    # Get the public key bytes
    public_key = solana_acc_path.PublicKey().RawCompressed().ToBytes()
    return private_key, public_key

def transfer_spl_token(sender_private_key, recipient_public_key, amount):
    """Transfer SPL tokens from one account to another.

    Args:
        sender_private_key (bytes): The sender's private key bytes.
        recipient_public_key (bytes): The recipient's public key bytes.
        amount (int): The amount of SPL tokens to transfer.

    Returns:
        str: The transaction signature.
    """
    # Create an account object for the sender using the private key
    sender_acc = Account(sender_private_key)
    # Define the recipient's account
    recipient_acc = recipient_public_key
    # Create a Solana RPC client
    client = Client("https://api.devnet.solana.com")
    # Build and sign the transaction to transfer tokens
    transaction = sender_acc.transfer(recipient_acc, amount)
    # Send the transaction and get the signature
    tx_sig = client.send_transaction(transaction, sender_acc)
    return tx_sig

if __name__ == "__main__":
    # This part of the code will only execute if the script is run directly
    # Replace "your twelve word mnemonic here" with your actual mnemonic
    mnemonic = "your twelve word mnemonic here"
    # Generate keypair from the mnemonic
    sender_private_key, sender_public_key = generate_keypair_from_mnemonic(mnemonic)
    # Replace "recipient_public_key_here" with the recipient's public key
    recipient_public_key = bytes.fromhex("recipient_public_key_here")
    # Define the amount of SPL token to transfer
    amount = 1000000  # Adjust as needed
    # Perform the token transfer
    transaction_signature = transfer_spl_token(sender_private_key, recipient_public_key, amount)
    # Print the transaction signature
    print("Transaction Signature:", transaction_signature)
