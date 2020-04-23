# encoding: utf-8
import sys
import requests
import simplejson
import time
from pyzabbix import ZabbixAPI

from service.ticket.ticket_base_service import TicketBaseService

class Zabbix(object):
    def __init__(self):
        try:
            self.ip = "58.195.98.222"
            self.port = '8000'
            self.username = 'admin'
            self.password = 'X2iparp.com'
        except:
            pass

    def login(self):
        ZABBIX_SERVER = 'http://%s:%s' % (self.ip, self.port)
        zapi = ZabbixAPI(ZABBIX_SERVER)
        zapi.login(self.username, self.password)
        return zapi


zapi = Zabbix().login()



input_dict = {
    "start_time": "xxzx_17_kssj",
    "end_time": 'xxzx_17_jssj',
    "userprofile_name": 'xxzx_17_glry',
    "asset_id_str": 'xxxz_17_glzc',
    "servicecluster_id_str": 'xxzx_17_gljq',
    "project_id_str": "xxzx_17_glxm",
}

mcenter_ip = "10.254.40.250"
mcenter_port = "9999"
username = 'xulei'
password = 'cernet@123'

url = 'http://%s:%s/cmdb/network-card/' % (mcenter_ip, mcenter_port)
try:
    get_token = requests.post(
        'http://%s:%s/api-token-auth/' % (mcenter_ip, mcenter_port),
        data={"username": username, "password": password},
    ).json()
except:
    print("Can not connect url:http://%s:%s/api-token-auth/" % (mcenter_ip, mcenter_port))
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(get_token)})
try:
    token = get_token['token']
except:
    print(get_token)
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
item_dict = dict()
res_list = {
    'sortData': {
        'columns': [
            {
                'tooltip': True,
                'title': '名称',
                'key': 'name',
                'width': 300,
                'align': 'left',
                'sortable': True
            },
            {
                'title': '开始时间',
                'key': 'start_time',
                'align': 'left',
                'sortable': True
            },
            {
                'title': '结束时间',
                'key': 'end_time',
                'align': 'left',
                'sortable': True
            },
            {
                'title': '接收(最大/Mbps)',
                'key': 'd_value_max',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '接收(最小/Mbps)',
                'key': 'd_value_min',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '接收(平均/Mbps)',
                'key': 'd_value_avg',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '发送(最大/Mbps)',
                'key': 'r_value_max',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '发送(最小/Mbps)',
                'key': 'r_value_min',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '发送(平均/Mbps)',
                'key': 'r_value_avg',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '总流量(平均/Mbps)',
                'key': 'all_value_avg',
                'align': 'center',
                'sortable': True
            },
        ],
        'data': [],
    }
}


params = {"page_size": 1000000}
if data["asset_id_str"]:
    params["to_basic_info"] = data["asset_id_str"]
elif data["servicecluster_id_str"]:
    params["service_cluster"] = data["servicecluster_id_str"]
elif data["project_id_str"]:
    params["project"] = data["project_id_str"]

resl = requests.request(method="GET", url=url, headers=headers, params=params, timeout=100000).json()['results']
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(resl)})

for n in resl:
    if n.get('remark', None):
        item_id_str = n.get('item_id', None)
        item_dict[n['id']] = item_dict.get(n['id'], {})
        if item_id_str:
            item_id_list = item_id_str.split(',')
            for item_id in item_id_list:
                awsl = zapi.trend.get(
                    output='extend',
                    itemids=int(item_id),
                    time_from=time.mktime(time.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S")),
                    time_till=time.mktime(time.strptime(data['end_time'], "%Y-%m-%d %H:%M:%S")),
                )
                count = 0
                sumall = 0
                value_min = float('Inf') if len(awsl) else 0
                value_max = float('-Inf') if len(awsl) else 0
                for i in awsl:
                    count += int(i['num'])
                    sumall += int(i['num']) * float(i['value_avg'])
                    if float(i['value_min']) < value_min:
                        value_min = float(i['value_min'])
                    if float(i['value_max']) > value_max:
                        value_max = float(i['value_max'])

                value_avg = sumall / count if count else 0
                if item_id == item_id_list[0]:
                    item_dict[n['id']].update({'d_value_max': value_max})
                    item_dict[n['id']].update({'d_value_min': value_min})
                    item_dict[n['id']].update({'d_value_avg': value_avg})
                else:
                    item_dict[n['id']].update({'r_value_max': value_max})
                    item_dict[n['id']].update({'r_value_min': value_min})
                    item_dict[n['id']].update({'r_value_avg': value_avg})
        res_list['sortData']['data'].append({
            'name': n['remark'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'd_value_max': round(item_dict[n['id']].get('d_value_max', 0) / 1000000, 2),
            'd_value_min': round(item_dict[n['id']].get('d_value_min', 0) / 1000000, 2),
            'd_value_avg': round(item_dict[n['id']].get('d_value_avg', 0) / 1000000, 2),
            'r_value_max': round(item_dict[n['id']].get('r_value_max', 0) / 1000000, 2),
            'r_value_min': round(item_dict[n['id']].get('r_value_min', 0) / 1000000, 2),
            'r_value_avg': round(item_dict[n['id']].get('r_value_avg', 0) / 1000000, 2),
            'all_value_avg': round(
                (item_dict[n['id']].get('r_value_avg', 0) + item_dict[n['id']].get('d_value_avg', 0)) / 1000000, 2)
        })
user_list = data["userprofile_name"].split(',')
for user in user_list:
    TicketBaseService.add_ticket_relation(ticket_id, user)
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(res_list)})

