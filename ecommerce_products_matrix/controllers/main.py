# -*- coding: utf-8 -*-
import re
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo.addons.website_sale_comparison.controllers.main import WebsiteSaleProductComparison
from odoo import fields, http, tools, _
import logging
from werkzeug.exceptions import NotFound

_logger = logging.getLogger(__name__)


class WebsiteAllowUsersProduct(WebsiteSale):
    """ to inherit controllers of eCommerce pages """

    # @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public",
    #             website=True)
    # def old_product(self, product, category='', search='', **kwargs):
    #     current_website = request.website
    #     if product.website_ids and current_website not in product.website_ids:
    #         _logger.warning(
    #             "Access denied: Product '%s' not available on website '%s'. Redirecting to /shop.",
    #             product.display_name, current_website.name
    #         )
    #         raise NotFound()
    #
    #     return super(WebsiteAllowUsersProduct, self).old_product(product=product,
    #                                                              category=category,
    #                                                              search=search, **kwargs)
    #
    # @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    # def product(self, product, category='', search='', **kwargs):
    #     """ Prevent access of product page from public users or wrong website """
    #     current_website = request.website
    #
    #     # 🔒 Check if product belongs to current website (or globally available)
    #     if product.website_ids and current_website not in product.website_ids:
    #         _logger.warning(
    #             "Access denied: Product '%s' not available on website '%s'. Redirecting to /shop.",
    #             product.display_name, current_website.name
    #         )
    #         raise NotFound()
    #     # ✅ Product available → show normally
    #     return super().product(product=product, category=category, search=search, **kwargs)