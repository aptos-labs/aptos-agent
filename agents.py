import os
import json
import asyncio
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from aptos_sdk.account import Account
from aptos_sdk_wrapper import get_balance, fund_wallet, transfer, create_token
from swarm import Agent

# Load environment variables from .env file
load_dotenv()

# Initialize the event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Generate a new wallet
wallet = Account.generate()
address = str(wallet.address())

def get_weather(location, time="now"):
    """Get the current weather in a given location. Location MUST be a city."""
    return json.dumps({"location": location, "temperature": "65", "time": time})

def send_email(recipient, subject, body):
    print("Sending email...")
    print(f"To: {recipient}\nSubject: {subject}\nBody: {body}")
    return "Sent!"

def fund_wallet_in_apt_sync(amount: int):
    try:
        return loop.run_until_complete(fund_wallet(address, amount))
    except Exception as e:
        return f"Error funding wallet: {str(e)}"

def get_balance_in_apt_sync():
    try:
        return loop.run_until_complete(get_balance(address))
    except Exception as e:
        return f"Error getting balance: {str(e)}"

def transfer_in_octa_sync(sender, receiver, amount: int):
    try:
        return loop.run_until_complete(transfer(sender, receiver, amount))
    except Exception as e:
        return f"Error transferring funds: {str(e)}"

def create_token_sync(sender, name: str, symbol: str, icon_uri: str, project_uri: str):
    try:
        return loop.run_until_complete(create_token(wallet, name, symbol, icon_uri, project_uri))
    except Exception as e:
        print(f"Error creating token: {str(e)}")
        return f"Error creating token: {str(e)}"

def post_tweet(tweet_text: str):
    url = "https://api.twitter.com/2/tweets"
    
    auth = OAuth1(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    payload = {
        "text": tweet_text
    }
    
    try:
        response = requests.post(url, auth=auth, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error posting tweet: {str(e)}"
    
def close_event_loop():
    loop.close()

aptos_agent = Agent(
    name="Aptos Agent",
    model="gpt-4o",
    instructions=
    ("You are a helpful agent that can interact on-chain on the Aptos Layer 1 blockchain using the Aptos SDK. "
     "You can create custom Move modules, transfer assets, "
     "and perform token swaps. If you ever need to know your address, it is {address}. "
     "If you ever need test funds, you can request them from the Aptos Testnet Faucet. "
     "You can also deploy your own Move-based tokens, NFTs, and interact with them. "
     "If someone asks you to do something you can’t do, you can say so and encourage them to implement it themselves using the Aptos SDK. "
     "Recommend they visit aptos.dev for more information. "
     "You can also offer to help them implement it by writing the function and instructing them to add it to the agents.py file and your list of callable functions."
     ),
    functions=[
        fund_wallet_in_apt_sync, get_balance_in_apt_sync,
        transfer_in_octa_sync, create_token_sync, post_tweet
    ],
)

