# -- encoding: utf-8 --

{
    'name': 'Personal Notes',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Simple personal notes',
    'depends': ['base'],
    'data': [
        'security/res_groups.xml',
        "security/ir.model.access.csv",
        'views/personal_notes_views.xml',
        'views/res_partner_views.xml',
        'data/personal_cron.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'personal_notes/static/src/css/kanban_colors.css',
        ],
    },
    'installable': True,
    'application': True,
}
