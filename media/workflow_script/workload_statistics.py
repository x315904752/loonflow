# encoding: utf-8
import sys
import requests
import simplejson
import datetime
from service.ticket.ticket_base_service import TicketBaseService

input_dict = {
    "start_time": "kssj",
    "end_time": 'jssj',
    "project": "glxm",
}
data = {}
type_list = ['数据库', '服务器', '网络', '安全', '环控', '其它']
reslist, flag = TicketBaseService.get_ticket_base_filed_list(ticket_id)
for i in reslist:
    for k, v in input_dict.items():
        if i['field_key'] == v:
            data[k] = str(i['field_value'])
mcenter_ip = "10.254.40.250"
mcenter_port = "9999"
username = 'xulei'
password = 'cernet@123'

url = 'http://%s:%s/work/workflow/?rela_to_project=%s' % (mcenter_ip, mcenter_port, data["project"])

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


# res = requests.request(method="GET", url=url, headers=headers, params=data,timeout=100000).text
res = requests.request(method="GET", url=url, headers=headers).json()
flow_id = 0
for i in res:
    if i['flow_type'] == 8:
        flow_id = i['flow_id']
lxtj = {}
rytj = {}
sjtj = []
if flow_id:
    url2 = 'http://%s:%s/api/tickets/' % (mcenter_ip, mcenter_port)
    params = {
        'workflow_ids': flow_id,
        'per_page': 10000,
        'category': 'all',
        'start_time': data["start_time"],
        'end_time': data["end_time"]
    }
    res2 = requests.request(method="GET", url=url2, params=params, headers=headers).json()
    id_list = [i["id"] for i in res2['data']['value']]
    for ticket in id_list:
        creator, nothing = TicketBaseService.get_ticket_field_value(ticket, 'creator')
        ticket_data, nothing = TicketBaseService.get_ticket_field_value(ticket, 'data')
        gmt_created, nothing = TicketBaseService.get_ticket_field_value(ticket, 'gmt_created')
        if ticket_data:
            real_data = eval(ticket_data)
            for log in real_data:
                if log['time']:
                    if log['type'] != '':
                        lxtj[type_list[log['type']]] = lxtj.get(type_list[log['type']], 0) + float(log['time'])
                    else:
                        lxtj['未选择类型'] = lxtj.get('未选择类型', 0) + float(log['time'])
                rytj[creator] = rytj.get(creator, 0) + 1
                sjtj.append({
                    'type': type_list[log['type']] if log['type'] != '' else '未选择类型',
                    'desc': log['desc'],
                    'date': gmt_created.strftime("%Y-%m-%d"),
                    'time': log['time'],
                    'creator': creator
                })
print(sjtj)
TicketBaseService.update_ticket_custom_field(ticket_id,{"lxtj": str(lxtj)})
TicketBaseService.update_ticket_custom_field(ticket_id,{"rytj": str(rytj)})
TicketBaseService.update_ticket_custom_field(ticket_id,{"sjtj": str(sjtj)})
print(1)
