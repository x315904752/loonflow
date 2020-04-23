# encoding: utf-8
import sys, os
import requests
import simplejson
import time, datetime
import re
from service.ticket.ticket_base_service import TicketBaseService
from pyzabbix import ZabbixAPI

class Zabbix(object):
    def __init__(self):
        try:
            self.ip = "10.254.50.51"
            self.port = '30486'
            #self.port = '31806'
            self.username = 'Admin'
            self.password = '123456aA?'
        except:
            pass

    def login(self):
        ZABBIX_SERVER = 'http://%s:%s' % (self.ip, self.port)
        zapi = ZabbixAPI(ZABBIX_SERVER)
        zapi.login(self.username, self.password)
        return zapi


zapi = Zabbix().login()

username_dict = {
    'wanglong': '王龙',
    'wumingrui': '吴明睿',
    'shibenteng': '史奔腾',
    'zhangshancun': '张善存',
    'xulei': '徐磊',
    'yanglianlei': '杨连磊',
    'yangxuebin': '杨学斌',
}

fzr_dict = {
    '1': 'wanglong',
    '2': 'zhangshancun',
    '3': 'wumingrui',
    '4': 'shibenteng',
}

input_dict = {
    "start_time": "xxzx_19_kssj",
    "end_time": 'xxzx_19_jssj',
    "userprofile_name": 'xxzx_19_glry',
    "principal":'xxzx_19_fzr',
    "asset_id_str": 'xxxz_19_glzc',
    "servicecluster_id_str": 'xxzx_19_gljq',
    "project_id_str": "xxzx_19_glxm",
}

mcenter_ip = "10.254.50.51"
mcenter_port = "30042"
username = 'xulei'
password = 'cernet@123'

url = 'http://%s:%s/asset/net-flow-network-card/' % (mcenter_ip, mcenter_port)
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
#token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Inh1bGVpIiwiZXhwIjoxNTc4MTk4MTI5LCJlbWFpbCI6Inh1bGVpQGNlcm5ldC5jb20ifQ.toEBeBJjywNvwaikN2AvoohhEnbipLED-wSMbZ3B5h8'
headers = {
    'Authorization': 'JWT ' + token,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}
reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    for k, v in input_dict.items():
        if i['field_key'] == v:
            data[k] = i['field_value']
if '0' in data['principal']:
    data['principal'] = 'wanglong,zhangshancun,wumingrui,shibenteng'
else:
    data['principal'] = ','.join([fzr_dict[p] for p in eval(data['principal'])])
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
                'title': '发送(最大/Mbps)',
                'key': 'r_value_max',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '总流量(最大/Mbps)',
                'key': 'all_value_max',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '协议带宽(Mbps)',
                'key': 'bandwidth',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '负责人',
                'key': 'principal',
                'align': 'center',
                'sortable': True
            },
            {
                'title': '使用率(%)',
                'key': 'per',
                'align': 'center',
                'sortable': True
            }
        ],
        'data': [],
    }
}

params = {"page_size": 1000000, "to_net_flow_asset__to_net_flow_node__to_project":20}
#if data["asset_id_str"]:
#    params["to_basic_info"] = data["asset_id_str"]
#elif data["servicecluster_id_str"]:
#    params["service_cluster"] = data["servicecluster_id_str"]
#elif data["project_id_str"]:
#    params["project"] = data["project_id_str"]
resl = requests.request(method="GET", url=url, headers=headers, params=params)
print(resl.text)
resl = resl.json()['results']
#TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(resl)})
network_list = []
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(network_list)})
for n in resl:
    if n.get('remark', None):
        rebandwidth = re.search('(\d+)mbps', n['remark'], re.IGNORECASE)
        if rebandwidth:
            n['bandwidth'] = int(rebandwidth.group(1))
            principal_re = n['remark'].split('-')
            if len(principal_re) == 3:
                n['principal'] = principal_re[1]
            else:
                n['principal'] = ''
            network_list.append(n)
