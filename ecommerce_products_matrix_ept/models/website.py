# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    # def _search_with_fuzzy(self, search_type, search, limit, order, options):
    #     res = super()._search_with_fuzzy(search_type, search, limit,
    #                                      order, options)
    #     # 'res' is a tuple: (count, details_list, fuzzy_term)
    #     if not res or not isinstance(res, tuple):
    #         return res
    #
    #     count, details_list, fuzzy_term = res
    #     current_website = request.website
    #
    #     if current_website and details_list:
    #         new_details_list = []
    #         for detail in details_list:
    #             results = detail.get("results")
    #             if results:
    #                 filtered_results = results.filtered(
    #                     lambda p:
    #                     not hasattr(p, "website_ids")  # category or other types
    #                     or not p.website_ids  # product with no website restriction
    #                     or current_website in p.website_ids
    #                 )
    #                 # filtered_results = results.filtered(
    #                 #     lambda p: not p.website_ids or current_website in p.website_ids
    #                 # )
    #                 # Update count accordingly
    #                 detail["results"] = filtered_results
    #                 detail["count"] = len(filtered_results)
    #             new_details_list.append(detail)
    #
    #         # Recalculate total count
    #         total_count = sum(len(d.get("results", [])) for d in new_details_list)
    #         return (total_count, new_details_list, fuzzy_term)
    #
    #     return res
