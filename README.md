# Binance Futures Testnet Trading Bot

A simplified trading bot for Binance Futures Testnet that supports market, limit, and stop-limit orders with comprehensive logging and error handling.

## Features

- ✅ **Market Orders**: Execute orders at current market price
- ✅ **Limit Orders**: Place orders at specified price levels
- ✅ **Stop-Limit Orders**: Advanced order type with stop price trigger
- ✅ **Comprehensive Logging**: All API requests, responses, and errors are logged
- ✅ **Error Handling**: Robust error handling with detailed error messages
- ✅ **CLI Interface**: Easy-to-use command-line interface
- ✅ **Interactive Mode**: User-friendly interactive mode for order placement
- ✅ **Account Management**: Check balances and order status

## Prerequisites

- Python 3.7 or higher
- Binance Testnet account with API credentials

## Setup Instructions

### 1. Register Binance Testnet Account

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Sign up for a testnet account
3. Log in to the testnet platform

### 2. Generate API Credentials

1. Go to your testnet account settings
2. Navigate to API Management
3. Create a new API key
4. Save your **API Key** and **API Secret** securely
   - ⚠️ **Important**: Never share your API credentials or commit them to version control

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended for Beginners)

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET --interactive
```

This will launch an interactive menu where you can:
- Place orders
- Check account balance
- Check order status
- Cancel orders

### Command-Line Mode

#### Place a Market Order

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET \
  --order-type market --symbol BTCUSDT --side BUY --quantity 0.001
```

#### Place a Limit Order

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET \
  --order-type limit --symbol BTCUSDT --side SELL --quantity 0.001 --price 50000
```

#### Place a Stop-Limit Order

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET \
  --order-type stop-limit --symbol BTCUSDT --side SELL \
  --quantity 0.001 --price 49000 --stop-price 50000
```

#### Check Account Balance

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET --balance
```

#### Check Order Status

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET \
  --order-status --symbol BTCUSDT --order-id 123456
```

#### Cancel an Order

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET \
  --cancel-order --symbol BTCUSDT --order-id 123456
```

### Using as a Python Module

```python
from bot import BasicBot

# Initialize bot
bot = BasicBot(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET', testnet=True)

# Place a market order
response = bot.place_market_order(symbol='BTCUSDT', side='BUY', quantity=0.001)
print(f"Order ID: {response['orderId']}")

# Place a limit order
response = bot.place_limit_order(
    symbol='BTCUSDT', 
    side='SELL', 
    quantity=0.001, 
    price=50000
)

# Place a stop-limit order
response = bot.place_stop_limit_order(
    symbol='BTCUSDT',
    side='SELL',
    quantity=0.001,
    price=49000,
    stop_price=50000
)

# Check account balance
balance = bot.get_account_balance()
print(f"Available balance: {balance['available_balance']} USDT")
```

## Logging

All API interactions are logged to:
- **Console**: Real-time output
- **File**: `trading_bot.log` (created automatically)

Log entries include:
- API requests with parameters
- API responses
- Errors and exceptions
- Connection status

## Error Handling

The bot includes comprehensive error handling for:
- Invalid API credentials
- Network connectivity issues
- Invalid order parameters
- Insufficient balance
- Binance API errors

All errors are logged with detailed information to help diagnose issues.

## Order Types Explained

### Market Order
Executes immediately at the current market price. Use when you want to enter/exit a position quickly.

### Limit Order
Places an order at a specific price. The order will only execute when the market reaches your specified price. Use for better price control.

### Stop-Limit Order
A combination of stop and limit orders. When the stop price is reached, a limit order is placed. Useful for:
- **Stop Loss**: Limit losses if price moves against you
- **Take Profit**: Lock in profits at a target price

## Security Best Practices

1. **Never commit API credentials** to version control
2. **Use environment variables** for API keys in production:
   ```bash
   export BINANCE_API_KEY="your_key"
   export BINANCE_API_SECRET="your_secret"
   ```
3. **Restrict API key permissions** to only what's needed
4. **Use testnet** for development and testing
5. **Monitor your API usage** regularly

## Troubleshooting

### Connection Issues
- Verify your API key and secret are correct
- Check your internet connection
- Ensure you're using the testnet URL: `https://testnet.binancefuture.com`

### Order Placement Errors
- Verify you have sufficient balance
- Check that the symbol is correct (e.g., BTCUSDT, not BTC/USDT)
- Ensure quantity and price meet minimum requirements
- Check the order logs for detailed error messages

### Common Error Messages
- `Invalid API-key`: Check your API credentials
- `Insufficient balance`: You don't have enough funds
- `Invalid symbol`: Symbol format is incorrect
- `MIN_NOTIONAL`: Order value is below minimum

## Project Structure

```
bot_tut/
├── bot.py              # Core trading bot class
├── cli.py              # Command-line interface
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── trading_bot.log    # Log file (created at runtime)
```

## API Reference

### BasicBot Class

#### Methods

- `place_market_order(symbol, side, quantity)` - Place a market order
- `place_limit_order(symbol, side, quantity, price)` - Place a limit order
- `place_stop_limit_order(symbol, side, quantity, price, stop_price)` - Place a stop-limit order
- `get_order_status(symbol, order_id)` - Get order status
- `cancel_order(symbol, order_id)` - Cancel an order
- `get_account_balance()` - Get account balance information
- `get_symbol_info(symbol)` - Get symbol trading information

## License

This project is for educational purposes only. Use at your own risk.

## Disclaimer

⚠️ **This is a testnet trading bot for educational purposes only.**
- Always test thoroughly on testnet before using on mainnet
- Trading cryptocurrencies involves risk
- The authors are not responsible for any financial losses
- Use this code at your own risk

## Support

For issues or questions:
1. Check the logs in `trading_bot.log`
2. Review the error messages in the console
3. Verify your API credentials and network connection
4. Consult the [Binance API documentation](https://binance-docs.github.io/apidocs/futures/en/)

