# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductAttributeValus(models.Model):
    _inherit = 'product.attribute.value'

    country_ids = fields.Many2many('res.country', string='Countries',
                                   help="Countries where this attribute value is available")

    # ------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._recompute_variant_countries()
        return records

    # ------------------------------------------------------------
    # WRITE (add / remove countries)
    # ------------------------------------------------------------
    def write(self, vals):
        res = super().write(vals)
        if 'country_ids' in vals:
            self._recompute_variant_countries()
        return res

    # ------------------------------------------------------------
    # UNLINK (attribute value deleted)
    # ------------------------------------------------------------
    def unlink(self):
        # Collect affected variants BEFORE delete
        variants = self._get_related_variants()
        res = super().unlink()
        if variants:
            variants._recompute_countries_from_attributes()
        return res

    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------
    def _get_related_variants(self):
        return self.env['product.product'].search([
            ('product_template_attribute_value_ids.product_attribute_value_id', 'in', self.ids)
        ])

    def _recompute_variant_countries(self):
        variants = self._get_related_variants()
        variants._recompute_countries_from_attributes()
