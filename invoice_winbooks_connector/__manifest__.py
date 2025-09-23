{
    'name': 'invoice winbooks connector',
    'version': '18.0.1.0.0',
    'depends': ['base','account','mail'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
