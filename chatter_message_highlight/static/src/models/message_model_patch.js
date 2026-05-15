/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Message } from "@mail/core/common/message_model";
import { Record } from "@mail/core/common/record";
import { rpc } from "@web/core/network/rpc";

patch(Message.prototype, {
    setup() {
        super.setup();
        /** @type {boolean} */
        this.is_pinned = Record.attr(false);
    },
    async toggleHighlight() {
        const result = await rpc("/mail/message/toggle_pin", {
            message_id: this.id,
        });
        if (result && "is_pinned" in result) {
            this.is_pinned = result.is_pinned;
        }
    },
});

