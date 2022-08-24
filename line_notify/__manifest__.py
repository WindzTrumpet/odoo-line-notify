# -*- coding: utf-8 -*-
{
    'name': "LINE Notify",
    'summary': "Line Notify Integration",
    'author': "WindzTrumpet",
    'website': "https://github.com/WindzTrumpet/odoo-line-notify",
    'category': 'Line/Notify',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/line_notify_user_views.xml',
        'views/res_settings_config_views.xml',
    ],
    'application': True,
}
