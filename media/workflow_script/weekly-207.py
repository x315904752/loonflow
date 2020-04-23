# encoding: utf-8
import sys
import requests
import simplejson
import time
import re
import operator
from elasticsearch import Elasticsearch
from service.ticket.ticket_base_service import TicketBaseService


def data_to_table_str(title_key_list, title_list, data):
    table_str = '<table border="0" width="100%" cellpadding="0" cellspacing="0"><tbody>'
    table_str = table_str + '<tr>'
    for title in title_list:
        table_str = table_str + '<th>' + title + '</th>'
    table_str = table_str + '</tr>'
    for td in data:
        table_str = table_str + '<tr>'
        for td_key in title_key_list:
            table_str = table_str + '<td>' + str(td[td_key]) + '</td>'
        table_str = table_str + '<tr>'
    table_str = table_str + '</tbody></table>'
    return table_str



# ticket_id = 1
# reslist = [
#     {
#         'field_key': 'start_time',
#         'field_value': '2019-10-21 00:00:00'
#     },
#     {
#         'field_key': 'end_time',
#         'field_value': '2019-10-26 00:00:00'
#     },
# ]
reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
print(reslist, flag)
for i in reslist:
    if i['field_key'] == 'start_time':
        start_time = str(i['field_value'])
    elif i['field_key'] == 'end_time':
        end_time = str(i['field_value'])
starttime = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
endtime = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
alltime = (endtime - starttime) / 60

username_dict = {
    'wanglong': '王龙',
    'wumingrui': '吴明睿',
    'shibenteng': '史奔腾',
    'zhangshancun': '张善存',
    'xulei': '徐磊',
    'yanglianlei': '杨连磊',
    'yangxuebin': '杨学斌',
}

mcenter_ip = "10.254.50.230"
mcenter_port = "31001/v1"
username = 'xulei'
password = 'cernet@123'
ELASTICSEARCHURL = 'http://10.254.50.230:32765'

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

es = Elasticsearch([ELASTICSEARCHURL])
print(1)
search_data = {
    "query": {
        "bool": {
            "must": [{
                "term": {
                    'is_delete': False,
                }
            }, {
                "term": {
                    'to_project_id': 20
                }
            }, {
                "term": {
                    'workflow_id': 32
                }
            }, {
                "simple_query_string": {
                    'query': '"中断"',
                    'fields': ['title']
                }
            }, {
                "exists": {
                    "field": "duration"
                }
            },{
                "range": {
                    'gmt_created': {
                        'gte': start_time,
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||yyyy-MM||yyyy||strict_date_optional_time||epoch_millis"
                    }
                }
            }, {
                "range": {
                    'gmt_created': {
                        'lte': end_time,
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||yyyy-MM||yyyy||strict_date_optional_time||epoch_millis"
                    }
                }
            },
            ],
            "must_not": [{
                "term": {
                    'duration.key_word': '',
                }
            }]
        },
    },
    'sort': {
        "gmt_created": {
            "order": "asc"
        }
    },
    'size': 2000
}

es_result = es.search(index='alarm', body=search_data)
data = []
operator_type = {"0": "移动","1": "联通","2": "电信","3": "其它"}
print(2)
for i in es_result['hits']['hits']:
    info = i['_source']
    if info['duration']:
        technician = info['technician']
        if technician:
            user_mc = requests.request(method="GET", url=user_url + technician, headers=headers).json()
            for user in user_mc['results']:
                if technician == user['username']:
                    technician = user['name']
                    break
        res = re.match(r'(\d+)小时(\d+)分钟', info['duration'])
        duration = int(res.group(1)) * 60 + int(res.group(2)) + 10
        h, m = divmod(duration, 60)
        info['duration'] = str(h) + '小时' + str(m) + '分钟'
        data.append({
            'title': info['title'],
            'gmt_created': info['gmt_created'].replace('T', ' '),
            'duration': info['duration'],
            'end_time': info['end_time'],
            'technician': technician,
            'salesman': info['salesman'],
            'operator': operator_type[info.get('operator', "3")],
            'cause': info.get('cause', ''),
            'cause_info': info.get('cause_info', ''),
        })
