# encoding: utf-8

import sys, django, os
from pyzabbix import ZabbixAPI
from service.ticket.ticket_base_service import TicketBaseService


class Zabbix(object):
    def __init__(self):
        self.ip = "221.214.92.94"
        self.port = "8888"
        self.username = "admin"
        self.password = "X2iparp.com"
        self.url = "/zabbix/"
    def login(self):
        ZABBIX_SERVER = 'http://%s:%s%s' % (self.ip, self.port, self.url)
        zapi = ZabbixAPI(ZABBIX_SERVER)
        zapi.login(self.username, self.password)
        return zapi



try:
    zapi = Zabbix().login()
except:
    pass


def gain_zabbix(value):
    """
    """

    traffic = []
    received_data = zapi.item.get(
        output="extend",
        itemids= value
        )
    if len(received_data):
         traffic.append({"itemid": received_data[0]["itemid"],"lastvalue": received_data[0]["lastvalue"]})

    return traffic

def pt_loonflow(params):
    """
    """
    res = dict()
    dcsj ={"xxzx_12_xjjg":118380 ,"xxzx_9_wlzj":118381 ,"xxzx_9_ccsb":118382 ,"xxzx_9_xnj":118383}
    for p in params:
        if p in dcsj.keys():
            tre =gain_zabbix(dcsj[p])
            res[p] = tre[0]["lastvalue"]

    return res


reslist,flag = TicketBaseService.get_ticket_base_filed_list(ticket_id)
params = list()
for d in reslist:
    params.append(d['field_key'])
res_dict = pt_loonflow(params)
TicketBaseService.update_ticket_custom_field(ticket_id,res_dict)
