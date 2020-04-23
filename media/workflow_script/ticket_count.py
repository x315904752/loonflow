# encoding: utf-8
import requests, simplejson
from service.ticket.ticket_base_service import TicketBaseService

mcenter_ip = "10.254.50.54"
mcenter_port = "30042"
username = 'zabbix'
password = 'cernet@123'

ticket_project_url =  'http://%s:%s/work/ticket-project-count/' % (mcenter_ip, mcenter_port)
ticket_date_url =  'http://%s:%s/work/ticket-date-count/' % (mcenter_ip, mcenter_port)
ticket_list_url =  'http://%s:%s/work/ticketslist/' % (mcenter_ip, mcenter_port)
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
field_list, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
params = {}
for i in field_list:
    if i['field_key'] == 'start_time':
        params['start_time'] = str(i['field_value'])
    elif i['field_key'] == 'end_time':
        params['end_time'] = str(i['field_value'])
    elif i['field_key'] == 'to_project_id':
        params['to_project'] = str(i['field_value'])

ticket_project = requests.get(ticket_project_url, params=params, headers=headers).json()
ticket_date = requests.get(ticket_date_url, params=params, headers=headers).json()

post_data = {
    'search': [
        {
            'key': 'gmt_created',
            'action': 'gte',
            'value': params['start_time']
        },
        {
            'key': 'gmt_created',
            'action': 'lte',
            'value': params['end_time']
        },
        {
            'key': 'to_project_id',
            'action': 'eq',
            'value': params['to_project']
        },
    ],
    'page': 1,
    'page_size': 100000,
}
headers['Content-Type'] = 'application/json'
ticket_mc = requests.post(ticket_list_url, data=simplejson.dumps(post_data), headers=headers).json()
ticket_list = []
for i in ticket_mc['results']:
    ticket_list.append({
        'title': i['title'],
        'ticket_id': i['ticket_id'],
        'workflow_name': i['workflow_name'],
        'creator': i['creator'],
        'gmt_created': i['gmt_created'].replace('T', ' ')
    })

ticket_table_list = {
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
            'title': '工作流名称',
            'key': 'workflow_name',
            'align': 'center',
            'sortable': True
        },
        {
            'title': '创建人',
            'key': 'creator',
            'align': 'center',
            'sortable': True
        },
        {
            'title': '创建时间',
            'key': 'gmt_created',
            'align': 'center',
        },
    ],
    'data': ticket_list,
}

res_list = {
    'ticket_project': ticket_project,
    'ticket_date': ticket_date,
    'ticket_table_list': ticket_table_list
}
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(res_list)})
try:
    requests.patch('http://%s:%s/report/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束'}), headers=headers)
    a = requests.patch('http://%s:%s/report/changeticketstate/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 10057}), headers=headers).json()
    print(a)
except:
    pass
try:
    requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束'}), headers=headers)
    a = requests.patch('http://%s:%s/work/changeticketstate/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 10057}), headers=headers).json()
    print(a)
except:
    pass


