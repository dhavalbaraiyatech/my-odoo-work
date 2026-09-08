/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePopover } from "@web/core/popover/popover_hook";
import { useService } from "@web/core/utils/hooks";

/**
 * Popover body. Two ways to feed it data, so the exact same component can be
 * reused by the backend (ORM-backed) and by the POS (which already has its
 * own richer, warehouse-aware stock lookup and runs against an offline
 * cache):
 *  - `getData`: an async function resolving to
 *    `{ display_name, qty_available, virtual_available, free_qty, uom_name, active }`
 *    (or `{ error: <reason> }`). Used by POS.
 *  - `productId` (+ optional `warehouseId`, `resModel`): the component looks
 *    the quantities up itself via `get_stock_info_popover_data`. Used by the
 *    backend widget.
 */
export class StockInfoPopoverContent extends Component {
    static template = "product_stock_info.StockInfoPopoverContent";
    static props = {
        close: Function,
        productId: { type: [Number, Boolean], optional: true },
        warehouseId: { type: [Number, Boolean], optional: true },
        resModel: { type: String, optional: true },
        getData: { type: Function, optional: true },
    };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: true,
            error: false,
            display_name: "",
            qty_available: 0,
            virtual_available: 0,
            free_qty: 0,
            uom_name: "",
            active: true,
        });
        onWillStart(() => this.loadData());
    }

    async loadData() {
        let data;
        try {
            data = this.props.getData ? await this.props.getData() : await this.fetchFromServer();
        } catch {
            data = { error: "fetch_failed" };
        }
        if (!data || data.error) {
            this.state.error = _t("Unable to retrieve stock information for this product.");
        } else {
            Object.assign(this.state, data);
        }
        this.state.loading = false;
    }

    async fetchFromServer() {
        if (!this.props.productId) {
            return { error: "no_product" };
        }
        return this.orm.call(this.props.resModel || "product.product", "get_stock_info_popover_data", [
            this.props.productId,
            this.props.warehouseId || false,
        ]);
    }
}

/**
 * Small, unobtrusive (i) icon. Clicking it toggles a popover with the
 * product's stock quantities. The click is stopped from propagating so the
 * icon never triggers row selection / product selection behaviour of
 * whatever it is placed inside.
 */
export class StockInfoPopoverButton extends Component {
    static template = "product_stock_info.StockInfoPopoverButton";
    static components = { Popover: StockInfoPopoverContent };
    static props = {
        productId: { type: [Number, Boolean], optional: true },
        warehouseId: { type: [Number, Boolean], optional: true },
        resModel: { type: String, optional: true },
        getData: { type: Function, optional: true },
    };

    setup() {
        this.popover = usePopover(this.constructor.components.Popover, { position: "bottom" });
    }

    get title() {
        return _t("View stock quantities");
    }

    onClick(ev) {
        ev.stopPropagation();
        if (this.popover.isOpen) {
            this.popover.close();
            return;
        }
        this.popover.open(ev.currentTarget, {
            productId: this.props.productId,
            warehouseId: this.props.warehouseId,
            resModel: this.props.resModel,
            getData: this.props.getData,
        });
    }
}
