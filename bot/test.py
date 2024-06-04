from connector.telegram_connector import send_message_tele
from analysis.bot import *
from connector.api_connector import get_token,get_list_stock,get_asset
import json
from common.helper import read_config
from collections import defaultdict 


check_poc('DBC')

