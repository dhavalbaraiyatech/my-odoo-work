# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.http import request
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import fields, http, tools, _
import logging

_logger = logging.getLogger(__name__)

class WebsiteSaleEpt(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        """Get domain but return variant products instead of templates"""
        domain = super()._get_search_domain(search, category, attrib_values)

        # Replace product.template domain with product.product domain
        domain.append(('product_variant_ids', '!=', False))
        return domain

    def _get_search_order(self, post):
        return super()._get_search_order(post)

    @http.route()
    def shop(self, page=0, category=None, search='', **kw):
        response = super().shop(page, category, search, **kw)

        website = request.website
        # PASS FLAG TO TEMPLATE
        response.qcontext["show_variants_on_shop"] = website.show_variants_on_shop

        if not website.show_variants_on_shop:
            return response

        templates = response.qcontext.get('products')
        if not templates:
            return response

        # Get user country
        user_country = request.env.user.partner_id.country_id

        # Fetch variants of these templates
        variants = request.env["product.product"].search([
            ("product_tmpl_id", "in", templates.ids),
        ])

        # ---- Country Filtering Added Here ----
        def allowed_variant(v):
            """
            Variant allowed if:
                - No country restriction
                - OR user country is in variant.country_ids
            """
            if not v.country_ids:
                return True
            return user_country in v.country_ids

        filtered_variants = variants.filtered(lambda v: allowed_variant(v))

        # Replace context products
        response.qcontext["products"] = filtered_variants

        # --- FIX BINS HERE ---
        ppg = response.qcontext.get("ppg")
        ppr = response.qcontext.get("ppr")

        new_bins = self._compute_variant_bins(filtered_variants, ppg, ppr)

        response.qcontext["bins"] = new_bins

        return response

    # ---- Custom bins generator for variants ----
    def _compute_variant_bins(self, variants, ppg, ppr):
        """
        Variants do not have template grid info, so default to x=1, y=1.
        This function generates the same structure TableCompute produces.
        """
        bins = []
        row = []

        for index, variant in enumerate(variants):
            row.append({
                "product": variant,
                "x": 1,  # column width
                "y": 1,  # row height
            })

            # If row is filled or end of list, push it
            if len(row) == ppr:
                bins.append(row)
                row = []

        # Push last row if any
        if row:
            bins.append(row)

        return bins
