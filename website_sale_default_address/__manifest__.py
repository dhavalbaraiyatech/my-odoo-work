# -*- coding: utf-8 -*-
{
    'name': 'Website Sale - Default Shipping Address',
    'version': '19.0.1.0.0',
    'category': 'Website/eCommerce',
    'summary': 'Allows customers to set a default shipping address on the website checkout.',
    'description': """
        This module adds a "Set as Default" button on the website shipping address
        selection page. When a customer marks an address as default, all future orders
        will pre-select that address automatically. The customer can still override it
        by clicking any other address during checkout.
    """,
    'author': 'Dhaval Baraiya',
    'maintainer': 'https://dhavalbaraiya.odoo.com/',
    'website': 'https://dhavalbaraiya.odoo.com/',
    'depends': [
        'website_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/website_sale_default_address_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_default_address/static/src/css/default_address.css',
            'website_sale_default_address/static/src/js/default_address.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
