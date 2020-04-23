# encoding: utf-8
import sys
import requests
import time
import re
from service.ticket.ticket_base_service import TicketBaseService


input_dict = {
    "start_time": "xxzx_21_kssj",
    "end_time": 'xxzx_21_jssj',
    "userprofile_name": 'xxzx_21_glry',
    "principal":'xxzx_21_fzr',
}
username_dict = {
    'wanglong': '王龙',
    'wumingrui': '吴明睿',
    'shibenteng': '史奔腾',
    'zhangshancun': '张善存',
    'xulei': '徐磊',
    'yanglianlei': '杨连磊',
    'yangxuebin': '杨学斌',
}

mcenter_ip = "10.254.50.54"
mcenter_port = "30042"
username = 'zabbix'
password = 'cernet@123'
url = 'http://%s:%s/cmdb/network-card/' % (mcenter_ip, mcenter_port)
url2 = 'http://%s:%s/alert/alert/' % (mcenter_ip, mcenter_port)
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

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}

for i in reslist:
    for k, v in input_dict.items():
        if i['field_key'] == v:
            data[k] = str(i['field_value'])
res_list = {
    'sortData': {
        'columns': [
            {
                'tooltip': True,
                'title': '学校名称',
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
                'title': '负责人',
                'key': 'principal',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '中断次数',
                'key': 'count',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '中断时间(分钟)',
                'key': 'time',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '可用率(%)',
                'key': 'per',
                'align': 'center',
                'sortable': True
            }
        ],
        'data': [],
    }
}

params = {"page_size": 1000000, 'search': 'mbps'}

resl = requests.request(method="GET", url=url, headers=headers, params=params, timeout=100000).json()['results']
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(resl)})

principal_list = [username_dict[i] for i in data["principal"].split(',')]
principal_dict = {}
school_list = []
for n in resl:
    if n.get('remark', None):
        rebandwidth = re.search('(\d+)mbps', n['remark'], re.IGNORECASE)
        if rebandwidth:
            n['bandwidth'] = int(rebandwidth.group(1))
            principal_re = n['remark'].split('-')
            if len(principal_re) == 3:
                if principal_re[1] in principal_list:
                    if principal_re[0] not in school_list:
                        school_list.append(principal_re[0])
                        principal_dict[principal_re[0]] = principal_re[1]
conut_dict = {}
time_dict = {}
for s in school_list:
    conut_dict[s] = 0
    time_dict[s] = 0
starttime = time.mktime(time.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S"))
endtime = time.mktime(time.strptime(data['end_time'], "%Y-%m-%d %H:%M:%S"))
alltime = (endtime - starttime) / 60
params2 = {"page_size": 1000000, 'search': '链路中断', 'start_time':data['start_time'], 'end_time': data['end_time']}
#res2 = requests.request(method="GET", url=url2, headers=headers, params=params2, timeout=100000).json()['results']
#for a in res2:
#    for s in school_list:
#        if s in a['alarm_content']:
#            conut_dict[s] += 1
#            duration = re.search('(\d+)天(\d+)小时(\d+)分', a["duration"])
#            time_dict[s] = time_dict[s] + int(duration.group(1))*1440 + int(duration.group(2))*60 + int(duration.group(3))

for s in school_list:
    res_list['sortData']['data'].append({
        'name': s,
        'start_time': data['start_time'],
        'end_time': data['end_time'],
        'principal': principal_dict[s],
        'count': 0,
        'time': 0,
        'per':  0
    })
user_list = data["userprofile_name"].split(',')
for user in user_list:
    TicketBaseService.add_ticket_relation(ticket_id, user)
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(res_list)})

