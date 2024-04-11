import pandas as pd
import pandas_ta as ta


def check_candle_buy(record):
#     print(record)
    floor_candle = min (record['close'],record['open'] )
    ceil_candle = max(record['close'],record['high'] )
    tail_candle = floor_candle - record['low']
    upper_tail_candle = record['high'] - ceil_candle
    candle_length = record['high'] - record['low']
    if(candle_length != 0 and tail_candle / candle_length >= 0.5):
#         print("ok")
        return True
    if(tail_candle == 0 and upper_tail_candle == 0 and record['close'] >= record['open']):
#         print("ok")
        return True
    return False


def calculate_ma(data, n):
    ma = pd.Series(data).rolling(n).mean()
    return ma.to_numpy()

def calculate_ema(data, n):
    ma = ta.ema(data, length=n)
    return ma.to_numpy()
def wt_lb(data):
    n1 =10
    n2 = 21
    ap = (data['high'] + data['low'] + data['close'])/3 
    esa = calculate_ema(ap, n1)
    d = calculate_ema(abs(ap - esa), n1)
    ci = (ap - esa) / (0.015 * d)
    tci = calculate_ema(ci, n2)
    wt1 = tci
    wt2 = calculate_ma(wt1,4)
    wt = wt1 - wt2
    return wt2[-1] < 0 and wt1[-1] < 0 and wt[-1] >= -6




