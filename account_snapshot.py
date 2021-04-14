# ------------------------------------------------------------------------------
# a simple script to check balances of my binance account.
#
# @Author: Ahmet Sagdic
# @Date: 14/04/2021
# ------------------------------------------------------------------------------
import time, hmac, urllib.parse, hashlib, requests,json
#BINANCE_URL='https://testnet.binance.vision'
BINANCE_URL='https://api.binance.com'
#f=open('test_key.json','r')
f=open('key.json','r')
dump=json.load(f)
API_KEY=dump['API_KEY']
SECRET_KEY=dump['SECRET_KEY']
f.close()

# REST API endpoints of binance
SNAPSHOT_URL='/sapi/v1/accountSnapshot'
# this function returns response from the request that sent to binance.
def get_account_snapshot():
    timestamp=int(time.time()*1000)
    headers={
        'X-MBX-APIKEY': API_KEY
    }
    params={
        'recvWindow': 60000,
        'timestamp': timestamp,
        'type':'SPOT'
    }
    params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), urllib.parse.urlencode(params).encode('utf-8'), hashlib.sha256).hexdigest()
    url=BINANCE_URL+SNAPSHOT_URL
    response=requests.get(url,headers=headers,params=params)
    if(response.status_code!=200):
        print("request failed with code",response.status_code)
        return None
    return response

# extracts symbols that are not zero from the daily snapshot of account..
def get_snapshotVos(response):
    if(response==None):
        return None
    balances_raw=response.json()['snapshotVos'][0]['data']['balances']
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

resp=get_account_snapshot()
print(get_snapshotVos(resp))