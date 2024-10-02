from odoo import models, fields, api
from odoo.exceptions import UserError

class AdvancedProductFilterWizard(models.TransientModel):
    _name="advanced.product.filter.wizard"

    product_family = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Familia",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'familia')]")
    product_subfamily = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Subfamilia",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'subfamilia')]")
    product_type = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Tipo",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'tipo')]")
    product_color = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Color",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'color')]")
    product_grams = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Gramos",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'gramos')]")
    product_wide = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Anchos",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'ancho')]")
    product_long = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Largos",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'largo')]")
    product_centro = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Centros",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'centro')]")
    product_diametro = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Diametros",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'diametro')]")
    product_certificate = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Certificado",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'certificado')]")
    
    result_ids = fields.Many2many(
        comodel_name='product.product',
        string='Search Results',
        readonly=True,
        relation='wizard_product_search_rel'  # Custom relation table for search results
    )
    line_wizard_ids = fields.One2many('advanced.product.filter.line.wizard', 'wizard_id', string="Lines")


    def action_search(self):
        domain = [('product_cosal', 'in', ('rollo', 'hoja'))]
        attribute_ids = []

        # Collecting the selected attribute ids from the fields
        if self.product_family:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_family.name))
        if self.product_subfamily:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_subfamily.name))
        if self.product_type:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_type.name))
        if self.product_color:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_color.name))
        if self.product_grams:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_grams.name))
        if self.product_wide:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_wide.name))
        if self.product_long:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_long.name))
        if self.product_centro:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_centro.name))
        if self.product_diametro:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_diametro.name))
        if self.product_certificate:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_certificate.name))

        # Add to the domain only if there are attribute_ids
        for attribute_id in attribute_ids:
            domain.append(attribute_id)

        # Log the domain to debug
        print('\n\n\nDomain: %s' % domain)

        # Perform the search
        products = self.env['product.product'].search(domain)
        print(products.ids)
        self.line_wizard_ids.unlink()
        lines = []
        for product in products:
            lines.append((0, 0, {
                'name': product.name,
                'product_id': product.id,
            }))
        self.write({'line_wizard_ids': lines})
        return {
            'view_mode': 'form',
            'res_model': 'advanced.product.filter.wizard',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target':'new'
            }

    def action_restore_fields(self):
        self.write({
            'product_family': False,
            'product_subfamily': False,
            'product_type': False,
            'product_color': False,
            'product_grams': False,
            'product_wide': False,
            'product_long': False,
            'product_centro': False,
            'product_diametro': False,
            'product_certificate': False,
            'result_ids': False
        })



    def action_add(self):
        purchase_order_id = self.env.context.get('active_id') 
        if not purchase_order_id:
            raise UserError('No purchase order found.')
        purchase_order = self.env['purchase.order'].browse(purchase_order_id)

        print("Selected Products to add:")
        print(self.result_ids)
        if not self.result_ids:
            raise UserError('No products were selected.')
        new_lines = []
        for product in self.result_ids:
            print(f"Adding product: {product.name} (ID: {product.id})")

            existing_line = self.env['purchase.order.line'].search([
                ('order_id', '=', purchase_order.id),
                ('product_id', '=', product.id)
            ])
            
            if existing_line:
                print(f"Product {product.name} already exists in the purchase order.")
                continue
            
            # Add the product to the purchase order
            new_line = (0, 0, {
                'product_id': product.id,
                'product_qty': 1.0, 
                'price_unit': product.standard_price,  
                'date_planned': fields.Date.today(), 
            })
            new_lines.append(new_line)
        if new_lines:
            print(f"Adding the following lines to the purchase order: {new_lines}")
            purchase_order.write({'order_line': new_lines})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }

    def action_save_products(self):
        result_products = self.result_ids
        for line in self.line_wizard_ids:
            if line.to_add:
                result_products |= line.product_id
        self.result_ids = result_products
        return {
            'view_mode': 'form',
            'res_model': 'advanced.product.filter.wizard',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target':'new'
            }