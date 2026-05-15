/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { url } from "@web/core/utils/urls";

/**
 * Displays a collapsible "Pinned Messages" section in the chatter.
 * Each item shows avatar, author, date, body snippet and a "Jump" button on hover
 * that scrolls + highlights the original message in the thread.
 */
export class PinnedMessagesPanel extends Component {
    static template = "chatter_message_pin_and_highlight.PinnedMessagesPanel";
    static props = ["thread"];

    setup() {
        super.setup();
        this.state = useState({ open: true });
    }

    /** @returns {import("models").Message[]} */
    get pinnedMessages() {
        return (this.props.thread.messages ?? []).filter((m) => m.is_pinned);
    }

    toggle() {
        this.state.open = !this.state.open;
    }

    /**
     * Scroll to and highlight the given message in the thread.
     * @param {import("models").Message} message
     */
    async jumpToMessage(message) {
        await this.env.messageHighlight?.highlightMessage(message, this.props.thread);
    }

    /**
     * Return the avatar image URL for a message's author.
     * @param {import("models").Message} msg
     * @returns {string}
     */
    getAvatarUrl(msg) {
        if (msg.author?.id) {
            return url(`/web/image/res.partner/${msg.author.id}/avatar_128`);
        }
        return "/web/static/img/user_menu_avatar.png";
    }

    /**
     * Strip HTML tags from message body to get plain text preview.
     * @param {string} html
     * @returns {string}
     */
    getBodyText(html) {
        if (!html) return "";
        const div = document.createElement("div");
        div.innerHTML = html;
        const text = div.textContent || div.innerText || "";
        const trimmed = text.trim();
        return trimmed.length > 120 ? trimmed.substring(0, 120) + "…" : trimmed;
    }
}

