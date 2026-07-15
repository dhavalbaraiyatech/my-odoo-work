# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_default_shipping_address = fields.Boolean(
        string='Default Shipping Address',
        default=False,
        help='If checked, this address will be auto-selected as the shipping '
             'address during website checkout.',
    )

    def write(self, vals):
        res = super().write(vals)
        if vals.get('is_default_shipping_address'):
            self._enforce_single_default_shipping_address()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        defaults = partners.filtered('is_default_shipping_address')
        if defaults:
            defaults._enforce_single_default_shipping_address()
        return partners

    def _enforce_single_default_shipping_address(self):
        """
        Ensure at most one default shipping address per commercial partner.
        Called whenever `is_default_shipping_address` is set to True, whether
        through the website checkout action or a manual edit on the res.partner
        form, so the two paths can never disagree.
        """
        for partner in self:
            if not partner.is_default_shipping_address:
                continue
            others = self.search([
                ('commercial_partner_id', '=', partner.commercial_partner_id.id),
                ('is_default_shipping_address', '=', True),
                ('id', '!=', partner.id),
            ])
            if others:
                others.write({'is_default_shipping_address': False})

    def _get_default_shipping_address(self):
        """
        Return the default shipping address for the commercial partner.
        Looks for a child delivery contact with is_default_shipping_address=True.
        Falls back to None if none is set.
        """
        self.ensure_one()
        commercial = self.commercial_partner_id
        return self.search([
            ('commercial_partner_id', '=', commercial.id),
            ('is_default_shipping_address', '=', True),
            ('type', 'in', ['delivery', 'other', 'contact']),
            ('id', '!=', commercial.id),
        ], limit=1) or self.search([
            ('id', '=', commercial.id),
            ('is_default_shipping_address', '=', True),
        ], limit=1)

    def action_set_default_shipping_address(self):
        """
        Set this partner as the default shipping address for its commercial partner.
        `write()` takes care of unsetting any previously set default within the
        same commercial partner family.
        """
        self.ensure_one()
        self.write({'is_default_shipping_address': True})
        return True

    def action_unset_default_shipping_address(self):
        """
        Unset this partner as the default shipping address.
        """
        self.ensure_one()
        self.write({'is_default_shipping_address': False})
        return True
