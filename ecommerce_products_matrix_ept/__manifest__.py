# __manifest__.py
{
    'name': 'eCommerce Products Matrix',
    'version': '1.0.0',
    'summary': '####',
    'category': 'Website',
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'license': 'OPL-1',
    'depends': ['website', 'website_sale', 'website_sale_stock'],
    'data': [
        'views/templates.xml',
        'views/variant_templates.xml',
        # 'views/product_template.xml',
        'views/product_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ecommerce_products_matrix_ept/static/src/js/variant_cart_autoupdate.js',
            'ecommerce_products_matrix_ept/static/src/js/variant_change.js',
        ],
    },
    'installable': True,
    'application': False,
}
