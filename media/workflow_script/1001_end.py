# encoding: utf-8
import requests
import simplejson

mcenter_ip = "10.254.50.54"
mcenter_port = "30042"
username = 'zabbix'
password = 'cernet@123'
url = 'http://%s:%s/cmdb/network-card/' % (mcenter_ip, mcenter_port)
try:
    get_token = requests.post(
        'http://%s:%s/api-token-auth/' % (mcenter_ip, mcenter_port),
        data={"username": username, "password": password},
    ).json()
except:
    print("Can not connect url:http://%s:%s/api-token-auth/" % (mcenter_ip, mcenter_port))

try:
    token = get_token['token']
except:
    print(get_token)
headers = {
    'Authorization': 'JWT ' + token,
    'Content-Type' : 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"participant": '','state_name':'结束', "state_id": 10042}), headers=headers)
requests.patch('http://%s:%s/work/changeticketstate/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 10042}), headers=headers).json()
