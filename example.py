"""
Example script demonstrating how to use the Trading Bot
"""

from bot import BasicBot

# Replace with your actual API credentials
API_KEY = 'your_api_key_here'
API_SECRET = 'your_api_secret_here'

def main():
    """Example usage of the trading bot"""
    
    # Initialize the bot with testnet
    print("Initializing bot...")
    bot = BasicBot(API_KEY, API_SECRET, testnet=True)
    
    # Check account balance
    print("\nChecking account balance...")
    balance = bot.get_account_balance()
    print(f"Available balance: {balance['available_balance']} USDT")
    
    # Example: Place a market order (commented out to prevent accidental execution)
    # print("\nPlacing market order...")
    # response = bot.place_market_order(
    #     symbol='BTCUSDT',
    #     side='BUY',
    #     quantity=0.001
    # )
    # print(f"Order ID: {response['orderId']}")
    
    # Example: Place a limit order
    # print("\nPlacing limit order...")
    # response = bot.place_limit_order(
    #     symbol='BTCUSDT',
    #     side='SELL',
    #     quantity=0.001,
    #     price=50000.0
    # )
    # print(f"Order ID: {response['orderId']}")
    
    # Example: Place a stop-limit order
    # print("\nPlacing stop-limit order...")
    # response = bot.place_stop_limit_order(
    #     symbol='BTCUSDT',
    #     side='SELL',
    #     quantity=0.001,
    #     price=49000.0,
    #     stop_price=50000.0
    # )
    # print(f"Order ID: {response['orderId']}")
    
    print("\nExample completed!")

if __name__ == '__main__':
    main()

