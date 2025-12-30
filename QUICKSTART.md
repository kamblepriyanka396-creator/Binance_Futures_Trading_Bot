# Quick Start Guide

## Step 1: Get Binance Testnet API Credentials

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Sign up or log in
3. Navigate to **API Management** in your account settings
4. Create a new API key
5. **Save your API Key and Secret** - you'll need them to run the bot

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Run the Bot

### Option A: Interactive Mode (Easiest)

```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET --interactive
```

This will show you a menu where you can:
- Place orders
- Check your balance
- View order status
- Cancel orders

### Option B: Command Line

Check your balance first:
```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET --balance
```

Place a test market order:
```bash
python cli.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET \
  --order-type market --symbol BTCUSDT --side BUY --quantity 0.001
```

## Step 4: Check Logs

All API interactions are logged to `trading_bot.log`. Check this file if you encounter any issues.

## Common Symbols

- BTCUSDT - Bitcoin
- ETHUSDT - Ethereum
- BNBUSDT - Binance Coin

## Tips

- Start with small quantities (0.001 BTC, 0.01 ETH)
- Always test on testnet first
- Check your balance before placing orders
- Review the logs if something goes wrong

## Troubleshooting

**"Invalid API-key" error:**
- Double-check your API key and secret
- Make sure there are no extra spaces
- Verify the API key is enabled on testnet

**"Insufficient balance" error:**
- You need testnet funds. Get them from the testnet faucet
- Check your balance with `--balance` flag

**Connection errors:**
- Check your internet connection
- Verify you're using the correct testnet URL
- Check the logs for detailed error messages

