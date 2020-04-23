# encoding: utf-8
import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
for i in reslist:
    if i['field_key'] == 'to_asset_id':
        assets_id_list =  list(map(int, i['field_value'].split(',')))
    elif i['field_key'] == 'user':
        username_list = i['field_value'].split(',')
    elif i['field_key'] == 'end_time':
        end_time = i['field_value']


class McenterAPI(object):

    def __init__(self):
        self.mcenter_ip = '58.195.98.222'
        self.mcenter_port = 40250
        self.url_v1 = 'v1'
        self.mcenter_username = 'zabbix'
        self.mcenter_password = 'cernet@123'

    def get_headers(self):
        get_token = requests.post(
            'http://{}:{}/{}/api-token-auth/'.format(self.mcenter_ip, self.mcenter_port, self.url_v1),
            data={"username": self.mcenter_username, "password": self.mcenter_password},
        ).json()
        token = get_token['token']
        headers = {
            'Authorization': 'JWT ' + token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            'Content-Type': 'application/json'
        }
        return headers

    def pending(self, asset_esid):  # 待处理事项
        url = 'http://{}:{}/{}/asset/loginfo/?jms=1&asset_esid={}'.format(self.mcenter_ip, self.mcenter_port, self.url_v1, asset_esid)
        pending_list = requests.get(url=url, headers=self.get_headers())
        return pending_list.json()["results"][0]

    def update_pending(self, pending_id, data): # 更新待处理事项
        url = 'http://{}:{}/{}/asset/loginfo/{}/'.format(self.mcenter_ip, self.mcenter_port, self.url_v1, pending_id)
        resp = requests.patch(url=url, data=simplejson.dumps(data), headers=self.get_headers())
        return resp

    def get_userprofile_by_user_name(self, user_name):  # 通过username获取用户信息
        url = 'http://{}:{}/{}/user/user-profile/?search={}'.format(self.mcenter_ip, self.mcenter_port, self.url_v1,
                                                                    user_name)
        resp = requests.get(url=url, headers=self.get_headers())
        return resp.json()["results"][0]

    def get_userprofile_by_name(self, name):  # 通过name获取用户信息
        url = 'http://{}:{}/{}/user/user-profile/?name={}'.format(self.mcenter_ip, self.mcenter_port, self.url_v1, name)
        resp = requests.get(url=url, headers=self.get_headers())
        return resp.json()["results"][0]


mcenter = McenterAPI()


for asset_id in assets_id_list:
    asset = mcenter.pending(asset_id)
    if not asset["temporary_users"]:  # 资产没有临时用户
        users = []
        for username in username_list:
            userprofile = mcenter.get_userprofile_by_user_name(username)
            if userprofile["id"] not in asset["manage_users"]:
                users.append(userprofile["name"] + "-{}".format(end_time))
        if len(users):
            mcenter.update_pending(asset["id"], {"temporary_users": ','.join(users), "is_update": True})
    else:
        users = []
        for username in username_list:
            userprofile = mcenter.get_userprofile_by_user_name(username)
            if (userprofile["id"] not in asset["manage_users"]) and (userprofile["name"] not in asset["temporary_users"]):
                users.append(userprofile["name"] + "-{}".format(end_time))
        if len(users):
            mcenter.update_pending(asset["id"], {"temporary_users": asset["temporary_users"] + ',' + ','.join(users), "is_update": True})
headers = mcenter.get_headers()
requests.patch('http://58.195.98.222:40250/v1/work/changeticketfield/%s/' % (ticket_id),data=simplejson.dumps({"state_id": 10045 ,'state_name':'结束'}), headers=headers)
