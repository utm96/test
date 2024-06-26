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

def check_volume_day_and_can_buy(symbol):
    today = date.today()
    sixty_days_ago = today - timedelta(days=60)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today + timedelta(days=1)),resolution ='D')
    if symbol_data is None:
        return False
    ma20_volume = calculate_ma(symbol_data['volume'], 20)
    ema9 = calculate_ema(symbol_data['close'], 9)
    ema5 = calculate_ema(symbol_data['close'], 5)
    high_current_price = symbol_data['high'].iloc[-1]
#     if(ma20_volume[-1] <= symbol_data['volume'].iloc[-1] ):
    return symbol_data['volume'].iloc[-1] < ma20_volume[-1] and (high_current_price > ema5[-1] or high_current_price > ema9[-1])

def squeez_on(symbol):
    today = date.today()
    sixty_days_ago = today - timedelta(days=60)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today + timedelta(days=1)),resolution ='D')
    if symbol_data is None:
        return False
    symbol_data['20sma'] = symbol_data['close'].rolling(window=20).mean()
    symbol_data['stddev'] = symbol_data['close'].rolling(window=20).std()
    symbol_data['lower_band'] = symbol_data['20sma'] - (2 * symbol_data['stddev'])
    symbol_data['upper_band'] = symbol_data['20sma'] + (2 * symbol_data['stddev'])

    symbol_data['TR'] = abs(symbol_data['high'] - symbol_data['low'])
    symbol_data['ATR'] = symbol_data['TR'].rolling(window=20).mean()

    symbol_data['lower_keltner'] = symbol_data['20sma'] - (symbol_data['ATR'] * 1.5)
    symbol_data['upper_keltner'] = symbol_data['20sma'] + (symbol_data['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    symbol_data['squeeze_on'] = symbol_data.apply(in_squeeze, axis=1)
    count = 0
    for i in range(1,10):
        if symbol_data.iloc[-i]['squeeze_on']:
            count += 1 

    return count 

        
def check_week(symbol):
    today = date.today()
    start_days = today - timedelta(days=600)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(start_days),end_date = str(today+ timedelta(days=1)),resolution ='W')

    if symbol_data is None:
        return False
    ma50 = calculate_ma(symbol_data['close'], 50)
    ma9 = calculate_ma(symbol_data['close'], 9)
    ma20 = calculate_ma(symbol_data['close'], 20)

    if(ma20[-1] <= symbol_data['close'].iloc[-1] ):
        return True
    if(ma50[-1] <= symbol_data['close'].iloc[-1] ):
        return True
    if(ma9[-1] <= symbol_data['close'].iloc[-1] ):
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

# def can_buy(symbol):
#     today = date.today()
#     four_years_ago = today - timedelta(days=465)
#     symbol_data = ohlc_data(symbol = symbol,start_date=str(four_years_ago),end_date = str(today+ timedelta(days=1)),resolution ='D')
#     if symbol_data is None:
#         return False
#     current_price = symbol_data['close'].iloc[-1]
#     ma200 = calculate_ma(symbol_data['close'], 200)
#     ma100 = calculate_ma(symbol_data['close'], 100)
#     ma50 = calculate_ma(symbol_data['close'], 50)
#     ma20 = calculate_ma(symbol_data['close'], 20)

# #     if(ma20_volume[-1] <= symbol_data['volume'].iloc[-1] ):
#     return ma200[-1] < ma100[-1] < ma50[-1] < ma20[-1] and current_price > ma50[-1]


def trading_symbol(symbol):
    today = date.today()
    four_years_ago = today - timedelta(days=60)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(four_years_ago),end_date = str(today+ timedelta(days=1)),resolution ='D')
    if symbol_data is None:
        return False
    return wt_lb(symbol_data)

#     if(ma20_volume[-1] <= symbol_data['volume'].iloc[-1] ):
    # return ma200[-1] < ma100[-1] < ma50[-1] < ma20[-1] and current_price > ma50[-1]

def rsi(symbol = 'VHC',period=14 , symbol_data = None):
    if symbol_data is None:
        today = date.today()
        sixty_days_ago = today - timedelta(days=60)
        symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today + timedelta(days=1)),resolution ='D')
    change = symbol_data['close'].diff()

    # Separate gains and losses
    gain = change.where(change > 0, 0.0)
    loss = change.where(change < 0, 0.0).abs()

    # Calculate the Exponential Moving Average (EMA) for gains and losses
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    # Calculate the Relative Strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the Relative Strength Index (RSI)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def check_poc(symbol):
    # money_flow = []
    today = date.today()
    sixty_days_ago = today - timedelta(days=365)
    symbol_data = ohlc_data(symbol = symbol,start_date=str(sixty_days_ago),end_date = str(today+ timedelta(days=1)),resolution ='D')
    if symbol_data is None:
        return False
    num_bars = 200
# Define the price levels
    price_levels = pd.cut(symbol_data['close'], bins=num_bars, labels=False)
    vol_profile = symbol_data.groupby(price_levels)['volume'].sum()
    poc_level = vol_profile.idxmax()
    poc_price = symbol_data['close'].min() + (symbol_data['close'].max() - symbol_data['close'].min()) * poc_level / num_bars
    current_price = symbol_data['close'].iloc[-1]
    if(current_price < poc_price * 1.04 ):
        return True
    rsi_values = rsi(symbol = symbol, symbol_data = symbol_data)
    ema200 = calculate_ema(symbol_data['close'], 200)
    current_price = symbol_data['close'].iloc[-1]
    if(current_price > ema200[-1] and rsi_values.iloc[-1] < 45):
        return True
    return False
#     for i in range(-1,-value_range,-1):
#         record = symbol_data.iloc[i]
# #         print(record)
#         if(check_candle_buy(record) and record['volume'] > 3 * vol_ma[i] and record['volume'] * record['low'] > 1000000000* 3):
#             money_flow.append(record)
#     return money_flow
import math

def floor_to_step(num, step=0.05):
    result = math.floor(num / step) * step
    result = round(result, 2)
    return result

def count_occurrences(data, step=1):
    occurrences = {}
    for value in data:
        if value in occurrences:
            occurrences[value] += step
        else:
            occurrences[value] = step
    return occurrences

# Example usage:
def calcul_command_price(init_vol, init_price, number_loop, step, step_vol = 1):
    average_price  = init_price
    current_vol = init_vol
    values = []
    for i in range(number_loop):
        buy_price = 0.95 * average_price
        current_vol += 1
        average_price = (current_vol*average_price + buy_price*step_vol)/(current_vol + step_vol)
        values.append(floor_to_step(buy_price,step))
    occurrences = count_occurrences(values,step_vol)
    print(occurrences)
# def average_price(price_current, buy_price, current_vol):
#     (current_vol*price_current + buy_price)/(current_vol + 1)

