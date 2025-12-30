"""
Command-line interface for the Trading Bot
"""

import argparse
import sys
from bot import BasicBot
from typing import Optional


def validate_side(side: str) -> str:
    """Validate order side"""
    side_upper = side.upper()
    if side_upper not in ['BUY', 'SELL']:
        raise ValueError(f"Side must be 'BUY' or 'SELL', got '{side}'")
    return side_upper


def validate_order_type(order_type: str) -> str:
    """Validate order type"""
    order_type_upper = order_type.upper()
    valid_types = ['MARKET', 'LIMIT', 'STOP-LIMIT', 'STOP_LIMIT']
    if order_type_upper not in valid_types:
        raise ValueError(
            f"Order type must be one of {valid_types}, got '{order_type}'"
        )
    return order_type_upper.replace('-', '_').upper()


def validate_positive_float(value: str, name: str) -> float:
    """Validate and convert to positive float"""
    try:
        val = float(value)
        if val <= 0:
            raise ValueError(f"{name} must be positive, got {val}")
        return val
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"{name} must be a valid number, got '{value}'")
        raise


def print_order_details(response: dict):
    """Print formatted order details"""
    print("\n" + "="*60)
    print("ORDER DETAILS")
    print("="*60)
    print(f"Order ID:        {response.get('orderId', 'N/A')}")
    print(f"Symbol:          {response.get('symbol', 'N/A')}")
    print(f"Side:            {response.get('side', 'N/A')}")
    print(f"Type:            {response.get('type', 'N/A')}")
    print(f"Quantity:        {response.get('origQty', 'N/A')}")
    print(f"Price:           {response.get('price', 'N/A')}")
    print(f"Status:          {response.get('status', 'N/A')}")
    print(f"Time:            {response.get('updateTime', 'N/A')}")
    if 'stopPrice' in response:
        print(f"Stop Price:      {response.get('stopPrice', 'N/A')}")
    print("="*60 + "\n")


def print_account_info(bot: BasicBot):
    """Print account balance information"""
    try:
        balance_info = bot.get_account_balance()
        print("\n" + "="*60)
        print("ACCOUNT BALANCE")
        print("="*60)
        print(f"Total Wallet Balance:  {balance_info.get('total_wallet_balance', 'N/A')} USDT")
        print(f"Available Balance:    {balance_info.get('available_balance', 'N/A')} USDT")
        print(f"Unrealized PnL:        {balance_info.get('total_unrealized_pnl', 'N/A')} USDT")
        print("="*60 + "\n")
    except Exception as e:
        print(f"Error getting account balance: {str(e)}")


