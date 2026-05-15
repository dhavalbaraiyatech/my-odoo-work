/** @odoo-module **/

import {messageActionsRegistry} from "@mail/core/common/message_actions";
import {_t} from "@web/core/l10n/translation";

messageActionsRegistry.add("highlight-message", {
    condition: (component) => !!component.props.message.id,
    icon: (component) =>
        component.props.message.is_pinned
            ? "fa fa-thumb-tack o-PinnedAction-active"
            : "fa fa-thumb-tack",
    title: (component) =>
        component.props.message.is_pinned ? _t("Unpin Message") : _t("Pin Message"),
    onClick: (component) => {
        component.props.message.toggleHighlight();
    },
    sequence: 15,
});



