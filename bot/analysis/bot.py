from connector.api_connector import ohlc_data
from common.common import *
from datetime import  timedelta,date

def check_money_flow(symbol):
    money_flow = []
    today = date.today()
    sixty_days_ago = today - timedelta(days=90)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today+ timedelta(days=1)),resolution ='5')
    if symbol_data is None:
        return False
    vol_ma = calculate_ma(symbol_data['volume'], 500)
    value_range = min(len(symbol_data.index), 2000)
    for i in range(-1,-value_range,-1):
        record = symbol_data.iloc[i]
#         print(record)
        if(check_candle_buy(record) and record['volume'] > 3 * vol_ma[i] and record['volume'] * record['low'] > 1000000000* 3):
            money_flow.append(record)
    return money_flow

def check_volume_day(symbol):
    today = date.today()
    sixty_days_ago = today - timedelta(days=60)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today + timedelta(days=1)),resolution ='D')
    if symbol_data is None:
        return False
    ma20_volume = calculate_ma(symbol_data['volume'], 20)
#     if(ma20_volume[-1] <= symbol_data['volume'].iloc[-1] ):
    return symbol_data['volume'].iloc[-1]/ma20_volume[-1]


def check_week(symbol):
    today = date.today()
    start_days = today - timedelta(days=300)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(start_days),end_date = str(today+ timedelta(days=1)),resolution ='W')

    if symbol_data is None:
        return False
    ma20 = calculate_ma(symbol_data['close'], 20)
    if(ma20[-1] <= symbol_data['close'].iloc[-1] ):
        return True
    return False

def check_sell(symbol):
    today = date.today()
    sixty_days_ago = today - timedelta(days=60)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today+ timedelta(days=1)),resolution ='D')
    if symbol_data is None:
        return False
    ma20_volume = calculate_ma(symbol_data['volume'], 20)
    ema15_price = calculate_ema(symbol_data['close'], 15)
    # print(ema15_price)
    # print(symbol_data['close'].iloc[-1])
    # print(symbol_data['volume'].iloc[-1])
    # print(ma20_volume[-1])
    # print(symbol_data['volume'])

#     if(ma20_volume[-1] <= symbol_data['volume'].iloc[-1] ):
    return symbol_data['volume'].iloc[-1] > ma20_volume[-1] and symbol_data['close'].iloc[-1]<ema15_price[-1]


def check_strong_stock(symbol):
    today = date.today()
    four_years_ago = today - timedelta(days=465)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(four_years_ago),end_date = str(today+ timedelta(days=1)),resolution ='D')
    if symbol_data is None:
        return False
    current_price = symbol_data['close'].iloc[-1]
    ma200 = calculate_ma(symbol_data['close'], 200)
    ma100 = calculate_ma(symbol_data['close'], 100)
    ma50 = calculate_ma(symbol_data['close'], 50)
    ma20 = calculate_ma(symbol_data['close'], 20)

#     if(ma20_volume[-1] <= symbol_data['volume'].iloc[-1] ):
    return ma200[-1] < ma100[-1] < ma50[-1] < ma20[-1] and current_price > ma50[-1]