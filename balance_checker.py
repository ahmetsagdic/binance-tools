# ------------------------------------------------------------------------------
# a simple script to check balances of my binance account.
#
# @Author: Ahmet Sagdic
# @Date: 12/04/2021
# ------------------------------------------------------------------------------
import time, hmac, urllib.parse, hashlib, requests,json

# current binance url is test url. feel free to change it to first url
# if you want to use it on your binance account.
#BINANCE_URL='https://api.binance.com'
BINANCE_URL='https://testnet.binance.vision'
f=open('test_key.json','r')
dump=json.load(f)
API_KEY=dump['API_KEY']
SECRET_KEY=dump['SECRET_KEY']
f.close()
# REST API endpoints of binance
ACCOUNT_URL='/api/v3/account'
TICKER_PRICE='/api/v3/ticker/price'

# this function returns response from the request that sent to binance.
def get_account():
    timestamp=int(time.time()*1000)
    headers={
        'X-MBX-APIKEY': API_KEY
    }
    params={
        'recvWindow': 60000,
        'timestamp': timestamp   
    }
    params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), urllib.parse.urlencode(params).encode('utf-8'), hashlib.sha256).hexdigest()
    url=BINANCE_URL+ACCOUNT_URL
    response=requests.get(url,headers=headers,params=params)
    if(response.status_code!=200):
        print("request failed with code",response.status_code)
        return None
    return response

# extracts balances that are not zero.
def get_balances(response):
    if(response==None):
        return None
    balances_raw=response.json()['balances']
    balances={}
    for i in balances_raw:
        if(float(i['free'])!=0):
            balances[i['asset']]=float(i['free'])
        if(float(i['locked'])!=0):
            if(balances.get(i['asset'])==None):
                balances[i['asset']]=float(i['locked'])
            else:
                balances[i['asset']]=balances[i['asset']]+float(i['locked'])
    return balances

# gets price of given symbol based on USDT from price ticker
# TODO: if not in usdt market try busd
def get_price(symbol):
    price_url=BINANCE_URL+TICKER_PRICE+"?symbol="+symbol.upper()+'USDT'
    response=requests.get(price_url)
    return float(response.json()['price'])

# calculates total value of balances based on USDT, special rule= 1USDT = 1BUSD
def calculate_wallet_value(balances):
    if(balances==None):
        return None
    wallet_value=0
    for i in balances:
        if(i!='USDT' and i!='BUSD'):
            wallet_value=wallet_value+float(balances[i])*get_price(i)
        else:
            wallet_value=wallet_value+float(balances[i])
    return wallet_value

def get_net_value():
    return calculate_wallet_value(get_balances(get_account()))

print("current total wallet value=",get_net_value(),"usdt")

