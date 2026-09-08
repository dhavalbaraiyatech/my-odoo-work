/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { StockInfoPopoverButton } from "@product_stock_info/core/stock_info_popover/stock_info_popover";

patch(ProductCard, {
    components: { ...ProductCard.components, StockInfoPopoverButton },
});

patch(ProductCard.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    /**
     * Reuses the POS' own product-info lookup (product.template's
     * get_product_info_pos, exposed client-side as pos.getProductInfo)
     * instead of a new endpoint: it already returns available_quantity,
     * free_qty and forecasted_quantity per warehouse, warehouse-scoped and
     * consistent with the rest of the POS UI.
     *
     * `<ProductCard product="product"/>` (see product_screen.xml) is fed
     * with product.template records, not variants: `this.props.product` IS
     * the template already, unlike on Orderline where `line.product_id` is
     * a product.product variant exposing its own `product_tmpl_id`. No
     * specific variant is known yet at this grid stage, so it is left
     * unset (getProductInfo then reports on the template's first/default
     * variant).
     */
    async getStockInfoData() {
        const productTemplate = this.props.product;
        if (!productTemplate) {
            return { error: "no_product" };
        }
        const info = await this.pos.getProductInfo(productTemplate, 1, 0, false);
        const warehouse = info?.productInfo?.warehouses?.[0];
        if (!warehouse) {
            return { error: "no_data" };
        }
        return {
            display_name: productTemplate.display_name,
            qty_available: warehouse.available_quantity,
            virtual_available: warehouse.forecasted_quantity,
            free_qty: warehouse.free_qty,
            uom_name: warehouse.uom,
            active: true,
        };
    },
});
