{
    'name': 'Chatter Message Pin & Highlight',
    'version': '18.0.0.1',
    'summary': 'Pin messages in chatter — shows a Pinned Messages panel with Jump-to functionality',
    'category': 'Tools',
    'author': 'Dhaval Baraiya.',
    'maintainer': 'https://dhavalbaraiya.odoo.com/',
    'website': 'https://dhavalbaraiya.odoo.com/',
    'depends': ['mail'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            # Models / store patches
            'chatter_message_pin_and_highlight/static/src/models/message_model_patch.js',
            'chatter_message_pin_and_highlight/static/src/models/message_patch.js',
            'chatter_message_pin_and_highlight/static/src/models/highlight_action.js',
            # Pinned panel component
            'chatter_message_pin_and_highlight/static/src/components/pinned_panel.js',
            'chatter_message_pin_and_highlight/static/src/components/pinned_panel.xml',
            # Chatter patch (registers component + extends template)
            'chatter_message_pin_and_highlight/static/src/components/chatter_patch.js',
            'chatter_message_pin_and_highlight/static/src/xml/chatter_extend.xml',
            # Styles
            'chatter_message_pin_and_highlight/static/src/css/message.css',
        ],
    },

    'installable': True,
    'application': False,
}
