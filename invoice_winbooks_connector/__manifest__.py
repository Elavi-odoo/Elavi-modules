{
    'name': 'invoice_winbooks_connector',
    'version': '18.0.1.0.0',
    'depends': ['base','account','mail'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/account_journal_views.xml',
        'views/action_send_winbooks_email.xml',
    ],
    'installable': True,
    'application': True,
}
