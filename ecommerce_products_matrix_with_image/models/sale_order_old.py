
from odoo import models
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_web_matrix(self, product):
        """Prepare a 2D or 3D matrix structure for product variants."""
        grid = {
            'header': [],
            'matrix': [],
            'attribute_count': 0,
        }
        # user_country = request.env.user.partner_id.country_id
        current_website = request.website
        order_sudo = request.cart or request.website._create_cart()

        # Resolve customer pricelist: prefer cart pricelist, fallback to website pricelist
        valid_lines = product.valid_product_template_attribute_line_ids
        grid['attribute_count'] = len(valid_lines)

        # Only process if at least 2 attributes exist
        if len(valid_lines) < 2:
            return grid

        # Extract attribute lines
        attr_third = valid_lines[2] if len(valid_lines) >= 3 else None
        attr_col = valid_lines[0]
        attr_row = valid_lines[1]

        # Prepare headers for columns (2nd attribute)
        grid['header'] = [{'name': ''}]
        allowed_columns = []

        for col_val in attr_col.value_ids:
            # pick ONE variant for this column (used only for image)

            # all variants having this color
            variants_for_color = product.product_variant_ids.filtered(
                lambda v: col_val in v.product_template_attribute_value_ids.mapped(
                    'product_attribute_value_id'
                )
            )

            # variants allowed for this country
            allowed_variants = variants_for_color.filtered(
                lambda v: self._variant_is_allowed(v, current_website)
            )

            # ❌ remove entire column if none allowed
            if not allowed_variants:
                continue

            # keep column
            grid['header'].append({
                'name': col_val.name,
                'variant_id': allowed_variants[0].id,  # for image
                'attribute_value_id': col_val.id,
            })

            allowed_columns.append(col_val)

            # variant = product.product_variant_ids.filtered(
            #     lambda v: col_val in v.product_template_attribute_value_ids.mapped('product_attribute_value_id')
            # )[:1]
            #
            # grid['header'].append({
            #     'name': col_val.name,
            #     'variant_id': variant.id if variant else False,
            # })

        # Prepare 3D or 2D matrix
        if attr_third:
            # For each third-attribute value, generate a section (sub-matrix)
            for third_val in attr_third.value_ids:
                section = {
                    'third_attr': {'id': third_val.id, 'name': third_val.name},
                    'rows': []
                }
                for row_val in attr_row.value_ids:
                    row_data = [{'name': f"{row_val.name} • {third_val.name}"}]
                    row_has_allowed_variant = False  # KEY FLAG
                    for col_val in allowed_columns:
                        variant = product.product_variant_ids.filtered(
                            lambda v: all([
                                row_val in v.product_template_attribute_value_ids.mapped('product_attribute_value_id'),
                                col_val in v.product_template_attribute_value_ids.mapped('product_attribute_value_id'),
                                third_val in v.product_template_attribute_value_ids.mapped(
                                    'product_attribute_value_id'),
                            ])
                        )[:1]

                        if not variant:
                            row_data.append({'is_possible_combination': False})
                            continue

                        is_allowed = self._variant_is_allowed(variant, current_website)

                        if not is_allowed:
                            row_data.append({
                                'is_possible_combination': True,
                                'is_not_visible': True,
                            })
                            continue

                        row_has_allowed_variant = True  # KEY FLAG

                        # is_allowed = self._variant_is_allowed(variant, user_country)
                        price = variant._get_combination_info_variant().get('price')
                        pro_qty = order_sudo.order_line.filtered(lambda line: line.product_id.id == variant.id)
                        qty = pro_qty.product_uom_qty if pro_qty else 0
                        free_qty = variant.sudo().with_context(warehouse=request.website.warehouse_id.id).free_qty
                        row_data.append({
                            'variant_id': variant.id,
                            'product_id': product.id,
                            'free_qty': free_qty,
                            'price': price,
                            'qty': qty,
                            'is_possible_combination': True,
                            'ptavs': [ptavs.id for ptavs in variant.product_template_attribute_value_ids],
                            'ptav_ids': [v.product_attribute_value_id.id for v in
                                         variant.product_template_attribute_value_ids],
                            'value_name': f"{row_val.name} / {col_val.name} / {third_val.name}",
                            'value_id': [v.product_attribute_value_id.id for v in
                                         variant.product_template_attribute_value_ids],
                            'is_custom': False,
                            'is_not_visible': False,
                        })
                    if row_has_allowed_variant:
                        section['rows'].append(row_data)
                grid['matrix'].append(section)
        else:
            # Normal 2-attribute behavior
            for row_val in attr_row.value_ids:
                row_data = [{'name': row_val.name}]
                row_has_allowed_variant = False  # KEY FLAG
                for col_val in allowed_columns:
                    variant = product.product_variant_ids.filtered(
                        lambda v: all([
                            row_val in v.product_template_attribute_value_ids.mapped('product_attribute_value_id'),
                            col_val in v.product_template_attribute_value_ids.mapped('product_attribute_value_id'),
                        ])
                    )[:1]

                    if not variant:
                        row_data.append({'is_possible_combination': False})
                        continue

                    is_allowed = self._variant_is_allowed(variant, current_website)

                    if not is_allowed:
                        row_data.append({
                            'is_possible_combination': True,
                            'is_not_visible': True,  # 👈 shows "Not Available"
                        })
                        continue
                    # at least ONE allowed variant in this row
                    row_has_allowed_variant = True


                    # is_allowed = self._variant_is_allowed(variant, user_country)
                    price = variant._get_combination_info_variant().get('price')
                    pro_qty = order_sudo.order_line.filtered(lambda line: line.product_id.id == variant.id)
                    qty = pro_qty.product_uom_qty if pro_qty else 0
                    free_qty = variant.sudo().with_context(warehouse=request.website.warehouse_id.id).free_qty
                    # request.env['website'].get_current_website()._get_product_available_qty(variant.sudo())
                    row_data.append({
                        'variant_id': variant.id,
                        'product_id': product.id,
                        'free_qty': free_qty,
                        'price': price,
                        'qty': qty,
                        'is_possible_combination': True,
                        'ptavs': [ptavs.id for ptavs in variant.product_template_attribute_value_ids],
                        'ptav_ids': [v.product_attribute_value_id.id for v in
                                     variant.product_template_attribute_value_ids],
                        'value_name': f"{row_val.name} / {col_val.name}",
                        'value_id': [v.product_attribute_value_id.id for v in
                                     variant.product_template_attribute_value_ids],
                        'is_custom': False,
                        'is_not_visible': False,
                    })
                if row_has_allowed_variant:
                    grid['matrix'].append(row_data)

        return grid

    # Add this helper inside the method before the loops:
    def _variant_is_allowed(self, variant, current_website):
        """Return True if variant has no country restriction OR user country matches."""
        if not variant.website_ids:
            return False
        return current_website in variant.website_ids