def place_order_interactive(bot: BasicBot):
    """Interactive order placement"""
    print("\n" + "="*60)
    print("PLACE ORDER")
    print("="*60)
    
    try:
        # Get symbol
        symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
        if not symbol:
            print("Error: Symbol cannot be empty")
            return
        
        # Get order type
        print("\nOrder types:")
        print("1. MARKET")
        print("2. LIMIT")
        print("3. STOP-LIMIT")
        order_type_choice = input("Select order type (1-3): ").strip()
        
        order_type_map = {'1': 'MARKET', '2': 'LIMIT', '3': 'STOP-LIMIT'}
        order_type = order_type_map.get(order_type_choice)
        if not order_type:
            print("Error: Invalid order type selection")
            return
        
        # Get side
        side = input("Enter side (BUY/SELL): ").strip()
        try:
            side = validate_side(side)
        except ValueError as e:
            print(f"Error: {str(e)}")
            return
        
        # Get quantity
        quantity_str = input("Enter quantity: ").strip()
        try:
            quantity = validate_positive_float(quantity_str, "Quantity")
        except ValueError as e:
            print(f"Error: {str(e)}")
            return
        
        # Place order based on type
        if order_type == 'MARKET':
            response = bot.place_market_order(symbol, side, quantity)
        elif order_type == 'LIMIT':
            price_str = input("Enter limit price: ").strip()
            try:
                price = validate_positive_float(price_str, "Price")
            except ValueError as e:
                print(f"Error: {str(e)}")
                return
            response = bot.place_limit_order(symbol, side, quantity, price)
        elif order_type == 'STOP-LIMIT':
            price_str = input("Enter limit price: ").strip()
            stop_price_str = input("Enter stop price: ").strip()
            try:
                price = validate_positive_float(price_str, "Price")
                stop_price = validate_positive_float(stop_price_str, "Stop price")
            except ValueError as e:
                print(f"Error: {str(e)}")
                return
            response = bot.place_stop_limit_order(
                symbol, side, quantity, price, stop_price
            )
        
        print_order_details(response)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\nError placing order: {str(e)}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Binance Futures Testnet Trading Bot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET
  
  # Place market order
  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET \\
    --order-type market --symbol BTCUSDT --side BUY --quantity 0.001
  
  # Place limit order
  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET \\
    --order-type limit --symbol BTCUSDT --side SELL --quantity 0.001 --price 50000
  
  # Place stop-limit order
  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET \\
    --order-type stop-limit --symbol BTCUSDT --side SELL \\
    --quantity 0.001 --price 49000 --stop-price 50000
  
  # Check account balance
  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET --balance
  
  # Check order status
  python cli.py --api-key YOUR_KEY --api-secret YOUR_SECRET \\
    --order-status --symbol BTCUSDT --order-id 123456
        """
    )
    
    parser.add_argument(
        '--api-key',
        required=True,
        help='Binance API key'
    )
    parser.add_argument(
        '--api-secret',
        required=True,
        help='Binance API secret'
    )
    parser.add_argument(
        '--testnet',
        action='store_true',
        default=True,
        help='Use testnet (default: True)'
    )
    parser.add_argument(
        '--mainnet',
        action='store_true',
        help='Use mainnet instead of testnet'
    )
    
    # Order placement arguments
    parser.add_argument(
        '--order-type',
        choices=['market', 'limit', 'stop-limit'],
        help='Order type'
    )
    parser.add_argument(
        '--symbol',
        help='Trading pair symbol (e.g., BTCUSDT)'
    )
    parser.add_argument(
        '--side',
        choices=['BUY', 'SELL'],
        help='Order side'
    )
    parser.add_argument(
        '--quantity',
        type=float,
        help='Order quantity'
    )
    parser.add_argument(
        '--price',
        type=float,
        help='Limit price (required for limit and stop-limit orders)'
    )
    parser.add_argument(
        '--stop-price',
        type=float,
        help='Stop price (required for stop-limit orders)'
    )
    
    # Other operations
    parser.add_argument(
        '--balance',
        action='store_true',
        help='Display account balance'
    )
    parser.add_argument(
        '--order-status',
        action='store_true',
        help='Check order status'
    )
    parser.add_argument(
        '--order-id',
        type=int,
        help='Order ID (required for --order-status)'
    )
    parser.add_argument(
        '--cancel-order',
        action='store_true',
        help='Cancel an order'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    # Determine testnet/mainnet
    use_testnet = args.testnet and not args.mainnet
    
    try:
        # Initialize bot
        bot = BasicBot(args.api_key, args.api_secret, testnet=use_testnet)
        
        # Interactive mode
        if args.interactive:
            while True:
                print("\n" + "="*60)
                print("TRADING BOT - INTERACTIVE MODE")
                print("="*60)
                print("1. Place order")
                print("2. Check account balance")
                print("3. Check order status")
                print("4. Cancel order")
                print("5. Exit")
                
                choice = input("\nSelect option (1-5): ").strip()
                
                if choice == '1':
                    place_order_interactive(bot)
                elif choice == '2':
                    print_account_info(bot)
                elif choice == '3':
                    symbol = input("Enter symbol: ").strip().upper()
                    order_id = int(input("Enter order ID: ").strip())
                    try:
                        status = bot.get_order_status(symbol, order_id)
                        print_order_details(status)
                    except Exception as e:
                        print(f"Error: {str(e)}")
                elif choice == '4':
                    symbol = input("Enter symbol: ").strip().upper()
                    order_id = int(input("Enter order ID: ").strip())
                    try:
                        bot.cancel_order(symbol, order_id)
                        print("Order cancelled successfully")
                    except Exception as e:
                        print(f"Error: {str(e)}")
                elif choice == '5':
                    print("Exiting...")
                    break
                else:
                    print("Invalid option")
        
        # Check balance
        elif args.balance:
            print_account_info(bot)
        
        # Check order status
        elif args.order_status:
            if not args.symbol or not args.order_id:
                print("Error: --symbol and --order-id are required for --order-status")
                sys.exit(1)
            try:
                status = bot.get_order_status(args.symbol, args.order_id)
                print_order_details(status)
            except Exception as e:
                print(f"Error: {str(e)}")
                sys.exit(1)
        
        # Cancel order
        elif args.cancel_order:
            if not args.symbol or not args.order_id:
                print("Error: --symbol and --order-id are required for --cancel-order")
                sys.exit(1)
            try:
                bot.cancel_order(args.symbol, args.order_id)
                print("Order cancelled successfully")
            except Exception as e:
                print(f"Error: {str(e)}")
                sys.exit(1)
        
        # Place order
        elif args.order_type:
            if not args.symbol or not args.side or not args.quantity:
                print("Error: --symbol, --side, and --quantity are required for placing orders")
                sys.exit(1)
            
            try:
                if args.order_type == 'market':
                    response = bot.place_market_order(
                        args.symbol, args.side, args.quantity
                    )
                elif args.order_type == 'limit':
                    if not args.price:
                        print("Error: --price is required for limit orders")
                        sys.exit(1)
                    response = bot.place_limit_order(
                        args.symbol, args.side, args.quantity, args.price
                    )
                elif args.order_type == 'stop-limit':
                    if not args.price or not args.stop_price:
                        print("Error: --price and --stop-price are required for stop-limit orders")
                        sys.exit(1)
                    response = bot.place_stop_limit_order(
                        args.symbol, args.side, args.quantity, 
                        args.price, args.stop_price
                    )
                
                print_order_details(response)
                
            except Exception as e:
                print(f"Error placing order: {str(e)}")
                sys.exit(1)
        
        # No operation specified
        else:
            print("No operation specified. Use --interactive, --balance, --order-status, or --order-type")
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

