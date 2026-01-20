# -*- coding: utf-8 -*-
{
    # App Information
    'name': "Dynamic Price List Fields",
    'category': 'Sales',
    'version': '17.0.0.0.1',
    'summary': 'This module allows us to dynamically display the pricelist values applied to products. It introduces a '
               'new column showing the pricelist name and also applies the corresponding discount values..',
    'license': 'OPL-1',

    # Author
    'author': "Dhaval Baraiya.",
    'website': 'https://dhavalbaraiya.odoo.com/',
    'maintainer': 'Dhaval Baraiya.',

    # Dependencies
    "depends": ["product"],

    # Views
    'data': [
        'views/product_template_view.xml',
    ],

    # Technical
    'installable': True,
    'auto_install': False,
    'application': False,
    'active': False,
}
