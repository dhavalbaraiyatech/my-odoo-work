from odoo import models, fields
from odoo.addons.mail.tools.discuss import Store


class MailMessage(models.Model):
    _inherit = 'mail.message'

    is_pinned = fields.Boolean(string='Highlighted', default=False)

    def _to_store(self, store: Store, /, **kwargs):
        """Override to include is_pinned (highlight) state in message store data."""
        super()._to_store(store, **kwargs)
        for message in self:
            store.add(message, {'is_pinned': message.is_pinned})
