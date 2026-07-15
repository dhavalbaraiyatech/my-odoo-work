# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDefaultAddress(WebsiteSale):

    @http.route(
        '/shop/set_default_shipping_address',
        type='jsonrpc',
        auth='user',
        website=True,
        methods=['POST'],
    )
    def set_default_shipping_address(self, address_id, **kwargs):
        """
        Set an address as the customer's default shipping address.
        Called via RPC from the frontend JS.

        :param address_id: int - ID of the res.partner to mark as default
        :return: dict with success flag and message
        """
        partner = request.env['res.partner'].sudo().browse(int(address_id))

        # Security: ensure the address belongs to the current user's commercial partner
        current_partner = request.env.user.partner_id
        if not partner.exists():
            return {'success': False, 'error': 'Address not found.'}

        if partner.commercial_partner_id.id != current_partner.commercial_partner_id.id:
            return {'success': False, 'error': 'Access denied.'}

        partner.action_set_default_shipping_address()

        # Also update the current cart's shipping address if a cart is open
        order = request.cart
        if order:
            order.write({'partner_shipping_id': partner.id})

        return {
            'success': True,
            'address_id': partner.id,
            'message': 'Default shipping address updated.',
        }

    @http.route(
        '/shop/unset_default_shipping_address',
        type='jsonrpc',
        auth='user',
        website=True,
        methods=['POST'],
    )
    def unset_default_shipping_address(self, address_id, **kwargs):
        """
        Remove the default flag from an address.

        :param address_id: int - ID of the res.partner to unmark
        :return: dict with success flag
        """
        partner = request.env['res.partner'].sudo().browse(int(address_id))
        current_partner = request.env.user.partner_id

        if not partner.exists():
            return {'success': False, 'error': 'Address not found.'}

        if partner.commercial_partner_id.id != current_partner.commercial_partner_id.id:
            return {'success': False, 'error': 'Access denied.'}

        partner.action_unset_default_shipping_address()
        return {'success': True, 'address_id': partner.id}