# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_default_shipping_from_partner(self, partner):
        """
        Return the default shipping address partner for a given customer partner.
        Checks the customer's delivery contacts for one marked as default.
        """
        if not partner:
            return partner
        commercial = partner.commercial_partner_id
        default_addr = self.env['res.partner'].search([
            ('commercial_partner_id', '=', commercial.id),
            ('is_default_shipping_address', '=', True),
            ('type', 'in', ['delivery', 'other', 'contact']),
            ('id', '!=', commercial.id),
        ], limit=1)
        if not default_addr:
            # Check if the commercial partner itself is marked as default
            if commercial.is_default_shipping_address:
                default_addr = commercial
        return default_addr or partner

    def _cart_add(self, product_id, quantity=1.0, *, uom_id=None, **kwargs):
        """
        Override to auto-assign the default shipping address when a product
        is first added to a website cart (order is just being created).
        """
        res = super()._cart_add(product_id, quantity, uom_id=uom_id, **kwargs)
        partner = self.partner_id
        if partner and partner != self.env.ref('base.public_partner', raise_if_not_found=False):
            default_shipping = self._get_default_shipping_from_partner(partner)
            if default_shipping and self.partner_shipping_id != default_shipping:
                self.write({'partner_shipping_id': default_shipping.id})
        return res
