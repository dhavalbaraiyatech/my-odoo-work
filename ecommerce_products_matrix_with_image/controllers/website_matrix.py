from odoo import http
from odoo.http import request


class WebsiteProductMatrix(http.Controller):

    @http.route(['/shop/get_web_matrix'], type='jsonrpc', auth='public', website=True)
    def get_web_matrix(self, product_id, parent_combination=None, **kwargs):
        """Return matrix data for the given product template."""
        product = request.env['product.template'].browse(int(product_id))
        if not product.exists():
            return {}

        matrix = request.env['sale.order']._get_web_matrix(product, parent_combination)
        return {'matrix': matrix}
