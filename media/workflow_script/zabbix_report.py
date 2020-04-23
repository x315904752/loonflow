# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
import requests
import simplejson
import time, datetime
import sys,os

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

mcenter_ip = "10.254.40.250"
mcenter_port = "9999"
username = 'xulei'
password = 'cernet@123'
url = 'http://%s:%s/cmdb/bear-service/' % (mcenter_ip, mcenter_port)

input_dict = {
    "start_time": "xxzx_16_kssj",
    "end_time": 'xxzx_16_jssj',
    "userprofile_name": 'xxzx_16_glry',
    "business_id_str": 'xxzx_16_glyw',
    "project_id_str": "xxzx_16_glxm",
}

reslist, flag = TicketBaseService.get_ticket_base_filed_list(ticket_id)
data = {}
for i in reslist:
    for k, v in input_dict.items():
        if i['field_key'] == v:
            data[k] = str(i['field_value'])

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
business_host_id_list = []

if data["business_id_str"] == '':
    params = {"to_project": data["project_id_str"], "page_size": 100000}
else:
    params = {"id": data["business_id_str"], "page_size": 100000}

res = requests.request(method="GET", url=url, headers=headers, params=params, timeout=100000).text
res = simplejson.loads(res)
host_name = {}
item_dict = {}
for i in res["results"]:
    if i["monitor_code"]:
        host_name[i["monitor_code"]] = i["name"]
        business_host_id_list.append(i["monitor_code"])
        item_dict[i["monitor_code"]] = {}
item_d_all = zapi.item.get(
    output=["itemid", "hostid", "name"],
    hostids=business_host_id_list,
    webitems=True,
    search={
        "name": "Download speed for scenario",
    }
)
item_r_all = zapi.item.get(
    output=["itemid", "hostid", "name"],
    hostids=business_host_id_list,
    webitems=True,
    search={
        "name": "Response time for step",
    }
)
item_all = item_d_all + item_r_all
res_list = {
    'sortData': {
        'columns': [
            {
                'tooltip': True,
                'title': '业务名',
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
                'title': '下载速度(最大/Kbps)',
                'key': 'd_value_max',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '下载速度(最小/Kbps)',
                'key': 'd_value_min',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '下载速度(平均/Kbps)',
                'key': 'd_value_avg',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '响应时间(最大/ms)',
                'key': 'r_value_max',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '响应时间(最小/ms)',
                'key': 'r_value_min',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '响应时间(平均/ms)',
                'key': 'r_value_avg',
                'align': 'center',
                'sortable': True
            },
        ],
        'data': [],
    }
}
for item in item_all:
    awsl = zapi.trend.get(
        output='extend',
        itemids=item['itemid'],
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
    if item['name'][0] == 'D':
        item_dict[item['hostid']].update({'d_value_max': value_max})
        item_dict[item['hostid']].update({'d_value_min': value_min})
        item_dict[item['hostid']].update({'d_value_avg': value_avg})
    else:
        item_dict[item['hostid']].update({'r_value_max': value_max})
        item_dict[item['hostid']].update({'r_value_min': value_min})
        item_dict[item['hostid']].update({'r_value_avg': value_avg})

for hostid in business_host_id_list:
    res_list['sortData']['data'].append({
        'name': host_name[hostid],
        'start_time': data['start_time'],
        'end_time': data['end_time'],
        'd_value_max': round(item_dict[hostid].get('d_value_max', 0)/1000, 2),
        'd_value_min': round(item_dict[hostid].get('d_value_min', 0)/1000, 2),
        'd_value_avg': round(item_dict[hostid].get('d_value_avg', 0)/1000, 2),
        'r_value_max': round(item_dict[hostid].get('r_value_max', 0)*1000, 2),
        'r_value_min': round(item_dict[hostid].get('r_value_min', 0)*1000, 2),
        'r_value_avg': round(item_dict[hostid].get('r_value_avg', 0)*1000, 2),
    })
resstr = str(res_list)
user_list = data["userprofile_name"].split(',')
for user in user_list:
    TicketBaseService.add_ticket_relation(ticket_id, user)
TicketBaseService.update_ticket_custom_field(ticket_id, {"report_forms": resstr})

