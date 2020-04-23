# -*- coding: utf-8 -*-
import pexpect
import requests
import simplejson
from service.ticket.ticket_base_service import TicketBaseService

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)

class BackUpStr(object):
    string = ''
    def write(self, s):
        self.string = self.string + s

    def read(self):
        return self.string

    def flush(self):
        pass


def ssh(name, ip, port, passwd, cmd):
    tag_search = BackUpStr()
    res = BackUpStr()
    child = pexpect.spawn('ssh -p%s %s@%s' % (port, name, ip), encoding='utf-8')
    child.logfile_read = tag_search
    i = child.expect(['word', 'yes'], timeout=60)
    if i == 0:
        child.sendline(passwd)
    elif i == 1:
        child.sendline('yes\n')
        child.expect('word')
        child.sendline('%s' % passwd)
    child.expect('>')
    child.sendline('sys')
    child.expect(']')
    child.sendline(cmd)
    child.expect(']')
    child.sendline('quit')
    child.logfile_read = res
    child.expect('>')
    child.sendline('quit')
    child.close()
    return res.read()


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

try:
    token = get_token['token']
except:
    print(get_token)
headers = {
    'Authorization': 'JWT ' + token,
    'Content-Type': 'application/json'
}


# reslist = [{'field_key':'ip_addr', 'field_value':'10.254.40.250'}]
ip_addr_str = ''
for i in reslist:
    if i['field_key'] == 'ip_addr':
        ip_addr_str = str(i['field_value'])
ip_addr = ip_addr_str.split("\r\n")

for i in ip_addr:
    i = i.replace(' ', '')
    cmd = 'ip route-static %s 32 NULL 0 preference 30' %(i)
    ssh('admin', '202.194.96.157','22' , 'Cernet@shandong', cmd)
    ssh('yangxb', '202.194.99.50','12222', 'Cernet@shandong', cmd)

requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束', 'state_id':10051}), headers=headers)


