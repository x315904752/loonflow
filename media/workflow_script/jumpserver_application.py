# encoding: utf-8
import sys
import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService

end_time = 'xxzx_13_jssj'
userprofile_name = 'creator'
asset_id_str = 'cmdb_basic_info_multiple'

mcenter_ip = "10.254.50.52"
mcenter_port = "30042"
username = 'zabbix'
password = 'cernet@123'
url = 'http://%s:%s/jumpserver/applications/' % (mcenter_ip, mcenter_port)
try:
    get_token = requests.post(
        'http://%s:%s/api-token-auth/' % (mcenter_ip, mcenter_port),
        data={"username": username, "password": password},
    ).text
except:
    logger.info("Can not connect url:http://%s:%s/api-token-auth/" % (mcenter_ip, mcenter_port))
token = simplejson.loads(get_token)['token']
headers = {'Authorization': 'JWT ' + token}
data = {}
reslist,flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
for i in reslist:
    if i['field_key'] == end_time:
        data['end_time'] = i['field_value']
    elif i['field_key'] == userprofile_name:
        data['user_name'] = i['field_value']
    elif i['field_key'] == asset_id_str:
        data['asset_id_str'] = i['field_value']
res = requests.request(method="GET", url=url, params=data, headers=headers)
TicketBaseService.update_ticket_custom_field(ticket_id,{"xxzx_13_text":res.text})

headers['Content-Type'] = 'application/json'
requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 10035 ,'state_name':'结束'}), headers=headers)

