# 🌐 Aptos Agent

Aptos Agent is a Python-based application designed to interact with the Aptos Layer 1 blockchain. It utilizes the Aptos SDK to perform various blockchain operations such as funding wallets, checking balances, transferring assets, and creating tokens. Additionally, it can post tweets.

**Note**: This is an experimental framework currently operating on the Aptos Devnet. Users are encouraged to fork the repository to make any changes or enhancements.

## 📁 Project Structure

- **`agents.py`**: This file contains the main logic for the Aptos Agent, including functions for blockchain interactions and other utilities like sending emails and posting tweets. It also initializes the agent with specific instructions and callable functions.

- **`aptos_sdk_wrapper.py`**: This file provides a wrapper around the Aptos SDK, offering asynchronous functions to interact with the blockchain. It includes functions to fund wallets, get balances, transfer assets, and create tokens.

- **`main.py`**: This script is the entry point for running the Aptos Agent. It loads environment variables and starts the agent's demo loop, ensuring the event loop is properly closed after execution.

## 🌟 Features

### 🤖 Agent Functionality

- **Fund Wallet**: `fund_wallet_in_apt_sync(amount: int)`  
  Funds the agent's wallet with a specified amount of APT. It uses the Aptos SDK to interact with the blockchain and handle the transaction.

- **Get Balance**: `get_balance_in_apt_sync()`  
  Retrieves the balance of the agent's wallet in APT. This function queries the blockchain to get the current balance.

- **Transfer Assets**: `transfer_in_octa_sync(sender, receiver, amount: int)`  
  Transfers a specified amount of APT from the sender to the receiver. It ensures the transaction is processed on the blockchain.

- **Create Token**: `create_token_sync(sender, name: str, symbol: str, icon_uri: str, project_uri: str)`  
  Creates a new token on the Aptos blockchain with the specified attributes. This function allows for the deployment of custom tokens.

### Additional Features

- **Post Tweet**: `post_tweet(tweet_text: str)`  
  Posts a tweet with the specified text using the Twitter API. It handles authentication and error management for the request.

## 🛠️ Setup

**Environment Variables**:
   Create a `.env` file in the root directory and add the following environment variables:
   ```plaintext
   OPENAI_API_KEY=<your_openai_api_key>

   # Optional
   TWITTER_API_KEY=<your_twitter_api_key>
   TWITTER_API_SECRET=<your_twitter_api_secret>
   TWITTER_ACCESS_TOKEN=<your_twitter_access_token>
   TWITTER_ACCESS_TOKEN_SECRET=<your_twitter_access_token_secret>
   ```

## 🚀 Usage

To install the required dependencies, execute the following command:
```bash
pip install -r requirements.txt
```

To run the Aptos Agent, execute the following command:
```bash
python main.py
```

This will start the agent and execute the demo loop, allowing it to perform blockchain operations and other tasks as defined in the `agents.py` file.


## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.