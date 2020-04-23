# -*- coding: utf-8 -*-
import os
import time
import random
import base64
import urllib.request
import json
import urllib
import requests
from Crypto.Cipher import AES, DES3

mcenter_url = os.environ.get('mcenter_url', None)


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


url = mcenter_url + '/setting/setting-wechat/'
work_url = mcenter_url + '/alarm/alarm/'
user_url = mcenter_url + '/user/user-profile/?to_user__username='


class Wechat(object):
    def __init__(self, AgentId, CropID, Secret, url):
        self.AgentId = AgentId
        self.CropID = CropID
        self.Secret = Secret
        self.url = url

    def send_text_card(self, title, description, touser, ticket_id):
        gurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (self.CropID, self.Secret)
        result = urllib.request.urlopen(urllib.request.Request(gurl)).read()
        dict_result = json.loads(result)
        gtoken = dict_result['access_token']
        purl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % gtoken
        post_data = {}
        msg_content = dict()
        msg_content['title'] = title
        msg_content['description'] = description
        msg_content['url'] = self.url + ticket_id
        post_data['touser'] = touser
        post_data['msgtype'] = 'textcard'
        post_data['agentid'] = self.AgentId
        post_data['textcard'] = msg_content
        jsonpost_data = json.dumps(post_data, ensure_ascii=False).encode(encoding='UTF8')
        res = urllib.request.Request(purl, jsonpost_data)
        response = urllib.request.urlopen(res)
        print(response.read())


headers = {
    'jms-timestamp-authkey': get_authkey(),
    'Content-Type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

ticket_mc = requests.request(method="GET", url=work_url + str(last_flow_log['ticket_id']), headers=headers).json()
ticket_mc = ticket_mc['data']['value']
alarm_level_option = {"0":"未分类","1":"信息","2":"警告","3":"一般严重","4":"严重","5":"灾难"}

# if ticket_mc['state_id'] == 10245:
if True:
    project_id = ticket_mc['to_project']['id']
    params = {'to_project':project_id}
    wechat_list = requests.request(method="GET", url=url, params=params, headers=headers).json()
    ip_addr = ''
    alarm_level = ''
    event_status = ''
    alarm_id = ''
    duty_member = ''
    for i in ticket_mc['field_list']:
        if i['field_key'] == 'host_ip':
            ip_addr = i['field_value']
        elif i['field_key'] == 'event_level':
            alarm_level = alarm_level_option[i['field_value']]
        elif i['field_key'] == 'waring_status':
            event_status = i['field_value']
        elif i['field_key'] == 'event_id':
            alarm_id = str(i['field_value'])
        elif i['field_key'] == 'handler' and i['field_value']:
            user_mc = requests.request(method="GET", url=user_url + i['field_value'], headers=headers).json()
            duty_member = user_mc['results'][0]['name']

    description = """告警内容: {}
告警时间: 【{}】
主机地址: 【{}】
告警等级: 【{}】
当前状态: 【{}】
告警编号: 【{}】
值班人员: 【{}】""".format(ticket_mc['title'], ticket_mc['gmt_created'], ip_addr, alarm_level, event_status, alarm_id, duty_member)
    if len(wechat_list):
        wechat_info = wechat_list[0]
        wechat = Wechat(AgentId=wechat_info['AgentId'],
                        CropID=wechat_info['CropID'],
                        Secret=wechat_info['Secret'],
                        url=wechat_info['url']+'/ticket-detail/?alarm_id=')
        for name in ticket_mc['participant'].split(','):
            user_mc = requests.request(method="GET", url=user_url + name, headers=headers).json()
            user_wechat = user_mc['results'][0]['wechat']
            wechat.send_text_card(title='您有新的待处理告警',
                                  description=description,
                                  touser=user_wechat,ticket_id=str(last_flow_log['ticket_id']))
