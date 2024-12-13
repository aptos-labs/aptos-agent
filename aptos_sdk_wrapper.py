import os
from dotenv import load_dotenv
from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.aptos_token_client import AptosTokenClient
from aptos_sdk.async_client import FaucetClient, RestClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload
from aptos_sdk.bcs import Serializer

# Load environment variables
load_dotenv()

# Environment variables
# NODE_URL = os.getenv("APTOS_NODE_URL")
# FAUCET_URL = os.getenv("APTOS_FAUCET_URL")
# FAUCET_AUTH_TOKEN = os.getenv("FAUCET_AUTH_TOKEN")

# # Print environment variables for debugging
# print(f"NODE_URL: {NODE_URL}")
# print(f"FAUCET_URL: {FAUCET_URL}")
# print(f"FAUCET_AUTH_TOKEN: {FAUCET_AUTH_TOKEN}")

# Initialize clients
rest_client = RestClient("https://api.testnet.aptoslabs.com/v1")
faucet_client = FaucetClient("https://faucet.testnet.aptoslabs.com", rest_client)
token_client = AptosTokenClient(rest_client)

async def fund_wallet(wallet_address, amount):
    """Funds a wallet with a specified amount of APT."""
    print(f"Funding wallet: {wallet_address} with {amount} APT")
    amount = int(amount)
    if amount > 1000:
        raise ValueError("Amount too large. Please specify an amount less than 1000 APT")
    octas = amount * 10**8  # Convert APT to octas
    if isinstance(wallet_address, str):
        wallet_address = AccountAddress.from_str(wallet_address)

    txn_hash = await faucet_client.fund_account(wallet_address, octas, True)
    print(f"Transaction hash: {txn_hash}\nFunded wallet: {wallet_address}")
    return wallet_address

async def get_balance(wallet_address):
    """Retrieves the balance of a specified wallet."""
    print(f"Getting balance for wallet: {wallet_address}")
    if isinstance(wallet_address, str):
        wallet_address = AccountAddress.from_str(wallet_address)
    balance = await rest_client.account_balance(wallet_address)
    balance_in_apt = balance / 10**8  # Convert octas to APT
    print(f"Wallet balance: {balance_in_apt:.2f} APT")  # Show balance with 2 decimal places
    return balance

async def transfer(sender: Account, receiver, amount):
    """Transfers a specified amount from sender to receiver."""
    if isinstance(receiver, str):
        receiver = AccountAddress.from_str(receiver)
    txn_hash = await rest_client.bcs_transfer(sender, receiver, amount)
    print(f"Transaction hash: {txn_hash} and receiver: {receiver}")
    return txn_hash

async def create_token(sender: Account, name: str, symbol: str, icon_uri: str, project_uri: str):
    """Creates a token with specified attributes."""
    print(f"Creating FA with name: {name}, symbol: {symbol}, icon_uri: {icon_uri}, project_uri: {project_uri}")
    payload = EntryFunction.natural(
        "0xe522476ab48374606d11cc8e7a360e229e37fd84fb533fcde63e091090c62149::launchpad", #(testnet)
        # "0x7cbd42946eda9349217568ef9a6a98c9b3dd9fcb4a8e98c23d6881dd6ea7251a::launchpad", #(devnet)
        "create_fa_simple",
        [],
        [
            TransactionArgument(name, Serializer.str),
            TransactionArgument(symbol, Serializer.str),
            TransactionArgument(icon_uri, Serializer.str),
            TransactionArgument(project_uri, Serializer.str),
        ]
    )
    signed_transaction = await rest_client.create_bcs_signed_transaction(
        sender, TransactionPayload(payload)
    )
    txn_hash = await rest_client.submit_bcs_transaction(signed_transaction)
    print(f"Transaction hash: {txn_hash}")
    return txn_hash