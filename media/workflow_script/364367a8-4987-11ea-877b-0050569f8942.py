# encoding: utf-8
import sys
import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService


mcenter_ip = "10.254.50.54"
mcenter_port = "32045"
username = 'root'
password = '123456a?'

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}
reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    data[i['field_key']] = str(i['field_value'])

data['change_data'] = eval(str(data['change_data']).replace('false', 'False').replace('true', "True").replace('null', 'None'))
headers['Content-Type'] = 'application/json'
url = 'http://%s:%s/' % (mcenter_ip, mcenter_port)
if data['data_type'] == '1':
    url = url + 'site/ip/'
elif data['data_type'] == '2':
    url = url + 'site/ip-address/'
elif data['data_type'] == '3':
    url = url + 'site/web-site/'

if data['handle_type'] == '1':
    requests.post(url=url,data=simplejson.dumps(data['change_data']), headers=headers)
else:
    url = url + str(data['change_data']['id']) + '/'
    old_data = requests.get(url=url, headers=headers).json()
    TicketBaseService.update_ticket_custom_field(ticket_id, {"old_data": simplejson.dumps(old_data)})
    requests.patch(url=url,data=simplejson.dumps(data['change_data']), headers=headers)

requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束'}), headers=headers)
a = requests.patch('http://%s:%s/work/changeticketstate/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 3}), headers=headers).json()

