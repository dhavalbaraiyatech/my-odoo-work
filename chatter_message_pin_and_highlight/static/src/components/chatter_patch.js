/** @odoo-module **/

import { Chatter } from "@mail/chatter/web_portal/chatter";
import { PinnedMessagesPanel } from "@chatter_message_pin_and_highlight/components/pinned_panel";
import { patch } from "@web/core/utils/patch";

// Register the PinnedMessagesPanel component so it can be used in the Chatter template
Object.assign(Chatter.components, { PinnedMessagesPanel });

// Extend Chatter state to control the pinned panel visibility
patch(Chatter.prototype, {
    setup() {
        super.setup(...arguments);
        Object.assign(this.state, {
            showPinnedMessages: true,
        });
    },

    togglePinnedMessages() {
        this.state.showPinnedMessages = !this.state.showPinnedMessages;
    },
});

