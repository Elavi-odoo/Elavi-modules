{
    'name': 'invoice email connector',
    'version': '16.0.1.0.0',
    'depends': ['base','account','mail'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'wizard/account_invoice_send_views_wizard.xml'

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
