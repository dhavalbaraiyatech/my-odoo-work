# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_line_header(self):
        """Overwrite this method for display product name with sku in website cart page"""
        if not self.product_template_attribute_value_ids:
            return self.name_short
        # not display_name because we don't want the combination name or the code.
        if self.product_id.default_code:
            return f"{self.product_id.name} \u2014 SKU: {self.product_id.default_code}"
        return self.product_id.name
