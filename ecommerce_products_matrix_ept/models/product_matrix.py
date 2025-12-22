import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    country_ids = fields.Many2many('res.country', string='Countries')
    # website_ids = fields.Many2many(
    #     'website',
    #     string="Websites",
    #     help="Restrict visibility of this product to selected websites countries."
    # )