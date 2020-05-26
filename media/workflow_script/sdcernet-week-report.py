# encoding: utf-8
import sys, os
import requests
import simplejson
import time, datetime
import re
from service.ticket.ticket_base_service import TicketBaseService
from jinja2 import Environment, FileSystemLoader
import json
from Crypto.Cipher import AES, DES3
from multiprocessing import Pool
import requests
import simplejson
import datetime
import base64
import random
import time
import json
import sys


def password_to_str(password):
    """
    加密
    :param password:
    :return:
    """

    def add_to_16(password):
        while len(password) % 16 != 0:
            password += '\0'
        return str.encode(password)  # 返回bytes

    key = 'saierwangluo'  # 密钥
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化aes加密器
    des3 = DES3.new(add_to_16(key), DES3.MODE_ECB)  # 初始化3des加密器
    # aes加密
    encrypted_text = str(
        base64.encodebytes(
            aes.encrypt(add_to_16(password))), encoding='utf8'
    ).replace('\n', '')
    des_encrypted_text = str(
        base64.encodebytes(des3.encrypt(add_to_16(encrypted_text))), encoding='utf8'
    ).replace('\n', '')  # 3des加密
    # 返回加密后数据
    return des_encrypted_text


def get_authkey():
    random_num1 = random.randrange(128, 256)
    random_num2 = random.randrange(256, 512)
    now = time.time()
    pw = '{}-{}-{}'.format(random_num1, now, random_num2)
    return password_to_str(pw)


headers = {
    'jms-timestamp-authkey': get_authkey(),
    'Content-Type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}


def conversion_time(start_time, end_time):
    """
       字符串转换时间
    """
    time_t1 = datetime.datetime.strptime("{}".format(start_time),
                                         "%Y-%m-%dT%H:%M:%S" if 'T' in start_time else "%Y-%m-%d %H:%M:%S")
    time_t2 = datetime.datetime.strptime("{}".format(end_time),
                                         "%Y-%m-%dT%H:%M:%S" if 'T' in end_time else "%Y-%m-%d %H:%M:%S")
    total_time = (time_t2 - time_t1).total_seconds()  # （秒）数

    return total_time


def link_visit_state(ip_addr, port, start_time, end_time):
    """
    	报表
    """
    rep_lk = requests.request(method='get',
                              url='http://{0}:{1}/v1/asset/net-flow-network-card/?to_net_flow_asset__to_net_flow_node__to_project=20&page=1&search=bps&page_size=20'.format(
                                  ip_addr, port), headers=headers)

    final_results = {}  # 最后返回结果
    totals_times = conversion_time(start_time, end_time)  # 总时间（秒）数

    for lnk in ['link', 'visit']:
        link_visit_data = []  # 存储数据
        outage_time = 0  # 中断 异常 持续时间
        query_criteria = [
            {'search': [{'key': "gmt_created", 'action': "gte", 'value': "{}".format(start_time)},
                        {'key': "new_end_time", 'action': "lte", 'value': "{}".format(end_time)},
                        {'key': "to_project_name", 'action': "eq", 'value': '"山东教育网省网运维"'}], "page": 1,
             "page_size": 10000},
            {'search': [{'key': "gmt_created", 'action': "lte", 'value': "{}".format(start_time)},
                        {'key': "new_end_time", 'action': "gte", 'value': "{}".format(start_time)},
                        {'key': "new_end_time", 'action': "lte", 'value': "{}".format(end_time)},
                        {'key': "to_project_name", 'action': "eq", 'value': '"山东教育网省网运维"'}], "page": 1,
             "page_size": 10000},
            {'search': [{'key': "gmt_created", 'action': "gte", 'value': "{}".format(start_time)},
                        {'key': "gmt_created", 'action': "lte", 'value': "{}".format(end_time)},
                        {'key': "new_end_time", 'action': "gte", 'value': "{}".format(end_time)},
                        {'key': "to_project_name", 'action': "eq", 'value': '"山东教育网省网运维"'}], "page": 1,
             "page_size": 10000},
            {'search': [{'key': "gmt_created", 'action': "lte", 'value': "{}".format(start_time)},
                        {'key': "new_end_time", 'action': "gte", 'value': "{}".format(end_time)},
                        {'key': "to_project_name", 'action': "eq", 'value': '"山东教育网省网运维"'}], "page": 1,
             "page_size": 10000}
        ]
        for index, value in enumerate(query_criteria):
            if lnk == 'link':
                value['search'].append({'key': 'title', 'action': 'eq', 'value': '"链路中断"'})
            else:
                value['search'].append({'key': 'title', 'action': 'eq', 'value': '"访问异常"'})

            search_info_link = simplejson.dumps(value)
            resp_link = requests.request(method='post', url='http://%s:%s/v1/alarm/alarmlist/' % (ip_addr, port),
                                         data=search_info_link, headers=headers)

            for value in json.loads(resp_link.text)["results"]:
                link_visit_data.append({"title": value.get("title", ""), "gmt_created": value.get("gmt_created", ""),
                                        "duration": value.get("duration", ""),
                                        "end_time": value.get("new_end_time", ""),
                                        "results ": value.get("results", "")})

                if index == 0:
                    outage_time += conversion_time(value.get("gmt_created", ""), value.get("new_end_time", ""))
                elif index == 1:
                    outage_time += conversion_time(start_time, value.get("new_end_time", ""))
                elif index == 2:
                    outage_time += conversion_time(value.get("gmt_created", ""), end_time)
                elif index == 3:
                    outage_time += conversion_time(start_time, end_time)

        final_results[lnk] = link_visit_data
        if lnk == 'link':
            final_results["{}_availability".format(lnk)] = format(
                (totals_times - outage_time / json.loads(rep_lk.text)['count']) / totals_times * 100, '.2f')
        else:
            final_results["{}_availability".format(lnk)] = format(
                (totals_times - outage_time / 112) / totals_times * 100, '.2f')
    return final_results


# 链路中断 和 访问异常 报表【山东教育网省网运维】
ip_addr = '10.254.50.230'
port = '31001'

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    if i['field_key'] == 'start_time':
        start_time = i['field_value']
    elif i['field_key'] == 'end_time':
        end_time = i['field_value']



def generate_html(data):
    env = Environment(loader=FileSystemLoader('/opt/loonflow/media/workflow_script/templates'))  # 加载模板
    template = env.get_template('cernet-week-report.html')
    return template.render(data=data)

TicketBaseService.update_ticket_custom_field(ticket_id, {"report_forms": str(generate_html(link_visit_state(ip_addr, port, start_time, end_time)))})
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketfield/%s/' % (ticket_id), data=simplejson.dumps({"participant": '', 'state_name': '结束'}), headers=headers)
print(a)
a = requests.patch('http://10.254.50.230:31001/v1/report/changeticketstate/%s/' % (ticket_id), data=simplejson.dumps({"state_id": 10260}), headers=headers).json()
print(a)
