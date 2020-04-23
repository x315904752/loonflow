# encoding: utf-8
import re
import requests, simplejson
from elasticsearch import Elasticsearch
from service.ticket.ticket_base_service import TicketBaseService



mcenter_ip = "10.254.50.54"
mcenter_port = "30042"
username = 'zabbix'
password = 'cernet@123'
ELASTICSEARCHURL = 'http://10.254.50.61:9200'

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

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
for i in reslist:
    if i['field_key'] == 'start_time':
        start_time = str(i['field_value'])
    elif i['field_key'] == 'end_time':
        end_time = str(i['field_value'])

es = Elasticsearch([ELASTICSEARCHURL])
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

a = es.search(index='test', body=search_data)
data = []
operator_type = {"0":"移动","1":"联通","2":"电信","3":"其它"}
for i in a['hits']['hits']:
    info = i['_source']
    if info['duration']:
        res = re.match(r'(\d+)小时(\d+)分钟', info['duration'])
        if int(res.group(1)) or (int(res.group(2)) > 20):
            technician = info['technician']
            if technician:
                user_mc = requests.request(method="GET", url=user_url + technician, headers=headers).json()
                for user in user_mc['results']:
                    if technician == user['username']:
                        technician = user['name']
                        break

            data.append({
                'title': info['title'],
                'gmt_created': info['gmt_created'],
                'duration': info['duration'],
                'end_time': info['end_time'],
                'technician': technician,
                'salesman': info['salesman'],
                'operator': operator_type[info.get('operator', "3")],
                'cause': info.get('cause',''),
                'cause_info': info.get('cause_info',''),
            })

res_list = {
    'sortData': {
        'columns': [
            {
                'tooltip': True,
                'title': '标题',
                'key': 'title',
                'width': 300,
                'align': 'left',
                'sortable': True
            },
            {
                'title': '产生时间',
                'key': 'gmt_created',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '持续时间',
                'key': 'duration',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '结束时间',
                'key': 'end_time',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '技术人员',
                'key': 'technician',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '销售人员',
                'key': 'salesman',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '运营商',
                'key': 'operator',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '故障原因',
                'key': 'cause',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '故障说明',
                'key': 'cause_info',
                'align': 'left',
                'sortable': True
            },
        ],
        'data': data,
    }
}
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(res_list)})
headers['Content-Type'] = 'application/json'
requests.patch('http://%s:%s/report/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束'}), headers=headers)
a = requests.patch('http://%s:%s/report/changeticketstate/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 10054}), headers=headers).json()
print(a)


