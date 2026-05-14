/** @odoo-module **/

import { localization } from '@web/core/l10n/localization';
import publicWidget from "@web/legacy/js/public/public_widget";
import { insertThousandsSep } from '@web/core/utils/numbers';
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { markup } from '@odoo/owl';

publicWidget.registry.VariantImageChanger = publicWidget.Widget.extend({
   selector: '.js_matrix_inputs',

   events: {
        'change .variant_qty_input': '_onVariantClick',
        'click .variant_qty_input': '_onVariantClick',
    },

   /**
    * Triggered when user clicks on a variant (radio button or attribute value)
    */
   async _onVariantClick(ev) {
      const target = ev.currentTarget;
      const $product = target.closest('.js_product');

      if (!$product) return;

      const productTemplateId = parseInt($product.querySelector('.product_template_id')?.value || 0);
      const parent = ev.target.closest('.js_product');
      const productId = parseInt(parent.querySelector('.product_id')?.value || 0);


      // Collect selected attribute value IDs
      const selectedInputs = $product.querySelectorAll('input.js_variant_change:checked, select.js_variant_change');

      const combination = JSON.parse(target.dataset.ptavIds)

      if (!productTemplateId || !productId) {
         console.warn("Missing product_template_id or product_id");
         return;
      }

      parseInt(parent.querySelector('.product_id').value);

      try {
         // ✅ Correct v19 combination info RPC call
         const combinationInfo = await rpc('/website_sale/get_combination_info', {
            product_template_id: productTemplateId,
            product_id: productId,
            combination: combination,
            add_qty: 1,
            uom_id: false,
            context: {},
         });


         if (combinationInfo && combinationInfo.product_id) {
            this._onChangeCombination(ev, parent, combinationInfo);
            //                this._updateProductImage($product, combinationInfo);
         }

      } catch (err) {
         console.error("Error fetching combination info:", err);
      }
   },

   _onChangeCombination(ev, parent, combination) {
      const isCombinationPossible = !!combination.is_combination_possible;
      const precision = combination.currency_precision;
      const productPrice = parent.querySelector('.product_price');
      if (productPrice && !productPrice.classList.contains('decimal_precision')) {
         productPrice.classList.add('decimal_precision');
         productPrice.dataset.precision = precision;
      }
      const pricePerUom = parent.querySelector('.o_base_unit_price')
         ?.querySelector('.oe_currency_value');
      if (pricePerUom) {
         const hasPrice = isCombinationPossible && combination.base_unit_price !== 0;
         pricePerUom.closest('.o_base_unit_price_wrapper').classList.toggle('d-none', !hasPrice);
         if (hasPrice) {
            pricePerUom.textContent = this._priceToStr(combination.base_unit_price, precision);
            const unit = parent.querySelector('.oe_custom_base_unit');
            if (unit) {
               unit.textContent = combination.base_unit_name;
            }
         }
      }

      // Triggers a new JS event with the correct payload, which is then handled
      // by the google analytics tracking code.
      // Indeed, every time another variant is selected, a new view_item event
      // needs to be tracked by google analytics.
      if ('product_tracking_info' in combination) {
         const product = document.querySelector('#product_detail');
         product.dispatchEvent(
            new CustomEvent('view_item_event', {
               'detail': combination['product_tracking_info']
            })
         );
      }
      const addToCart = parent.querySelector('#add_to_cart_wrap');
      const contactUsButton = parent.closest('#product_details')
         ?.querySelector('#contact_us_wrapper');
      const quantity = parent.querySelector('.css_quantity');
      const productUnavailable = parent.querySelector('#product_unavailable');

      const preventSale = combination.prevent_zero_price_sale;
      productPrice?.classList?.toggle('d-inline-block', !preventSale);
      productPrice?.classList?.toggle('d-none', preventSale);
      quantity?.classList?.toggle('d-inline-flex', !preventSale);
      quantity?.classList?.toggle('d-none', preventSale);
      addToCart?.classList?.toggle('d-inline-flex', !preventSale);
      addToCart?.classList?.toggle('d-none', preventSale);
      contactUsButton?.classList?.toggle('d-none', !preventSale);
      contactUsButton?.classList?.toggle('d-flex', preventSale);
      productUnavailable?.classList?.toggle('d-none', !preventSale);
      productUnavailable?.classList?.toggle('d-flex', preventSale);

      if (contactUsButton) {
         const contactUsButtonLink = contactUsButton.querySelector('a');
         const url = contactUsButtonLink.getAttribute('data-url');
         contactUsButtonLink.setAttribute('href', `${url}?subject=${combination.display_name}`);
      }

      const price = parent.querySelector('.oe_price')?.querySelector('.oe_currency_value');
      const defaultPrice = parent.querySelector('.oe_default_price')
         ?.querySelector('.oe_currency_value');
      const comparePrice = parent.querySelector('.oe_compare_list_price');
      if (price) {
         price.textContent = this._priceToStr(combination.price, precision);
      }
      if (defaultPrice) {
         defaultPrice.textContent = this._priceToStr(combination.list_price, precision);
         defaultPrice.closest('.oe_website_sale').classList
            .toggle('discount', combination.has_discounted_price);
         defaultPrice.parentElement.classList
            .toggle('d-none', !combination.has_discounted_price);
      }
      if (comparePrice) {
         comparePrice.classList.toggle('d-none', combination.has_discounted_price);
      }

      //        this._toggleDisable(parent, isCombinationPossible);

      // update images & tags only when changing product
      // or when either ids are 'false', meaning dynamic products.
      // Dynamic products don't have images BUT they may have invalid
      // combinations that need to disable the image.
      if (!combination.no_product_change) {
         this._updateProductImage(
            parent.closest('tr.js_product, .oe_website_sale'), combination.carousel
         );
         const productTags = parent.querySelector('.o_product_tags');
         productTags?.insertAdjacentHTML('beforebegin', markup(combination.product_tags));
         productTags?.remove();
      }

      const productIdInput = parent.querySelector('.product_id');
      productIdInput.value = combination.product_id || 0;
      productIdInput.dispatchEvent(new Event('change', {
         bubbles: true
      }));

      //        this.handleCustomValues(ev.target);
   },

   _updateProductImage(productContainer, newImages) {
      let images = productContainer.querySelector(this._getProductImageContainerSelector());
      // When using the web editor, don't reload this or the images won't
      // be able to be edited depending on if this is done loading before
      // or after the editor is ready.
      if (images) {
         images.insertAdjacentHTML('beforebegin', markup(newImages));
         images.remove();

         // Re-query the latest images.
         images = productContainer.querySelector(this._getProductImageContainerSelector());
         // Update the sharable image (only work for Pinterest).
         const shareImageSrc = images.querySelector('img').src;
         document.querySelector('meta[property="og:image"]')
            .setAttribute('content', shareImageSrc);

         //            if (images.id === 'o-carousel-product') {
         //                window.Carousel.getOrCreateInstance(images).to(0);
         //            }
         //            this._startZoom();
      }
   },

   _getProductImageContainerSelector() {
      return {
         'carousel': "#o-carousel-product",
         'grid': "#o-grid-product",
      } [this._getProductImageLayout()];
   },
   _getProductImageLayout() {
      return document.querySelector("#product_detail_main").dataset.image_layout;
   },
   _priceToStr: function (price, precision) {
      if (!Number.isInteger(precision)) {
         precision = parseInt(
            this.el.querySelector('.decimal_precision:last-of-type')?.dataset.precision ?? 2
         );
      }
      const formatted = price.toFixed(precision).split('.');
      const {
         thousandsSep,
         decimalPoint,
         grouping
      } = localization;
      formatted[0] = insertThousandsSep(formatted[0], thousandsSep, grouping);
      return formatted.join(decimalPoint);
   },
});

export default publicWidget.registry.VariantImageChanger;