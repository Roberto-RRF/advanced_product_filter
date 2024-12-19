from odoo import models, fields, api
from odoo.exceptions import UserError

class AdvancedProductFilterWizard(models.TransientModel):
    _name="advanced.product.filter.wizard"

    @api.model
    def default_get(self, default_fields):
        rec = super(AdvancedProductFilterWizard, self).default_get(default_fields)
        active_ids = self._context.get('active_ids')
        active_model = self._context.get('active_model')

        rec.update({
            'document_id': active_ids[0],
            'document_model': active_model,
        })
        return rec

    document_id = fields.Integer('Document ID')
    document_model = fields.Char('Document Model')

    type_cosal = fields.Selection(
        [
            ('',''),
            ('hoja', 'Hoja'),
            ('rollo', 'Rollo'),
        ],
        string='Tipo',
    )
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
    product_ancho = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Ancho cm",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'ancho')]")
    product_largo = fields.Many2one(
        comodel_name='product.attribute.value',
        string="Largo cm",
        change_default=True,
        domain="[('attribute_id.attribute_cosal', '=', 'largo')]")
    product_tag = fields.Many2one(
        'product.tag', 
        string="Product Tag"
    )
    result_ids = fields.Many2many(
        comodel_name='product.product',
        string='Search Results',
        readonly=True,
        relation='wizard_product_search_rel'  # Custom relation table for search results
    )
    line_wizard_ids = fields.One2many('advanced.product.filter.line.wizard', 'wizard_id', string="Lines")

    def action_add_all(self):
        # result_products = self.result_ids
        result_ids = self.result_ids.ids if self.result_ids else []
        for line in self.line_wizard_ids:
            result_ids.append(line.product_id.id)
        #self.result_ids = result_products
        self.result_ids = [(6,0, result_ids)]
        return {
            'view_mode': 'form',
            'res_model': 'advanced.product.filter.wizard',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target':'new'
            }

    def action_search(self):
        domain = []
        attribute_ids = []

        if self.type_cosal:
            domain.append(('product_cosal', '=', self.type_cosal))
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
        if self.product_largo:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_largo.name))
        if self.product_ancho:
            attribute_ids.append(('product_template_attribute_value_ids','=',self.product_ancho.name))
        if self.product_tag:
            domain.append(('additional_product_tag_ids', 'in', self.product_tag.ids))
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
        if not self.document_id or not self.document_model:
            raise UserError('No document found.')
        
        # PURCHASE ORDER
        if self.document_model == 'purchase.order':
            purchase_order = self.env['purchase.order'].browse(self.document_id)
            purchase_order_line_obj = self.env['purchase.order.line'] 
            if not purchase_order:
                raise UserError('No purchase order found.')
            
            if not self.result_ids:
                raise UserError('No products were selected.')
            new_vals_list = []
            for product in self.result_ids:             
                new_line = {
                                'order_id': purchase_order.id,
                                'product_id': product.id,
                                'name': product.display_name,
                                'date_planned': fields.Date.today(),
                                'product_qty': 1,
                                'product_uom': product.uom_po_id.id,
                                'price_unit': product.standard_price
                        }
                new_vals_list.append(new_line)
            if new_vals_list:
                for dictvls in new_vals_list:
                        purchase_order_line_obj.create(dictvls)
        # MRP PRODUCTION
        if self.document_model == 'mrp.production':
            mrp_production = self.env['mrp.production'].browse(self.document_id)
            if not mrp_production:
                raise UserError('No manufacturing order found.')
            
            if not self.result_ids:
                raise UserError('No products were selected.')
            
            for product in self.result_ids:
                component_vals = {
                    'name': product.display_name,
                    'product_id': product.id,
                    'product_uom_qty': 1,  # Quantity of the component (raw material)
                    'product_uom': product.uom_id.id,  # Unit of measure
                    'production_id': mrp_production.id,  # Production order reference
                    'location_id': mrp_production.location_src_id.id,  # Source location (components warehouse)
                    'location_dest_id': mrp_production.location_dest_id.id,  # Destination location (production location)
                    'raw_material_production_id': mrp_production.id,  # Important: link to the production order as a raw material
                    'company_id': mrp_production.company_id.id,  # Company context
                    'state': 'draft',  # Stock move state (draft until confirmed)
                }
                # Add product to the manufacturing order components list
                mrp_production.move_raw_ids.create(component_vals)


        
        if self.document_model == 'sale.order':
            sale_order = self.env['sale.order'].browse(self.document_id)
            sale_order_line_obj = self.env['sale.order.line'] 
            if not sale_order:
                raise UserError('No purchase order found.')
            
            if not self.result_ids:
                raise UserError('No products were selected.')
            new_vals_list = []
            for product in self.result_ids:             
                new_line = {
                                'order_id': sale_order.id,
                                'product_id': product.id,
                                'name': product.display_name,
                                'product_qty': 1,
                                'product_uom': product.uom_po_id.id,
                                'price_unit': product.standard_price
                        }
                new_vals_list.append(new_line)
            if new_vals_list:
                for dictvls in new_vals_list:
                    sale_order_line_obj.create(dictvls)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Document',
            'res_model': self.document_model,
            'res_id': self.document_id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }

    def action_save_products(self):
        # result_products = self.result_ids
        result_ids = self.result_ids.ids if self.result_ids else []
        for line in self.line_wizard_ids:
            if line.to_add:
                #result_products |= line.product_id
                result_ids.append(line.product_id.id)
        #self.result_ids = result_products
        self.result_ids = [(6,0, result_ids)]
        return {
            'view_mode': 'form',
            'res_model': 'advanced.product.filter.wizard',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target':'new'
            }
