{
    'name': 'Chatter Message Highlight',
    'version': '18.0.0.1',
    'summary': 'Adds a highlight button to chatter messages to toggle yellow background',
    'category': 'Tools',
    'depends': ['mail'],
    'author': 'Dhaval Baraiya.',
    'maintainer': 'https://dhavalbaraiya.odoo.com/',
    'website': 'https://dhavalbaraiya.odoo.com/',
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'chatter_message_highlight/static/src/models/message_model_patch.js',
            'chatter_message_highlight/static/src/models/message_patch.js',
            'chatter_message_highlight/static/src/models/highlight_action.js',
            'chatter_message_highlight/static/src/css/message.css',
        ],
    },

    'installable': True,
    'application': False,
}
