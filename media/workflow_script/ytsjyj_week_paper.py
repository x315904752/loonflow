import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService


headers = {}


class WeekPaper(object):
    def __init__(self, url='http://10.254.50.230:31001/v1/', project=27):
        self.url = url
        self.project = project
        self.username = 'xulei'
        self.password = 'cernet@123'

    def getToken(self):
        url = self.url + 'api-token-auth/'
        data = {
            'v_code': 1,
            'username': self.username,
            'password': self.password
        }
        resp = requests.post(url=url, data=data).json()['token']
        return resp

    def getContent(self, day_start, day_end):
        content = "<html><head><meta charset='utf-8'></head><h2 style='text-align: center;'><font face='黑体' style='font - weight: bold;'>烟台市教育局运维简报</font></h2>"+ \
                  "<h3><span style='font-size: large;'>本周重要工作：</span></h3>"
        url = self.url + 'work/ticketslist/'
        token = 'JWT' + ' ' + self.getToken()
        global headers
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        data = {
            'page': 1,
            'page_size': 1000,
            'search': [
                {'key': "to_project_id", 'action': "eq", 'value': 27},
                {'key': "gmt_created", 'action': "gt", 'value': day_start},
                {'key': "gmt_created", 'action': "lt", 'value': day_end}
            ]
        }
        data = simplejson.dumps(data)
        resp = requests.post(url=url, headers=headers, data=data).json()['results']
        start = 0
        worktitle_str = ""
        for work_flow in resp:
            start += 1
            worktitle_str += ("<p class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<face='等线'>" + str(start) + "、" + work_flow['title'] + "</p>")
        return content + worktitle_str + "</html>"

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    if i['field_key'] == 'start_time':
        start_time = str(i['field_value'])
    elif i['field_key'] == 'end_time':
        end_time = str(i['field_value'])
week = WeekPaper()
res_list = week.getContent(start_time, end_time)
TicketBaseService.update_ticket_custom_field(ticket_id, {"report_forms": str(res_list)})
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '张善存,徐磊','state_name':'相关人员处理'}), headers=headers)
print(a)
a = requests.patch('http://10.254.50.230/31001/v1/report/changeticketstate/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10111}), headers=headers).json()
print(a)

