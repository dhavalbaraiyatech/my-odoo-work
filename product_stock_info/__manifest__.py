# -*- coding: utf-8 -*-
{
    'name': 'Product Stock Info Popover',
    'version': '19.0.1.0.0',
    'category': 'Warehouse',
    'summary': 'Reusable Info icon widget showing On Hand, Forecasted and Free to Use quantities for a product.',
    'description': """
Product Stock Info Popover
===========================
Adds a small, reusable Info (i) icon that can be dropped into any
product-related view. Clicking the icon opens a lightweight popover showing:

* On Hand quantity (qty_available)
* Forecasted quantity (virtual_available)
* Free to Use quantity (free_qty)

Enabled out of the box on:

* Sale Order Lines (list and form)
* Product list/tree view (product.product and product.template)
* Point of Sale product grid and order lines
    """,
    'author': 'Dhaval Baraiya.',
    'website': 'https://dhavalbaraiya.odoo.com/',
    'license': 'OPL-1',

    # 'sale_stock' is required explicitly (rather than relying on its
    # auto_install) because the "warehouse_id" field it adds to
    # sale.order.line is a hard dependency of the widget on that view.
    'depends': ['stock', 'sale', 'sale_stock', 'point_of_sale'],

    'data': [
        'views/sale_order_views.xml',
        'views/product_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'product_stock_info/static/src/core/stock_info_popover/stock_info_popover.js',
            'product_stock_info/static/src/core/stock_info_popover/stock_info_popover.xml',
            'product_stock_info/static/src/core/stock_info_popover/stock_info_popover.scss',
            'product_stock_info/static/src/widgets/stock_info_widget.js',
            'product_stock_info/static/src/widgets/stock_info_widget.xml',
        ],
        'point_of_sale._assets_pos': [
            'product_stock_info/static/src/core/stock_info_popover/stock_info_popover.js',
            'product_stock_info/static/src/core/stock_info_popover/stock_info_popover.xml',
            'product_stock_info/static/src/core/stock_info_popover/stock_info_popover.scss',
            'product_stock_info/static/src/pos/product_card_patch.js',
            'product_stock_info/static/src/pos/product_card_patch.xml',
            'product_stock_info/static/src/pos/orderline_patch.js',
            'product_stock_info/static/src/pos/orderline_patch.xml',
        ],
    },

    'installable': True,
    'auto_install': False,
    'application': False,
}
