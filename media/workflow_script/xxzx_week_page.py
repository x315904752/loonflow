import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService


headers = {}
class WeekPaper(object):
    def __init__(self, url='http://10.254.50.230:31001/v1/', project=1):
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

    def getTitle(self):
        title = "<html><head><meta charset='utf-8'></head><h2 style='text-align: center;'><font face='黑体' style='font - weight: bold;'>山东省教育数据中心运维简报</font></h2>" + \
                "<h2><font face='等线' style='font-weight: bold;'>一、数据中心状态展示</font></h2><h3 class='MsoNormal'><font face='等线'>（一）重要业务运行时间</font></h3>" + \
                "<h3 class='MsoNormal'><font face='等线'>（二）出口流量</font></h3>" + \
                "<h3 class='MsoNormal'><font face='等线'>（三）主要业务系统（基于百度统计和应用负载设备）</font></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>1、edu.shandong.gov.cn</span></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>2、sdei.edu.cn访问情况</span></h3>" + \
                "<h3 class='MsoNormal'><font face='等线'>（四）主要业务系统（基于迪普链路负载出口设备）</font></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>1、迪普出口链路负载设备-一师一优课业务流量情况</span></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>2、迪普出口链路负载设备-其他业务流量情况</span></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>3、综合素质评价并发数</span></h3>" + \
                "<h3 class='MsoNormal'><font face='等线'>（五）至政务云万兆专线</font></h3>" + \
                "<h3 class='MsoNormal'><font face='等线'>（六）服务器及存储运行情况</font></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>1、深信服超融合虚拟化系统（二期设备正在施工中）</span></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>2、VMware虚拟化系统（运行正常）</span></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>3、EMC存储（已更换vplex上的失效sps电池模块）</span></h3>" + \
                "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>4、宏杉存储（运行正常）</span></h3>" + \
                "<h3 class='MsoNormal'><font face='等线'>（七）主要数据库运行情况</font></h3>" \
                "<table border='0' width='100%' cellpadding='0' cellspacing='0'><tbody>" + \
                "<tr><th>业务系统\数据库信息</th><th>数据库版本</th><th>机器名</th><th>虚拟IP地址</th><th>CPU使用情况</th><th>内存使用情况</th><th>共享存储使用情况</th><th>巡检过程中出现的问题</th><th>解决方案</th></tr>" + \
                "<tr><td>学前教育数据库</td><td>11.2.0.4.0</td><td>xqdb1-xqdb2</td><td>172.16.1.143/144</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为1T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>中职系统数据库</td><td>11.2.0.4.0</td><td>zzdb1-zzdb2</td><td>172.16.1.103/104</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为1T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>"  + \
                "<tr><td>应用支撑系统数据库</td><td>12.1.0.2.0</td><td>yyzcdb1-yyzcdb2</td><td>172.16.1.163/164</td><td>空闲率：%</td><td>内存总量为15G，内存剩余量为</td><td>共享存储总量为512G，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>学生资助系统数据库</td><td>11.2.0.1.0</td><td>rac1-rac2</td><td>172.16.1.123/124</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为2T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>基础数据系统数据库</td><td>12.1.0.2.0</td><td>JCSJRac1-JCSJRac2</td><td>172.16.1.185/186</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为1T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>教师系统数据库</td><td>12.1.0.1.0</td><td>jsywrac1-jsywrac2</td><td>172.16.1.205/206</td><td>空闲率：%</td><td>内存总量为129G，内存剩余量为</td><td>共享存储总量为1T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>全国校舍系统数据库</td><td>10.2.0.4.0</td><td>Xiaoshe_1-Xiaoshe_2</td><td>172.16.1.225/226</td><td>空闲率：%</td><td>内存总量为16G，内存剩余量为</td><td>共享存储总量为2T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>综合素质评价系统数据库</td><td>11.2.0.4.0</td><td>zhszdb1-zhszdb2</td><td>172.16.3.84/85</td><td>空闲率：%</td><td>内存总量为616G，内存剩余量为</td><td>共享存储总量为4T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>体质健康系统数据库</td><td>12.1.0.2.0</td><td>tcdbrac_1-tcdbrac_2</td><td>172.16.3.4/5</td><td>空闲率：%</td><td>内存总量为64G，内存剩余量为</td><td>共享存储总量为1T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>教育厅网站系统数据库</td><td>12.1.0.2.0</td><td>jytwebdb1-jytwebdb2</td><td>172.16.3.43/44</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为409G，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>大班额系统数据库</td><td>12.1.0.2.0</td><td>DBERAC1-DBERAC2</td><td>172.16.3.63/64</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为512G，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>山东基教系统数据库</td><td>11.2.0.4.0</td><td>sdbe-db-01/02/03/04</td><td>172.16.148.245/246/247/248</td><td>空闲率：%</td><td>内存总量为512G，内存剩余量为</td><td>共享存储总量为8T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>山东省特殊教育管理信息系统数据库</td><td>12.2.0.1.0</td><td>TSJY-RAC2-TSJY-RAC1</td><td>172.16.3.53/54</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为512G，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>山东云平台系统数据库（1）</td><td>12.1.0.2.0</td><td>sdcdb1-sdcdb2</td><td>172.16.3.25/26</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为512G，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>山东云平台系统数据库（2）</td><td>12.1.0.2.0</td><td>SDYPT-DataMana-Db3-SDYPT-DataMana-Db4</td><td>172.16.3.35/36</td><td>空闲率：%</td><td>内存总量为32G，内存剩余量为</td><td>共享存储总量为1T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>联通省学籍系统数据库</td><td>11.2.0.4.0</td><td>sdbe-exch-ora-rac1-sdbe-exch-ora-rac2</td><td>172.16.148.182/183</td><td>空闲率：%</td><td>内存总量为64G，内存剩余量为</td><td>共享存储总量为3T，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr>" + \
                "<tr><td>行走齐鲁系统数据库</td><td>11.2.0.4.0</td><td>sdbe-exch-ora-rac1-sdbe-exch-ora-rac2</td><td>172.16.3.107/108</td><td>空闲率：%</td><td>内存总量为129G，内存剩余量为</td><td>共享存储总量为511G，共享存储总量剩余量为</td><td>巡检过程无发现问题</td><td></td></tr></tbody></table>"
        return title

    def getContent(self, day_start, day_end):
        content = "<h3 class='MsoNormal'><font face='等线'>（八）环控系统运行情况</font></h3>" + \
                  "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>1、机房设备总用电电流、功率周截图-A路</span></h3>" + \
                  "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>2、 机房设备总用电电流、功率周截图-B路</span></h3>" + \
                  "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>3、主机房温湿度周曲线图</span></h3>" + \
                  "<h3 class='MsoNormal'>&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-size: large;'>4、接入间温湿度周曲线图</span></h3>" + \
                  "<h2><font face='等线' style='font-weight: bold;'>二、工作内容(总工作量&nbsp;&nbsp;起)</font></h2>"
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
                {'key': "to_project_id", 'action': "eq", 'value': 1},
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
        footer = "<h2><font face='等线' style='font-weight: bold;'>三、下一步工作计划</font></h2></html>"
        return content + worktitle_str + footer

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    if i['field_key'] == 'start_time':
        start_time = str(i['field_value'])
    elif i['field_key'] == 'end_time':
        end_time = str(i['field_value'])
week = WeekPaper()
res_list = week.getTitle() + week.getContent(start_time, end_time)
TicketBaseService.update_ticket_custom_field(ticket_id, {"report_forms": str(res_list)})
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '范振岐,于纪欢,王东东,王承哲,路行腾,刘荣海,徐磊,毛建波','state_name':'相关人员处理'}), headers=headers)
print(a)
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketstate/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10106}), headers=headers).json()
print(a)

