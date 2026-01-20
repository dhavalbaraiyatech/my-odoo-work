from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    is_allow_in_tree_view = fields.Boolean(
        string="Allow this Pricelist in Product Tree View?",
        help="If checked, this pricelist will be shown in the product list view as a column.", default=False)

    def create(self, vals):
        res = super(ProductPricelist, self).create(vals)
        if vals.get('is_allow_in_tree_view') == True:
            res._create_check_dynamic_field_ids()
        return res

    def write(self, vals):
        res = super(ProductPricelist, self).write(vals)
        if vals.get('is_allow_in_tree_view') == True:
            self._create_check_dynamic_field_ids()
        return res

    # @api.depends('allow_in_tree_view')
    def _create_check_dynamic_field_ids(self):
        for price in self:
            for items in price.item_ids:
                pricelist_name = re.sub(r"[ \-]+", "_", self.name)
                if items.compute_price == 'fixed' and items.applied_on == '1_product' or items.applied_on == '3_global':
                    model = 'product.template'
                    field_name = "x_" + pricelist_name

                    # Create dynamic field if not exists
                    field = self._create_dynamic_field(field_name, self.name, model, 'char')

                    if field:
                        # Update product template prices
                        if items.product_tmpl_id:
                            products = items.product_tmpl_id
                        else:
                            products = self.env['product.template'].search([])

                        for pro in products:
                            pro.sudo().write({field.name: items.price})

                        # Create view to display the field in tree view
                        inherit_view_name = f"inherit.dynamic.custom.{field_name}.field"
                        xml_id = "product.product_template_tree_view"
                        x_path_field = "list_price"
                        self._create_dynamic_view(field_name, model, inherit_view_name, xml_id, x_path_field)

                    # self.allow_in_tree_view = True

                elif items.compute_price == 'fixed' and items.applied_on == '0_product_variant':
                    model = 'product.product'
                    field_name = "x_" + pricelist_name

                    # Create dynamic field if not exists
                    field = self._create_dynamic_field(field_name, self.name, model, 'char')

                    if field:
                        # Update product template prices
                        items.product_id.sudo().write({field.name: items.price})

                        # Create view to display the field in tree view
                        inherit_view_name = f"product_inherit.dynamic.custom.{field_name}.field"
                        xml_id = "product.product_product_tree_view"
                        x_path_field = "lst_price"
                        self._create_dynamic_view(field_name, model, inherit_view_name, xml_id, x_path_field)

                elif items.compute_price == 'fixed' and items.applied_on == '2_product_category':
                    model = 'product.template'
                    field_name = "x_" + pricelist_name

                    # Create dynamic field if not exists
                    field = self._create_dynamic_field(field_name, self.name, model, 'char')

                    if field:
                        # Update product template prices
                        category_pro = self.env['product.template'].search([('categ_id', '=', items.categ_id.id)])
                        for product_template in category_pro:
                            product_template.sudo().write({field.name: items.price})

                        # Create view to display the field in tree view
                        inherit_view_name = f"inherit.dynamic.custom.{field_name}.field"
                        xml_id = "product.product_template_tree_view"
                        x_path_field = "list_price"
                        self._create_dynamic_view(field_name, model, inherit_view_name, xml_id, x_path_field)

    def _create_dynamic_field(self, field_name, field_description, model, field_type):
        """
        Create a dynamic field in the specified model if it does not exist.
        """
        model_id = self.env['ir.model'].sudo().search([('model', '=', model)], limit=1)

        existing_field = self.env['ir.model.fields'].sudo().search([
            ('name', '=', field_name),
            ('model_id', '=', model_id.id)
        ], limit=1)

        if not existing_field:
            new_field = self.env['ir.model.fields'].sudo().create({
                'name': field_name,
                'field_description': field_description,
                'model_id': model_id.id,
                'ttype': field_type
            })
            self._cr.commit()
            return new_field
        return existing_field

    def _create_dynamic_view(self, field_name, model, view_name, xml_id, x_path_field):
        """
        Create a dynamic view for the specified field in the model if it does not exist.
        """
        existing_view = self.env['ir.ui.view'].sudo().search(
            [('name', '=', view_name), ('model', '=', model), '|', ('active', '=', True), ('active', '=', False)],
            limit=1)
        if not existing_view:
            inherit_id = self.env.ref(xml_id, raise_if_not_found=False)
            if not inherit_id:
                raise ValidationError(f"Base view '{xml_id}' not found.")

            arch_base = _(
                '<?xml version="1.0"?>'
                '<data>'
                '<field name="%s" position="after">'
                '<field optional="hide" name="%s"/>'
                '</field>'
                '</data>'
            ) % (x_path_field, field_name)

            self.env['ir.ui.view'].sudo().create({
                'name': view_name,
                'type': 'tree',
                'model': model,
                'mode': 'extension',
                'inherit_id': inherit_id.id,
                'arch_base': arch_base,
                'active': True
            })

    def unlink(self):
        # Iterate over the price lists to be deleted
        for pricelist in self:
            for item in pricelist.item_ids:
                domain = [('active', '=', True), ]
                dynamic_view = self.set_as_active_or_note(pricelist.name, item, domain)
                if dynamic_view:
                    dynamic_view.unlink()

        return super(ProductPricelist, self).unlink()

    def toggle_active(self):
        """
        Inherit the toggle_active method to handle archiving/unarchiving
        dynamic views associated with this price list.
        """
        # Iterate over the price lists being toggled
        for pricelist in self:
            if not pricelist.active:
                # If being archived, archive related views
                for item in pricelist.item_ids:
                    domain = [('active', '=', False), ]
                    dynamic_view = self.set_as_active_or_note(pricelist.name, item, domain)
                    # Archive the view if it exists
                    if dynamic_view:
                        dynamic_view.active = True
            else:
                # If being unarchived, reactivate related views
                for item in pricelist.item_ids:
                    domain = [('active', '=', False), ]
                    dynamic_view = self.set_as_active_or_note(pricelist.name, item, domain)
                    # Reactivate the view if it exists
                    if dynamic_view:
                        dynamic_view.active = False

        # Call the super method to toggle the active state
        return super(ProductPricelist, self).toggle_active()

    def set_as_active_or_note(self, name, item, domain):
        pricelist_name = re.sub(r"[ \-]+", "_", name)
        model = 'product.product' if item.applied_on == '0_product_variant' else 'product.template'
        field_name = f"x_{pricelist_name}"
        view_name = (
            f"product_inherit.dynamic.custom.{field_name}.field"
            if item.applied_on == '0_product_variant'
            else f"inherit.dynamic.custom.{field_name}.field"
        )
        domain.append(('name', '=', view_name))
        domain.append(('model', '=', model))
        dynamic_view = self.env['ir.ui.view'].sudo().search(domain)
        return dynamic_view