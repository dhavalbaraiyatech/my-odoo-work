/** @odoo-module **/

import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';
import { rpc } from '@web/core/network/rpc';

/**
 * Handles the "Set as Default" / "Remove Default" button on delivery address
 * cards, both on /shop/checkout and on the portal's /my/addresses page.
 *
 * The checkout page's own `website_sale.checkout` interaction listens for
 * clicks on `.card` to change the selected address, so our buttons must stop
 * propagation (like the core `.js_edit_address` link does) before doing
 * their own RPC call.
 */
export class DefaultShippingAddress extends Interaction {
    static selector = '#shop_checkout, .o_portal_addresses';
    dynamicContent = {
        '.o_wsda_set_default': { 't-on-click.stop.prevent': this.onSetDefault },
        '.o_wsda_remove_default': { 't-on-click.stop.prevent': this.onRemoveDefault },
    };

    async onSetDefault(ev) {
        const partnerId = ev.currentTarget.dataset.partnerId;
        await this.waitFor(rpc('/shop/set_default_shipping_address', { address_id: partnerId }));
        window.location.reload();
    }

    async onRemoveDefault(ev) {
        const partnerId = ev.currentTarget.dataset.partnerId;
        await this.waitFor(rpc('/shop/unset_default_shipping_address', { address_id: partnerId }));
        window.location.reload();
    }
}

registry
    .category('public.interactions')
    .add('website_sale_default_address.default_shipping', DefaultShippingAddress);