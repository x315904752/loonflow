# -*- coding: utf-8 -*-
from service.ticket.ticket_base_service import TicketBaseService


reslist, flag = TicketBaseService.get_ticket_base_filed_list(ticket_id)

username = ''
for i in reslist:
    if '_hbg' in i['field_key']:
        username = str(i['field_value'])
user_list = username.split(',')
for user in user_list:
    TicketBaseService.add_ticket_relation(ticket_id, user)
