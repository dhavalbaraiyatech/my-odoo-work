/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Message } from "@mail/core/common/message";

patch(Message.prototype, {
    get attClass() {
        return {
            ...super.attClass,
            "o-mail-Message-highlighted": this.message.is_pinned,
        };
    },
});

