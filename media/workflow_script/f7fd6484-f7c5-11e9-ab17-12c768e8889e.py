#!/usr/bin/python
# encoding: utf-8
import requests
import time
import pdfkit
import simplejson
from service.ticket.ticket_base_service import TicketBaseService

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    if i['field_key'] == 'report_forms':
        week_str = str(i['field_value'])
    if i['field_key'] == 'email':
        #receivers = str(i['field_value'])+',1124874950@qq.com,948838865@qq.com'
        #print(receivers)
        receivers = 'shigk@cernet.com,yangxb@cernet.com,1124874950@qq.com,948838865@qq.com'
    if i['field_key'] == 'title':
        week_title = str(i['field_value'])

name = int(time.time())
username = 'xulei'
password = 'cernet@123'
week_str = week_str.replace('<td>', '<td style="border: 1px solid #ccc;">').replace('<th>', '<th style="border: 1px solid #ccc;">')
x = "/media/"
if x in week_str:
    a = week_str.replace(x, "http://10.254.50.100/media/")
    week_str = a
#try:
#    pdfkit.from_string(week_str, "/opt/loonflow/media/workflow_script/" + str(name) + ".pdf")
#except:
#    pass
print(week_str)
pdfkit.from_string(week_str, "/opt/loonflow/media/workflow_script/" + str(name) + ".pdf")

token = requests.post("http://10.254.50.230:31001/v1/api-token-auth/",
                data={"username": username, "password": password}).json()['token']
headers = {
    'Authorization': 'JWT ' + token,
}
data = {
    'receivers': receivers,
    'from': '3467992173@qq.com',
    'title': week_title,
    'content': ' '
}
#files = {'file': open('/opt/loonflow/media/workflow_script/1572577319.pdf', 'rb')}
files = {'file': open('/opt/loonflow/media/workflow_script/' + str(name) + '.pdf', 'rb')}
resp = requests.post(url='http://10.254.50.230:31001/v1/api/send-mail/', data=data, files=files, headers=headers)
headers['Content-Type'] = 'application/json'
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '','state_name':'结束'}), headers=headers)

a = requests.patch('http://10.254.50.230:31001/v1/work/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '','state_name':'结束'}), headers=headers)
