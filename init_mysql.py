# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./loonflow")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.pro")
django.setup()

from django.contrib.auth.hashers import make_password
from apps.account.models import LoonUser, LoonDept, AppToken


admin_user = LoonUser.objects.filter(username='admin')
if not len(admin_user):
    # init sql
    LoonUser.objects.create(
        username='admin',
        alias='管理员',
        email='admin@mcenter.com',
        password=make_password('Cernet@2020'),
        is_admin=True
    )
    LoonDept.objects.create(
        id=3,
        name='资产管理员',
        leader='admin',
        approver='admin',
        creator='admin',
    )
    AppToken.objects.create(
        id=1,
        app_name='all',
        token='7816f554-f380-11e8-be96-0242ac110002',
        ticket_sn_prefix='loonflow',
        creator='admin',
    )
    AppToken.objects.create(
        id=2,
        app_name='alarm',
        token='7816f554-f380-11e8-be96-0242ac110002',
        ticket_sn_prefix='alarm',
        creator='admin',
    )
    AppToken.objects.create(
        id=3,
        app_name='report',
        token='7816f554-f380-11e8-be96-0242ac110002',
        ticket_sn_prefix='report',
        creator='admin',
    )
    AppToken.objects.create(
        id=4,
        app_name='asset',
        token='7816f554-f380-11e8-be96-0242ac110002',
        ticket_sn_prefix='asset',
        creator='admin',
    )