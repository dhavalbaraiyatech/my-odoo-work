from odoo import http
from odoo.http import request


class DiscussController(http.Controller):

    @http.route('/mail/message/toggle_pin', type='json', auth='user')
    def toggle_pin(self, message_id):
        """
        Toggle the 'is_pinned' field for the given message.
        """
        message = request.env['mail.message'].browse(message_id)
        if not message.exists():
            return {'error': 'Message not found'}

        # Toggle the pin state
        message.is_pinned = not message.is_pinned
        return {'is_pinned': message.is_pinned}
