import requests
import simplejson
import time
import datetime
from service.ticket.ticket_base_service import TicketBaseService
from pyzabbix import ZabbixAPI


class Zabbix(object):
    def __init__(self):
        try:
            self.ip = "10.254.50.53"
            self.port = '30486'
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

headers = {}
url = 'http://10.254.50.52:30042/asset/net-flow-network-card/?to_net_flow_asset__to_net_flow_node__to_project=19&is_delete=false&page_size=1000000'

class WeekPaper(object):
    def __init__(self, url='http://10.254.50.51:30042/', project=19):
        self.url = url
        self.project = project

    def getToken(self, username, password):
        url = self.url + 'api-token-auth/'
        data = {
            'v_code': 1,
            'username': username,
            'password': password
        }
        resp = requests.post(url=url, data=data).json()['token']
        return resp

    def getPeople(self):
        title = "<html><head><meta charset='utf-8'><h2 style='text-align: center;'><font face='黑体' style='font - weight: bold;'>山东省青岛市教育局系统运维简报</font></h2>" + \
                "<h2><font face='等线' style='font-weight: bold;'>一、信息汇总</font></h2><h3 class='MsoNormal'><font face='等线'>1.1本周安全监控总述：</font></h3>" + \
                "<h3 class='MsoNormal'><font face='等线'>1.2人员信息：</font></h3>" + \
                "<table border='0' width='100%' cellpadding='0' cellspacing='0'><tbody><tr><th>&nbsp;客户单位</th><th>青岛市教育局</th><th></th><th></th></tr>" \
                "<tr><td>&nbsp;服务地址</td><td>&nbsp;青岛市教育局延安一路29号乙</td></td></td></td></td></tr>" \
                "<tr><td>&nbsp;用户及联系方式</td><td>&nbsp;霍超</td><td>13370860185</td><td>328337428@qq.com</td></tr>" \
                "<tr><td>&nbsp;巡检人员</td><td>&nbsp;牛延群</td><td>18561713559</td><td>348597420@qq.com</td></tr>" \
                "<tr><td>&nbsp;巡检人员</td><td>&nbsp;王朝阳</td><td>18396757612</td><td>1165960378@qq.com</td></tr>" \
                "<tr><td>&nbsp;巡检人员</td><td>&nbsp;盛明任</td><td>15689990332</td><td>459347585@qq.com</td></tr></tbody></table>"
        return title

    def getThingsTable(self):
        table = "<h2><font face='等线' style='font-weight: bold;'>二、基础运维事件分类统计</font></h2><h3 class='MsoNormal'><font face='等线'>2.1本周较重要处理事件列表：</font></h3>"\
                "<table border='0'' width='100%' cellpadding='0' cellspacing='0'><tbody><tr><th>序号</th><th>问题归类</th><th>问题描述</th><th>问题处理</th><th>处理结果</th></tr>" \
                "<tr><td>1</td><td>服务器</td><td>无</td><td>无</td><td>正常</td></tr>" \
                "<tr><td>2</td><td>运维监控</td><td>日常巡检</td><td>设备运行正常</td><td>正常</td></tr>" \
                "<tr><td>3</td><td>动力环境</td><td>无</td><td>无</td><td>正常</td></tr>" \
                "<tr><td>4</td><td>机房</td><td>无</td><td>无</td><td>正常</td></tr>" \
                "<tr><td>5</td><td>安全设备</td><td>无</td><td>无</td><td>正常</td></tr>" \
                "<tr><td>6</td><td>网络设备</td><td>无</td><td>无</td><td>正常</td></tr></tbody></table>" + \
                "<h3 class='MsoNormal'><font face='等线'>2.2设施运行情况：</font></h3>" + \
                "<p class='20'><span style='font-weight: normal;'>&nbsp; &nbsp;&nbsp;</span>&nbsp; &nbsp;&nbsp;<span style='font-family: 宋体; font-size: large;'>运行正常</span></p>" + \
                "<h3 class='MsoNormal'><font face='等线'>2.3网络设备运行情况：</font></h3>" + \
                "<p class='20'><span style='font-weight: normal;'>&nbsp; &nbsp;&nbsp;</span>&nbsp; &nbsp;&nbsp;<span style='font-family: 宋体; font-size: large;'>运行正常</span></p>" + \
                "<h3 class='MsoNormal'><font face='等线'>2.4服务器存储运行情况：</font></h3>" + \
                "<p class='20'><span style='font-weight: normal;'>&nbsp; &nbsp;&nbsp;</span>&nbsp; &nbsp;&nbsp;<span style='font-family: 宋体; font-size: large;'>运行正常</span></p>" + \
                "<h3 class='MsoNormal'><font face='等线'>2.5安全设备：</font></h3>" + \
                "<p class='20'><span style='font-weight: normal;'>&nbsp; &nbsp;&nbsp;</span>&nbsp; &nbsp;&nbsp;<span style='font-family: 宋体; font-size: large;'>运行正常</span></p>" + \
                "<h2><font face='等线' style='font-weight: bold;'>三、现场运维问题处理</font></h2>"
        return table


    def getTikets(self, start_time, end_time):
        url = self.url + 'work/ticketslist/'
        token = 'JWT' + ' ' + self.getToken('xulei', 'cernet@123')
        global headers
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        data = {"search": [{"key": "to_project_id", "action": "eq", "value": 19},
                           {"key": "gmt_created", "action": "gt", "value": start_time},
                           {"key": "gmt_created", "action": "lt", "value": end_time}],
                "page": 1, "page_size": 20}
        data = simplejson.dumps(data)
        resp = requests.post(url=url, headers=headers, data=data).json()['results']
        print(resp)
        print(start_time, end_time)
        title_str = "<table width='100%'><tbody><tr><td>问题描述</td><td>处理结果</td><td>备注</td></tr>"
        for work_flow in resp:
            title_str += "<tr><td>" + work_flow['title'] + "</td><td>" + work_flow.get('sjjl_5_qt','') + "</td><td>"+ work_flow.get('sjjl_5_bz','') +"</td></tr>"
        return title_str + "</tbody></table><h2><font face='等线' style='font-weight: bold;'>四、流量报表</font></h2>"


reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    if i['field_key'] == 'start_time':
        start_time = str(i['field_value'])
    elif i['field_key'] == 'end_time':
        end_time = str(i['field_value'])
week = WeekPaper()
res_list = week.getPeople() + week.getThingsTable() + week.getTikets(start_time, end_time)
header = {
    'Authorization': headers['Authorization']
}
a = requests.request(method="GET", url=url, headers=header).text
print(a)
network_list = requests.request(method="GET", url=url, headers=header).json()['results']
starttime = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
endtime = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")))
delay = (endtime - starttime) > 604800
item_dict = {}
network_tab = []
for n in network_list:
    item_id_str = n.get('item_id', None)
    item_dict[n['id']] = item_dict.get(n['id'], {})
    if item_id_str:
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
                            for i in range(0, len(awsl), 10):
                                value_list.append(int(awsl[i]['value']))
                        else:
                            for i in range(lefttime, righttime, 300):
                                value_list.append(0)
                    except:
                        print(1)
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
    network_tab.append({
        'name': n['remark'],
        'start_time': start_time,
        'end_time': end_time,
        'd_value_max': d_value_max,
        'r_value_max': r_value_max,
        'all_value_max': max(d_value_max,r_value_max),
    })

network_tab = sorted(network_tab, key=lambda x:x['all_value_max'],reverse=True)
table_str = "<table border='0'' width='100%' cellpadding='0' cellspacing='0'><tbody><tr><th>名称</th><th>开始时间</th><th>结束时间</th><th>接受(最大/Mbps)</th><th>发送(最大/Mbps)</th><th>总流量(最大/Mbps)</th></tr>"
for n in network_tab:
    table_str += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(n['name'], start_time, end_time, n['d_value_max'], n['r_value_max'], n['all_value_max'])
table_str += "</tbody></table>"
res_list += table_str
res_list += "<h2><font face='等线' style='font-weight: bold;'>五、下周工作计划和措施</font></h2></html>"
TicketBaseService.update_ticket_custom_field(ticket_id, {"report_forms": str(res_list)})
a = requests.patch('http://10.254.50.51:30042/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '牛延群,徐磊','state_name':'相关人员处理'}), headers=headers)
print(a)
a = requests.patch('http://10.254.50.51:30042/report/changeticketstate/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10121}), headers=headers).json()
print(a)

