# encoding: utf-8
import sys
import requests
import simplejson
import time
from service.ticket.ticket_base_service import TicketBaseService

input_dict = {
    "start_time": "xxzx_15_kssj",
    "end_time": 'xxzx_15_jssj',
    "userprofile_name": 'xxzx_15_glry',
    "asset_id_str": 'xxxz_15_glzc',
    "business_id_str": 'xxzx_15_glyw',
    "project_id_str": "xxzx_15_glxm",
}

mcenter_ip = "10.254.30.27"
mcenter_port = "8008"
username = 'xulei'
password = '123456a?'

url = 'http://%s:%s/alert/alert/' % (mcenter_ip, mcenter_port)

try:
    get_token = requests.post(
        'http://%s:%s/api-token-auth/' % (mcenter_ip, mcenter_port),
        data={"username": username, "password": password},
    ).text
except:
    print("Can not connect url:http://%s:%s/api-token-auth/" % (mcenter_ip, mcenter_port))
token = simplejson.loads(get_token)['token']
headers = {
    'Authorization': 'JWT ' + token,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

reslist, flag = TicketBaseService.get_ticket_base_filed_list(ticket_id)


data = {}
for i in reslist:
    for k, v in input_dict.items():
        if i['field_key'] == v:
            data[k] = str(i['field_value'])

alertlist = []
params = { 'page_size': 1000000,'start_time':data["start_time"],'end_time':data["end_time"]}
if data["project_id_str"]:
    params['to_project'] = data["project_id_str"]
    alertp = requests.request(method="GET", url=url, headers=headers, params=params, timeout=100000).json()[
        'results']
    alertlist += alertp
    print(alertlist)
    params = { 'page_size': 1000000,'start_time':data["start_time"],'end_time':data["end_time"]}
if data["business_id_str"]:
    params['to_bearer_service'] = data["business_id_str"]
    alertp = requests.request(method="GET", url=url, headers=headers, params=params, timeout=100000).json()[
        'results']
    alertlist += alertp
    print(alertlist)
    params = {'page_size': 1000000, 'start_time': data["start_time"], 'end_time': data["end_time"]}
if data["asset_id_str"]:
    params['to_basic_info'] = data["asset_id_str"]
    alertp = requests.request(method="GET", url=url, headers=headers, params=params, timeout=100000).json()[
        'results']
    alertlist += alertp
bearer_alert = {}
print(alertlist)
for alert in alertlist:
    if alert['to_bearer_service']:
        name = alert['to_bearer_service']
        if bearer_alert.get(name, None):
            bearer_alert[name].append(alert)
        else:
            bearer_alert[name] = [alert]
    else:
        if bearer_alert.get("未分类", None):
            bearer_alert["未分类"].append(alert)
        else:
            bearer_alert["未分类"] = [alert]
resstr = str(bearer_alert)
print(bearer_alert)
user_list = data["userprofile_name"].split(',')
for user in user_list:
    TicketBaseService.add_ticket_relation(ticket_id, user)
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": resstr})
