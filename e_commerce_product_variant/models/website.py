# -*- coding: utf-8 -*-

import base64
import json
import werkzeug.urls
from urllib.parse import urlparse, parse_qs, urlencode

from odoo.osv import expression
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.addons.auth_oauth.controllers.main import OAuthLogin


class Website(models.Model):
    _inherit = "website"

    show_variants_on_shop = fields.Boolean(
        string="Show Variants in Shop Page",
        help="Enable this to display product variants instead of product templates on the shop page.",
        default=False
    )
