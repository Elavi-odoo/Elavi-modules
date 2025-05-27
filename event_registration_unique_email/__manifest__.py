{
    'name': 'event registration unique email',
    'version': '17.0.1.0.0',
    'depends': ['base', 'website_sale', 'website_event', 'event'],
    'data': [
        'views/website_event_templates.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'event_registration_unique_email/static/src/js/event_registration_unique_email.js',
        ],
    },
    'installable': True,
    'application': True,
}
