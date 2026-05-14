import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    country_ids = fields.Many2many('res.country', string='Countries')

    website_ids = fields.Many2many(
        'website',
        string="Websites",
        help="Restrict visibility of this product to selected websites countries."
    )

    # def _recompute_countries_from_attributes(self):
    #     """
    #     Variant country_ids = union of all attribute value countries
    #     """
    #     for variant in self:
    #         attribute_values = variant.product_template_attribute_value_ids.mapped(
    #             'product_attribute_value_id'
    #         )
    #
    #         countries = attribute_values.mapped('country_ids')
    #
    #         variant.country_ids = [(6, 0, countries.ids)]