principal_list = data["principal"].split(',')
principal_list = [username_dict[n] for n in principal_list]
starttime = int(time.mktime(time.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S")))
endtime = int(time.mktime(time.strptime(data['end_time'], "%Y-%m-%d %H:%M:%S")))
delay = (endtime - starttime) > 604800
for n in network_list:
    if n["principal"] in principal_list:
        item_id_str = n.get('item_id', None)
        print(item_id_str)
        item_dict[n['id']] = item_dict.get(n['id'], {})
        if item_id_str and (item_id_str!='None,None'):
            item_id_list = item_id_str.split(',')
            for item_id in item_id_list:
                value_list = []
                righttime = starttime
                time_flag = True
                while righttime < endtime:
                    if time_flag:
                        lefttime = righttime
                        righttime = (righttime+86400) if (endtime-righttime)>86400 else endtime
                    if datetime.datetime.fromtimestamp(lefttime).weekday() > 4:
                        if lefttime < righttime:
                            lefttime += 1
                            time_flag = False
                        else:
                            time_flag = True
                        continue
                    elif datetime.datetime.fromtimestamp(righttime).weekday() > 4:
                        if lefttime < (righttime-1):
                            righttime -= 1
                            time_flag = False
                        else:
                            time_flag = True
                            righttime = (righttime+86400*2) if (endtime-righttime)>86400*2 else endtime
                        continue
                    try_flag = 1
                    time_flag = True
                    while try_flag:
                        try:
                            awsl = zapi.history.get(
                                output='extend',
                                itemids=int(item_id),
                                time_from=lefttime,
                                time_till=righttime,
                            )
                            if len(awsl) > 0:
                                for i in range(0, len(awsl), 1):
                                    value_list.append(int(awsl[i]['value']))
                            else:
                                for i in range(lefttime, righttime, 300):
                                    value_list.append(0)
                        except Exception as e:
                            print('获取失败')
                            print(e.args)
                            time.sleep(5)
                        else:
                            try_flag = 0
                value_list.sort()
                print(len(value_list))
                length = len(value_list)
                if length == 0:
                    value_list = [0]
                if item_id == item_id_list[0]:
                    item_dict[n['id']].update({'d_value_max': value_list[int(length*0.95 - 1)]})
                else:
                    item_dict[n['id']].update({'r_value_max': value_list[int(length*0.95 - 1)]})
        d_value_max = round(item_dict[n['id']].get('d_value_max', 0)/1000000, 2)
        r_value_max = round(item_dict[n['id']].get('r_value_max', 0)/1000000, 2)
        res_list['sortData']['data'].append({
            'name': n['remark'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'd_value_max': d_value_max,
            'r_value_max': r_value_max,
            'all_value_max': max(d_value_max,r_value_max),
            'bandwidth': n['bandwidth'],
            'per': round(max(d_value_max, r_value_max)/n['bandwidth']*100,2) if n['bandwidth'] else round(max(d_value_max, r_value_max)*100,2),
            'principal': n['principal']
        })
print(res_list)
headers['Content-Type'] = 'application/json'
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(res_list)})
requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束', "state_id": 9963}), headers=headers)
requests.patch('http://%s:%s/report/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束', "state_id": 9963}), headers=headers)
basepath = '/opt/loonflow/media/workflow_script/'
today = datetime.date.today().strftime('%Y%m%d')
today_path = basepath + today
if os.path.exists(today_path) != True:
    os.mkdir(today_path, 777)
now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
finpath  = today_path + '/' + str(ticket_id) + '-' + now + '.txt'
os.system('echo "' + str(res_list) + '">>' + finpath)
a = requests.patch('http://%s:%s/work/changeticketstate/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 9963}), headers=headers).json()
TicketBaseService.update_ticket_custom_field(ticket_id,{"report_forms": str(res_list)})
