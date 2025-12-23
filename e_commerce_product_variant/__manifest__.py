{
    'name': 'E-commerce product variant',
    'version': '19.0.0.0.1',
    'category': 'Sale',
    'summary': 'This module allows to display product varaint in website shop page instanded of product template.',
    'description': """E-commerce product variant module allows to display product varaint in website shop page instanded of product template. 
    This module is useful when you have products with multiple variants and you want to showcase each variant separately on your e-commerce website.
    """,
    'author': 'Dhaval Baraiya.',
    'maintainer': 'https://dhavalbaraiya.odoo.com/',
    'website': 'https://dhavalbaraiya.odoo.com/',
    'depends': ['ecommerce_products_matrix_ept'],
    'data': [
        'views/website.xml',
        'views/templates.xml',
        'views/product_tile_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
