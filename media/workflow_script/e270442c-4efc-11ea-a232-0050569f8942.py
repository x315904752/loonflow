# encoding: utf-8
import nmap
import sys
import requests
import simplejson

from service.ticket.ticket_base_service import TicketBaseService

def nmap_A_scan(network_prefix):
    nm = nmap.PortScanner()
    # 配置nmap扫描参数
    scan_raw_result = nm.scan(hosts=network_prefix, arguments='-sT -Pn -F -v -n -A ')
    print(scan_raw_result)
    # 分析扫描结果
    result_list = [['ip', 'os', 'port', 'name', 'product', 'version', 'cpe', 'script']]
    for host, result in scan_raw_result['scan'].items():
        os = ''
        if result['status']['state'] == 'up':
            try:
               os = result['osmatch'][0]['name']
            except:
                pass
            try:
                for port in result['tcp']:
                    if result['tcp'][port]['state'] == 'open':
                        try:
                            result_list.append([
                                host,
                                os,
                                port,
                                result['tcp'][port].get('name', ''),
                                result['tcp'][port].get('product', ''),
                                result['tcp'][port].get('version', ''),
                                result['tcp'][port].get('cpe', ''),
                                result['tcp'][port].get('script', ''),
                            ])
                        except:
                            pass
            except:
                pass
    return result_list


mcenter_ip = "10.254.50.54"
mcenter_port = "32045"
username = 'root'
password = '123456a?'

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

reslist, flag = TicketBaseService.get_ticket_base_field_list(ticket_id)
data = {}
ip = ''
for i in reslist:
    if i['field_key'] == 'ip':
        ip = str(i['field_value'])
        break

result_data = nmap_A_scan(ip)
TicketBaseService.update_ticket_custom_field(ticket_id, {"result": simplejson.dumps(result_data)})
print(result_data)
headers['Content-Type'] = 'application/json'
a = requests.patch('http://%s:%s/work/changeticketfield/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({'state_name':'结束'}), headers=headers).json()
print(a)
a = requests.patch('http://%s:%s/work/changeticketstate/%s/' % (mcenter_ip, mcenter_port, ticket_id),data=simplejson.dumps({"state_id": 7}), headers=headers).text
print(a)

