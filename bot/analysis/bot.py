from connector.api_connector import ohlc_data
from common.common import *
from datetime import  timedelta,date

def check_money_flow(symbol):
    money_flow = []
    today = date.today()
    sixty_days_ago = today - timedelta(days=90)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today),resolution ='5')
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
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today),resolution ='D')
    if symbol_data is None:
        return False
    ma20_volume = calculate_ma(symbol_data['volume'], 20)
#     if(ma20_volume[-1] <= symbol_data['volume'].iloc[-1] ):
    return symbol_data['volume'].iloc[-1]/ma20_volume[-1]


def check_week(symbol):
    today = date.today()
    start_days = today - timedelta(days=300)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(start_days),end_date = str(today),resolution ='W')

    if symbol_data is None:
        return False
    ma20 = calculate_ma(symbol_data['close'], 20)
    if(ma20[-1] <= symbol_data['close'].iloc[-1] ):
        return True
    return False