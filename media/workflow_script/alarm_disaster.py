# encoding: utf-8
import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService

mcenter_ip = "10.254.50.54"
mcenter_port = "30042"
username = 'zabbix'
password = 'cernet@123'
user_url =  'http://%s:%s/user/user-profile/?search=' % (mcenter_ip, mcenter_port)
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
    'Content-Type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}
duty_manager_str = ''
reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
for i in reslist:
    if i['field_key'] == 'duty_manager':
        duty_manager_str = str(i['field_value'])
duty_manager_list = []
for duty_manager in duty_manager_str.split(','):
    user_mc = requests.request(method="GET", url=user_url + duty_manager, headers=headers).json()
    for user in user_mc['results']:
        if duty_manager == user['username']:
            duty_manager_list.append(user['name'])
            break
duty_manager = ','.join(duty_manager_list)
requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"participant": duty_manager,'state_name':'值班经理处理', "state_id": 210}), headers=headers)

