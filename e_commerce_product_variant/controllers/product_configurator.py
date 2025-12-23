# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import request, route

from odoo.addons.sale.controllers.product_configurator import SaleProductConfiguratorController
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleProductConfiguratorController(SaleProductConfiguratorController, WebsiteSale):

    @route(
        route='/website_sale/should_show_product_configurator',
        type='jsonrpc',
        auth='public',
        website=True,
        readonly=True,
    )
    def website_sale_should_show_product_configurator(
            self, product_template_id, ptav_ids, is_product_configured
    ):
        """
        OVERRIDE:
        - If website.show_variants_on_shop is enabled → ALWAYS return False.
        - Otherwise → return default Odoo behavior using super().
        """
        website = request.website
        # If shop displays variants, disable configurator popup
        if website.show_variants_on_shop:
            return False
        else:
            return super().website_sale_should_show_product_configurator(
                product_template_id,
                ptav_ids,
                is_product_configured
            )
