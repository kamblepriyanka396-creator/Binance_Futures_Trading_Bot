"""
Simplified Trading Bot for Binance Futures Testnet
Supports Market, Limit, and Stop-Limit orders
"""

import logging
import sys
from typing import Optional, Dict, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from datetime import datetime


class BasicBot:
    """Trading bot for Binance Futures Testnet"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the trading bot
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Configure logging
        self._setup_logging()
        
        # Initialize Binance client
        try:
            if testnet:
                # For testnet, we need to use the testnet base URL
                # Create client with testnet flag
                self.client = Client(
                    api_key=api_key,
                    api_secret=api_secret,
                    testnet=True
                )
                # Override base URL for Futures Testnet
                # The python-binance library uses FUTURES_URL for futures endpoints
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
                # Also set the base URL if needed
                if hasattr(self.client, 'FUTURES_BASE_URL'):
                    self.client.FUTURES_BASE_URL = 'https://testnet.binancefuture.com'
                self.logger.info("Initialized Binance Futures Testnet client")
                self.logger.info(f"Using Futures URL: {self.client.FUTURES_URL}")
            else:
                self.client = Client(api_key=api_key, api_secret=api_secret)
                self.logger.info("Initialized Binance client (mainnet)")
                
            # Test connection
            self._test_connection()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize client: {str(e)}")
            raise
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_bot.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _test_connection(self):
        """Test connection to Binance API"""
        try:
            if self.testnet:
                # Test futures connection
                account_info = self.client.futures_account()
                self.logger.info("Successfully connected to Binance Futures Testnet")
                self.logger.info(f"Account balance: {account_info.get('totalWalletBalance', 'N/A')} USDT")
            else:
                account_info = self.client.get_account()
                self.logger.info("Successfully connected to Binance")
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            raise
    
    def _log_request(self, method: str, params: Dict[str, Any]):
        """Log API request details"""
        self.logger.info(f"API Request - Method: {method}, Params: {params}")
    
    def _log_response(self, response: Dict[str, Any]):
        """Log API response details"""
        self.logger.info(f"API Response: {response}")
    
    def _log_error(self, error: Exception, context: str = ""):
        """Log error details"""
        error_msg = f"Error {context}: {type(error).__name__} - {str(error)}"
        self.logger.error(error_msg)
    
    def place_market_order(
        self, 
        symbol: str, 
        side: str, 
        quantity: float
    ) -> Dict[str, Any]:
        """
        Place a market order
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            
        Returns:
            Order response dictionary
        """
        try:
            self.logger.info(f"Placing market order: {side} {quantity} {symbol}")
            
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'MARKET',
                'quantity': quantity
            }
            
            self._log_request('futures_create_order', params)
            
            response = self.client.futures_create_order(**params)
            self._log_response(response)
            
            self.logger.info(f"Market order placed successfully. Order ID: {response.get('orderId')}")
            return response
            
        except BinanceAPIException as e:
            self._log_error(e, f"placing market order for {symbol}")
            raise
        except BinanceRequestException as e:
            self._log_error(e, f"placing market order for {symbol}")
            raise
        except Exception as e:
            self._log_error(e, f"placing market order for {symbol}")
            raise
    
    def place_limit_order(
        self, 
        symbol: str, 
        side: str, 
        quantity: float, 
        price: float,
        time_in_force: str = 'GTC'
    ) -> Dict[str, Any]:
        """
        Place a limit order
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Limit price
            time_in_force: Time in force ('GTC', 'IOC', 'FOK')
            
        Returns:
            Order response dictionary
        """
        try:
            self.logger.info(f"Placing limit order: {side} {quantity} {symbol} @ {price}")
            
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'LIMIT',
                'quantity': quantity,
                'price': price,
                'timeInForce': time_in_force
            }
            
            self._log_request('futures_create_order', params)
            
            response = self.client.futures_create_order(**params)
            self._log_response(response)
            
            self.logger.info(f"Limit order placed successfully. Order ID: {response.get('orderId')}")
            return response
            
        except BinanceAPIException as e:
            self._log_error(e, f"placing limit order for {symbol}")
            raise
        except BinanceRequestException as e:
            self._log_error(e, f"placing limit order for {symbol}")
            raise
        except Exception as e:
            self._log_error(e, f"placing limit order for {symbol}")
            raise
    
    def place_stop_limit_order(
        self, 
        symbol: str, 
        side: str, 
        quantity: float, 
        price: float, 
        stop_price: float,
        time_in_force: str = 'GTC'
    ) -> Dict[str, Any]:
        """
        Place a stop-limit order (bonus feature)
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price (trigger price)
            time_in_force: Time in force ('GTC', 'IOC', 'FOK')
            
        Returns:
            Order response dictionary
        """
        try:
            self.logger.info(
                f"Placing stop-limit order: {side} {quantity} {symbol} @ {price} "
                f"(stop: {stop_price})"
            )
            
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'STOP',
                'quantity': quantity,
                'price': price,
                'stopPrice': stop_price,
                'timeInForce': time_in_force
            }
            
            self._log_request('futures_create_order', params)
            
            response = self.client.futures_create_order(**params)
            self._log_response(response)
            
            self.logger.info(f"Stop-limit order placed successfully. Order ID: {response.get('orderId')}")
            return response
            
        except BinanceAPIException as e:
            self._log_error(e, f"placing stop-limit order for {symbol}")
            raise
        except BinanceRequestException as e:
            self._log_error(e, f"placing stop-limit order for {symbol}")
            raise
        except Exception as e:
            self._log_error(e, f"placing stop-limit order for {symbol}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order status
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order status dictionary
        """
        try:
            response = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order {order_id} status: {response.get('status')}")
            return response
        except Exception as e:
            self._log_error(e, f"getting order status for {order_id}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Cancellation response dictionary
        """
        try:
            self.logger.info(f"Cancelling order {order_id} for {symbol}")
            response = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self._log_response(response)
            self.logger.info(f"Order {order_id} cancelled successfully")
            return response
        except Exception as e:
            self._log_error(e, f"cancelling order {order_id}")
            raise
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance
        
        Returns:
            Account balance information
        """
        try:
            account_info = self.client.futures_account()
            return {
                'total_wallet_balance': account_info.get('totalWalletBalance'),
                'available_balance': account_info.get('availableBalance'),
                'total_unrealized_pnl': account_info.get('totalUnrealizedProfit'),
                'assets': account_info.get('assets', [])
            }
        except Exception as e:
            self._log_error(e, "getting account balance")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get symbol trading information
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Symbol information dictionary
        """
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    return s
            raise ValueError(f"Symbol {symbol} not found")
        except Exception as e:
            self._log_error(e, f"getting symbol info for {symbol}")
            raise

