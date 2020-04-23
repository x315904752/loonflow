# encoding: utf-8
import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService

mcenter_ip = "10.254.50.230"
mcenter_port = "31001/v1"
username = 'xulei'
password = 'cernet@123'
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
    'Content-Type': 'application/json'
}


def getContent():
    title = "<html><head><meta charset='utf-8'></head><h2 style='text-align: center;'><font face='黑体' style='font - weight: bold;'>技术部工作周报（&nbsp;&nbsp;月第&nbsp;&nbsp;周, 时间范围&nbsp;&nbsp;-&nbsp;&nbsp;）</font></h2>" + \
            "<h3 class='MsoNormal'><font face='等线'>一、本周工作内容</font></h3>" + \
            "<h3 class='MsoNormal'><font face='等线'>二、资料库更新情况</font></h3>" + \
            "<h3 class='MsoNormal'><font face='等线'>三、重点工作推进情况</font></h3>" + \
            "<h3 class='MsoNormal'><font face='等线'>四、内部学习及培训情况</font></h3>" + \
            "<h3 class='MsoNormal'><font face='等线'>五、下周工作计划</font></h3>" + \
            "<h3 class='MsoNormal'><font face='等线'>六、遗留问题及支持情况</font></h3></html>"
    return title

res_list = getContent()
TicketBaseService.update_ticket_custom_field(ticket_id, {"report_forms": str(res_list)})
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '韦东星,徐磊','state_name':'相关人员处理'}), headers=headers)
print(a)
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketstate/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10116}), headers=headers).json()
print(a)

