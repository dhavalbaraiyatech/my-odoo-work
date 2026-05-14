/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { browser } from "@web/core/browser/browser";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.VariantAutoCart = publicWidget.Widget.extend({
   selector: '.js_matrix_inputs',

   events: {
      'change .js_matrix_input': '_onQtyChange',
      'click .js_matrix_qty_plus': '_onPlus',
      'click .js_matrix_qty_minus': '_onMinus',
   },

   /**
    * Triggered when a variant quantity input changes.
    */
   async _onQtyChange(ev) {
      const input = ev.currentTarget;
      //        const qty = parseFloat(input.value) || 0;
      const newQty = parseFloat(input.value) || 0;
      const variantId = parseInt(input.dataset.variantId);
      const productTmplId = parseInt(input.dataset.productTmplId);
      const uomId = input.dataset.uomId ? parseInt(input.dataset.uomId) : false;

      if (!variantId) {
         console.warn("No variant ID found for input:", input);
         return;
      }

      // 🧮 Find the hidden <input name="add_qty"> sibling to get old qty
      const hiddenQtyInput = input.closest('.js_matrix_inputs')?.querySelector('input[name="add_qty"]');
      const oldQty = hiddenQtyInput ? parseFloat(hiddenQtyInput.value) || 0 : 0;

      // Calculate how much we actually need to add/remove
      const qtyDiff = newQty - oldQty;

      // Update the hidden input to reflect current quantity
      if (hiddenQtyInput) {
         hiddenQtyInput.value = newQty;
      }

      // If no change, skip RPC
      if (qtyDiff === 0) {
         return;
      }

      try {
         // Call `/shop/cart/add` with "set_qty" mode — forcing cart to match input qty
         const result = await rpc('/shop/cart/add', {
            product_template_id: productTmplId,
            product_id: variantId,
            quantity: qtyDiff,
            uom_id: uomId,
            product_custom_attribute_values: [],
            no_variant_attribute_value_ids: [],
         });

         if (result && result.cart_quantity !== undefined) {
            this._updateCartIcon(result.cart_quantity);

            const $cart = document.querySelector('.my_cart_quantity');
            if ($cart) {
               $cart.textContent = result.cart_quantity;
            }
         }

         if (result.notification_info) {
            this._showCartNotification(result.notification_info);
         }

      } catch (err) {
         console.error("Failed to update variant in cart:", err);
      }
   },

   _onPlus(ev) {
        ev.preventDefault();
        const wrapper = ev.currentTarget.closest('.js_matrix_inputs');
        const input = wrapper.querySelector('.js_matrix_input');

        const max = parseFloat(input.getAttribute('max')) || Infinity;
        let qty = parseFloat(input.value) || 0;

        if (qty < max) {
            input.value = qty + 1;
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    },

    _onMinus(ev) {
        ev.preventDefault();
        const wrapper = ev.currentTarget.closest('.js_matrix_inputs');
        const input = wrapper.querySelector('.js_matrix_input');

        let qty = parseFloat(input.value) || 0;
        if (qty > 0) {
            input.value = qty - 1;
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    },

   /**
    * Updates the cart icon quantity in the header.
    */
   _updateCartIcon(cartQuantity) {
      browser.sessionStorage.setItem('website_sale_cart_quantity', cartQuantity);
      const cartQuantityElements = document.querySelectorAll('.my_cart_quantity');

      for (const el of cartQuantityElements) {
         if (cartQuantity === 0) {
            el.classList.add('d-none');
         } else {
            const cartIcon = document.querySelector('li.o_wsale_my_cart');
            if (cartIcon) cartIcon.classList.remove('d-none');
            el.classList.remove('d-none');
            el.classList.add('o_mycart_zoom_animation');
            setTimeout(() => {
               el.textContent = cartQuantity;
               el.classList.remove('o_mycart_zoom_animation');
            }, 300);
         }
      }
   },

   /**
    * Show a small toast notification when cart is updated.
    */
   _showCartNotification(props, options = {}) {
      if (!this.cartNotificationService) {
         return;
      }

      if (props.lines) {
         this.cartNotificationService.add('', {
            lines: props.lines,
            currency_id: props.currency_id,
            ...options,
         });
      }

      if (props.warning) {
         this.cartNotificationService.add('', {
            warning: props.warning,
            ...options,
         });
      }
   },
});

export default publicWidget.registry.VariantAutoCart;