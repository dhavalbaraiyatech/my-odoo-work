# -*- coding: utf-8 -*-
from odoo import api, models


def _read_stock_info(product):
    """Build the payload consumed by the "Stock Info" popover widget.

    `product` is a single-record product.product or product.template. Both
    models expose qty_available / virtual_available with the same semantics
    (computed from stock.quant / stock.move, context-aware on warehouse_id,
    location, etc.); on product.template these are already the sum over all
    of the template's variants (see stock's `_compute_quantities`).

    `free_qty`, however, is only ever defined on product.product - there is
    no such field on product.template - so for a template it is derived by
    summing `free_qty` over its variants (mirroring how qty_available /
    virtual_available are themselves aggregated for templates). Reading
    `product.free_qty` directly on a product.template record raises, which
    is why the popover previously failed for templates only.
    """
    if product._name == 'product.template':
        free_qty = sum(product.product_variant_ids.mapped('free_qty'))
    else:
        free_qty = product.free_qty
    return {
        'display_name': product.display_name,
        'qty_available': product.qty_available,
        'virtual_available': product.virtual_available,
        'free_qty': free_qty,
        'uom_name': product.uom_id.display_name,
        'active': product.active,
    }


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def get_stock_info_popover_data(self, product_id, warehouse_id=False):
        """Return On Hand / Forecasted / Free to Use quantities for one product variant.

        Called from the JS "Stock Info" popover widget (Sale Order Lines,
        Product list view). `exists()` is used instead of a search domain so
        archived products are still found; the `active` flag lets the widget
        warn the user instead of silently failing.
        """
        product = self.browse(product_id).exists()
        if not product:
            return {'error': 'not_found'}
        if warehouse_id:
            product = product.with_context(warehouse_id=warehouse_id)
        return _read_stock_info(product)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def get_stock_info_popover_data(self, product_id, warehouse_id=False):
        """Same as ProductProduct.get_stock_info_popover_data, for template-level views."""
        product = self.browse(product_id).exists()
        if not product:
            return {'error': 'not_found'}
        if warehouse_id:
            product = product.with_context(warehouse_id=warehouse_id)
        return _read_stock_info(product)
