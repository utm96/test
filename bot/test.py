from connector.telegram_connector import send_message_tele
from analysis.bot import *
from connector.api_connector import get_token,get_list_stock,get_asset
import json
from common.helper import read_config
from collections import defaultdict 


# calcul_command_price(init_price=31.25,init_vol=25,number_loop=14, step = 0.05, step_vol = 1pp)


# rsi = check_poc('MSB')
# print(rsi)

values = [1,2,3]
def test_func(nums):
    nums.append(4)
test_func(values)
print(values)