title_key_list = ['title', 'gmt_created', 'duration', 'end_time',  'technician', 'salesman', 'operator', 'cause', 'cause_info']
title_list = ['标题', '产生时间', '持续时间', '结束时间', '技术人员', '销售人员', '运营商', '故障原因', '故障说明']
table1 = data_to_table_str(title_key_list, title_list, data)

url = 'http://%s:%s/asset/net-flow-network-card/?is_delete=false&to_net_flow_asset__to_net_flow_node__to_project=20' % (mcenter_ip, mcenter_port)
print(3)
title_key_list2 = ['name', 'start_time', 'end_time', 'principal', 'count', 'time', 'per']
title_list2 = ['学校名称', '开始时间', '结束时间', '负责人', '中断次数', '中断时间(分钟)', '可用率(%)']

params = {"page_size": 1000000, 'search': 'mbps'}

resl = requests.request(method="GET", url=url, headers=headers, params=params, timeout=100000).json()['results']
principal_list = ['王龙', '史奔腾', '张善存', '吴明睿']
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

print(4)
for i in es_result['hits']['hits']:
    info = i['_source']
    if info['duration']:
        duration = re.match(r'(\d+)小时(\d+)分钟', info['duration'])
        for s in school_list:
            if s in info['title']:
                conut_dict[s] += 1
                time_dict[s] = time_dict[s] + int(duration.group(1)) * 60 + int(duration.group(2))
data2 = []
for s in school_list:
    data2.append({
        'name': s,
        'start_time': start_time,
        'end_time': end_time,
        'principal': principal_dict[s],
        'count': conut_dict[s],
        'time': time_dict[s],
        'per':  round((1 - time_dict[s]/alltime) * 100, 2)
    })
data2 = sorted(data2, key=operator.itemgetter('per'))
table2 = data_to_table_str(title_key_list2, title_list2, data2)
base_str = '<html><head><meta charset="utf-8"></head><div style="text-align: center;"><span style="font-size: xx-large; font-weight: bold;">值班周报</span></div><div style="text-align: center;"><span style="font-size: xx-large;">({}至{})</span></div><div style="text-align: left;"><span style="font-size: x-large;">一. 链路故障</span></div><div style="text-align: left;">{}<span style="font-size: x-large;"><br></span></div><div style="text-align: left;"><span style="font-size: x-large;">二. 主页故障</span></div><div style="text-align: left;"><table border="0" width="100%" cellpadding="0" cellspacing="0"><tbody><tr><th>序号&nbsp;</th><th>高校&nbsp;</th><th>&nbsp;主页</th><th>故障&nbsp;</th><th>开始时间&nbsp;</th><th>&nbsp;持续时间</th><th>&nbsp;原因</th><th>&nbsp;备注</th></tr><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></tbody></table><p><br></p></div><div style="text-align: left;"><span style="font-size: x-large;">三. 网盾防护</span></div><div style="text-align: left;"><span style="font-size: large;">网盾攻击数目超过1000次, 自动封禁</span></div><div style="text-align: left;"><table border="0" width="100%" cellpadding="0" cellspacing="0"><tbody><tr><th>序号&nbsp;</th><th>IP&nbsp;</th><th>备注&nbsp;</th></tr><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></tbody></table><p><br></p></div><div style="text-align: left;"><span style="font-size: x-large;">四. 链路可用性</span></div>{}<p><br></p>'.format(start_time[:10], end_time[:10], table1, table2)
print(5)
headers['Content-Type'] = 'application/json'
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": base_str})
try:
    requests.patch('http://10.254.50.230:31001/v1/work/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10077,'state_name': '相关人员处理', 'participant':'徐磊,杨学斌,王龙'}), headers=headers)
    a = requests.patch('http://10.254.50.230:31001/v1/work/changeticketstate/%s/' % (ticket_id),data=simplejson.dumps({"state_id": 10077}), headers=headers)
except Exceptions as e:
    pass
try:
    requests.patch('http://10.254.50.230:31001/v1/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10077,'state_name': '相关人员处理', 'participant':'徐磊,杨学斌,王龙'}), headers=headers)
    a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketstate/%s/' % (ticket_id),data=simplejson.dumps({"state_id": 10077}), headers=headers)
except Exceptions as e:
    pass


