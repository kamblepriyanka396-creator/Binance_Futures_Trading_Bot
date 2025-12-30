# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



# See PyCharm help at https://www.jetbrains.com/help/pycharm/


from config import API_KEY, API_SECRET
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validator import validate_order

def main():
    client = BinanceClient(API_KEY, API_SECRET).client
    manager = OrderManager(client)

    symbol = input("Symbol (e.g. BTCUSDT): ").upper()
    side = input("Side (BUY/SELL): ").upper()
    order_type = input("Order Type (MARKET/LIMIT): ").upper()
    quantity = float(input("Quantity: "))

    price = None
    if order_type == "LIMIT":
        price = float(input("Price: "))

    validate_order(symbol, side, order_type, quantity, price)

    if order_type == "MARKET":
        result = manager.place_market_order(symbol, side, quantity)
    else:
        result = manager.place_limit_order(symbol, side, quantity, price)

    print("Order placed successfully!")
    print(result)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


