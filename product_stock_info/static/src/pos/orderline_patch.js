/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { StockInfoPopoverButton } from "@product_stock_info/core/stock_info_popover/stock_info_popover";

patch(Orderline, {
    components: { ...Orderline.components, StockInfoPopoverButton },
});

patch(Orderline.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    async getStockInfoData() {
        const product = this.line.product_id;
        const productTemplate = product?.product_tmpl_id;
        if (!productTemplate) {
            return { error: "no_product" };
        }
        const info = await this.pos.getProductInfo(productTemplate, 1, 0, product);
        const warehouse = info?.productInfo?.warehouses?.[0];
        if (!warehouse) {
            return { error: "no_data" };
        }
        return {
            display_name: product.display_name,
            qty_available: warehouse.available_quantity,
            virtual_available: warehouse.forecasted_quantity,
            free_qty: warehouse.free_qty,
            uom_name: warehouse.uom,
            active: true,
        };
    },
});
