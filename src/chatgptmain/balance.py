import json
import requests
import datetime
import pytz
import threading
balancelist={}
threads=[]
def ckBalance(ymldata):
  for openwxuser in ymldata:
    key=ymldata[openwxuser]['Api_key']
    thread = threading.Thread(target=reBalance, args=(key,openwxuser,))
    threads.append(thread)
    thread.start()
  for thread in threads:
      thread.join()
  return balancelist
def reBalance(key,openwxuser):
    balancejson={}
    url = 'https://api.openai.com/dashboard/billing/credit_grants'
    headers = {'Authorization': 'Bearer ' + key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
            print(response.reason+response.text)
            balancejson={'created':"ERROR",'end':"ERROR",'balance':"ERROR"}
            balancelist[openwxuser]=balancejson
            return balancelist
    responsejson = json.loads(response.text)
    datalist=responsejson['grants']['data']
    effective_at=0;expires_at=0;grant_amount=0;used_amount=0
    for data in datalist:
        effective_at=int(data['effective_at']) 
        expires_at=int(data['expires_at']) 
        grant_amount=data['grant_amount']
        used_amount=data['used_amount']
    created_at = datetime.datetime.utcfromtimestamp(effective_at).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    end_at = datetime.datetime.utcfromtimestamp(expires_at).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    balance_at = round(grant_amount - used_amount,2)
    balancejson={'created':created_at,'end':end_at,'balance':balance_at}
    balancelist[openwxuser]=balancejson
    return balancelist
