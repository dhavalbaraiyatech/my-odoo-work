/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { StockInfoPopoverButton } from "@product_stock_info/core/stock_info_popover/stock_info_popover";

/**
 * Reusable "stock info" widget: <widget name="stock_info_widget"/>.
 *
 * Works out of the box in two kinds of views:
 *  - Views whose record IS a product (product.product / product.template
 *    list & form views, e.g. the Product list view): the record's own id is
 *    used as the product id.
 *  - Views whose record references a product variant through a many2one
 *    field (e.g. `product_id` on sale.order.line): the name of that field is
 *    passed in through widget options, e.g.
 *    `<widget name="stock_info_widget" options="{'product_field': 'product_id'}"/>`.
 *    If the field isn't set yet (e.g. a section/note line, or a line where
 *    only the template has been picked so far), the icon simply doesn't
 *    render.
 *
 * An optional `warehouse_field` option (same idea) points to a many2one
 * field on the record that scopes the quantities to a specific warehouse,
 * e.g. `warehouse_id` on sale.order.line.
 *
 * Odoo 19's relational model exposes many2one field values on
 * `record.data` as `{ id, display_name }` objects (not the old `[id, name]`
 * tuples), so `.id` is used to read them.
 *
 * The icon is hidden entirely when there is no product to report on (e.g.
 * section/note order lines), so it never interferes with normal row
 * behaviour.
 */
export class StockInfoWidget extends Component {
    static template = "product_stock_info.StockInfoWidget";
    static components = { StockInfoPopoverButton };
    static props = {
        ...standardWidgetProps,
        productField: { type: String, optional: true },
        warehouseField: { type: String, optional: true },
    };

    get resModel() {
        const { record } = this.props;
        return ["product.product", "product.template"].includes(record.resModel)
            ? record.resModel
            : "product.product";
    }

    get productId() {
        const { record } = this.props;
        if (["product.product", "product.template"].includes(record.resModel)) {
            return record.resId || false;
        }
        if (!this.props.productField) {
            return false;
        }
        const productField = record.data[this.props.productField];
        return (productField && productField.id) || false;
    }

    get warehouseId() {
        if (!this.props.warehouseField) {
            return false;
        }
        const warehouseField = this.props.record.data[this.props.warehouseField];
        return (warehouseField && warehouseField.id) || false;
    }
}

registry.category("view_widgets").add("stock_info_widget", {
    component: StockInfoWidget,
    extractProps: ({ options }) => ({
        productField: options.product_field,
        warehouseField: options.warehouse_field,
    }),
    // Declared dynamically (from the `options` configured on each
    // `<widget>` tag) instead of hardcoded, since the field(s) to depend on
    // don't exist on every model the widget is reused on (e.g. there is no
    // "product_id" field on product.product itself).
    fieldDependencies: ({ options }) => {
        const deps = [];
        if (options.product_field) {
            deps.push({ name: options.product_field, type: "many2one" });
        }
        if (options.warehouse_field) {
            deps.push({ name: options.warehouse_field, type: "many2one" });
        }
        return deps;
    },
});
