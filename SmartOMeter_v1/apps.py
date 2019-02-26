from django.contrib.admin.apps import AdminConfig


class SmartAdminConfig(AdminConfig):
    default_site = 'SmartOMeter_v1.admin.SmartAdminSite'
