# encoding: utf-8
import sys, os
import requests
import simplejson
import time, datetime
import re
from service.ticket.ticket_base_service import TicketBaseService
from jinja2 import Environment, FileSystemLoader
import json

data = {
    'link': [
        {
            'title': '【101.4.116.246-山东省教育网-济南S7706】山东教育网济南S7706-5/0/5-山东协和学院链路中断',
            'gmt_created': '2020-04-26T13: 05: 53',
            'duration': '3小时00分钟06秒',
            'end_time': '2020-04-2616: 05: 59',
            'results': '线路中断'
        },
        {
            'title': '【101.4.116.246-山东省教育网-济南S7706】山东教育网济南S7706-5/0/18-山东外事翻译大学链路中断',
            'gmt_created': '2020-04-26T10: 45: 44',
            'duration': '4小时45分钟18秒',
            'end_time': '2020-04-2615: 31: 02',
            'results': '线路中断'
        }
    ],
    'visit': [
        {
            'title': '【山东青年政治学院-首页-www.sdyu.edu.cn】【http: //www.sdyu.edu.cn】访问异常',
            'gmt_created': '2020-04-26T23: 52: 00',
            'duration': '0小时16分钟01秒',
            'end_time': '2020-04-2700: 08: 01',
            'results': ''
        },
        {
            'title': '【山东劳动职业技术学院-首页-www.sdlvtc.edu.cn】【http: //www.sdlvtc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T23: 40: 00',
            'duration': '7小时25分钟09秒',
            'end_time': '2020-04-2707: 05: 09',
            'results': ''
        },
        {
            'title': '【济宁学院-首页-www.jnxy.edu.cn】【http: //www.jnxy.edu.cn】访问异常',
            'gmt_created': '2020-04-26T23: 09: 59',
            'duration': '7小时55分钟09秒',
            'end_time': '2020-04-2707: 05: 08',
            'results': ''
        },
        {
            'title': '【济宁医学院-首页-www.jnmc.edu.cn】【http: //www.jnmc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T23: 06: 58',
            'duration': '7小时56分钟11秒',
            'end_time': '2020-04-2707: 03: 09',
            'results': ''
        },
        {
            'title': '【潍坊工程职业学院-首页-www.wfec.cn】【http: //www.wfec.cn】访问异常',
            'gmt_created': '2020-04-26T22: 09: 59',
            'duration': '8小时50分钟06秒',
            'end_time': '2020-04-2707: 00: 05',
            'results': ''
        },
        {
            'title': '【威海海洋职业学院-首页-www.whovc.edu.cn】【http: //www.whovc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T22: 08: 59',
            'duration': '8小时55分钟09秒',
            'end_time': '2020-04-2707: 04: 08',
            'results': ''
        },
        {
            'title': '【莱芜职业技术学院-首页-www.lwvc.edu.cn】【http: //www.lwvc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T14: 33: 56',
            'duration': '0小时04分钟58秒',
            'end_time': '2020-04-2614: 38: 54',
            'results': ''
        },
        {
            'title': '【莱芜职业技术学院-首页-www.lwvc.edu.cn】【http: //www.lwvc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T14: 03: 56',
            'duration': '0小时05分钟00秒',
            'end_time': '2020-04-2614: 08: 56',
            'results': ''
        },
        {
            'title': '【莱芜职业技术学院-首页-www.lwvc.edu.cn】【http: //www.lwvc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T13: 38: 56',
            'duration': '0小时05分钟00秒',
            'end_time': '2020-04-2613: 43: 56',
            'results': ''
        },
        {
            'title': '【山东协和学院-首页-www.sdxiehe.edu.cn】【http: //www.sdxiehe.edu.cn】访问异常',
            'gmt_created': '2020-04-26T12: 59: 55',
            'duration': '3小时04分钟00秒',
            'end_time': '2020-04-2616: 03: 55',
            'results': '链路中断'
        },
        {
            'title': '【山东农业工程学院-首页-www.sdaeu.edu.cn】【http: //www.sdaeu.edu.cn】访问异常',
            'gmt_created': '2020-04-26T12: 13: 55',
            'duration': '0小时04分钟59秒',
            'end_time': '2020-04-2612: 18: 54',
            'results': ''
        },
        {
            'title': '【莱芜职业技术学院-首页-www.lwvc.edu.cn】【http: //www.lwvc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T10: 13: 52',
            'duration': '0小时25分钟00秒',
            'end_time': '2020-04-2610: 38: 52',
            'results': ''
        },
        {
            'title': '【莱芜职业技术学院-首页-www.lwvc.edu.cn】【http: //www.lwvc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T08: 38: 51',
            'duration': '0小时04分钟58秒',
            'end_time': '2020-04-2608: 43: 49',
            'results': ''
        },
        {
            'title': '【莱芜职业技术学院-首页-www.lwvc.edu.cn】【http: //www.lwvc.edu.cn】访问异常',
            'gmt_created': '2020-04-26T08: 23: 48',
            'duration': '0小时05分钟03秒',
            'end_time': '2020-04-2608: 28: 51',
            'results': ''
        },
        {
            'title': '【山东青年政治学院-首页-www.sdyu.edu.cn】【http: //www.sdyu.edu.cn】访问异常',
            'gmt_created': '2020-04-26T00: 37: 45',
            'duration': '5小时31分钟05秒',
            'end_time': '2020-04-2606: 08: 50',
            'results': ''
        },
        {
            'title': '【山东理工职业学院-首页-www.sdpu.edu.cn】【http: //www.sdpu.edu.cn】访问异常',
            'gmt_created': '2020-04-26T00: 11: 43',
            'duration': '6小时12分钟07秒',
            'end_time': '2020-04-2606: 23: 50',
            'results': ''
        },
        {
            'title': '【山东协和学院-首页-www.sdxiehe.edu.cn】【http: //www.sdxiehe.edu.cn】访问异常',
            'gmt_created': '2020-04-26T00: 10: 43',
            'duration': '5小时59分钟07秒',
            'end_time': '2020-04-2606: 09: 50',
            'results': ''
        }
    ]
}


def generate_html(data):
    env = Environment(loader=FileSystemLoader('./templates'))  # 加载模板
    template = env.get_template('cernet-week-report.html')
    return template.render(data=data)

TicketBaseService.update_ticket_custom_field(ticket_id, {"report_forms": str(generate_html(data))})
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '', 'state_name': '结束'}), headers=headers)
print(a)
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketstate/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10260}), headers=headers).json()
print(a)
