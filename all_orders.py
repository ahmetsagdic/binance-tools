# ------------------------------------------------------------------------------
# a simple script to check all orders of my binance account.
#
# @Author: Ahmet Sagdic
# @Date: 17/04/2021
# ------------------------------------------------------------------------------
import time, hmac, urllib.parse, hashlib, requests,json
BINANCE_URL='https://testnet.binance.vision'
f=open('test_key.json','r')
#BINANCE_URL='https://api.binance.com'
#f=open('key.json','r')
dump=json.load(f)
API_KEY=dump['API_KEY']
SECRET_KEY=dump['SECRET_KEY']
f.close()

# REST API endpoints of binance
ALL_ORDERS_URL='/api/v3/allOrders'

all_orders_last_response=None
all_orders_last_fetch_timestamp=0
# this function returns response from the request that sent to binance.
# weight 40
def get_all_orders(symbol):
    global all_orders_last_fetch_timestamp,all_orders_last_response
    timestamp=int(time.time()*1000)
    diff=(timestamp-all_orders_last_fetch_timestamp)/60000
    if(diff<1):
        print("already requested in the same minute...")
        return all_orders_last_response
    headers={
        'X-MBX-APIKEY': API_KEY
    }
    params={
        'recvWindow': 60000,
        'timestamp': timestamp,
        'symbol': symbol
    }
    params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), urllib.parse.urlencode(params).encode('utf-8'), hashlib.sha256).hexdigest()
    url=BINANCE_URL+ALL_ORDERS_URL
    response=requests.get(url,headers=headers,params=params)
    if(response.status_code!=200):
        print("request failed with code",response.status_code)
        print(response)
        return None
    all_orders_last_fetch_timestamp=timestamp
    all_orders_last_response=response
    return response

#TEST
resp=get_all_orders('BTCUSDT')
print(resp.headers)