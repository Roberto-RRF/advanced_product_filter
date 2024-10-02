from odoo import models, fields, api
from odoo.exceptions import UserError

class AdvancedProductFilterLineWizard(models.TransientModel):
    _name = "advanced.product.filter.line.wizard"
    _description = "Advanced Product Filter Line Wizard"

    name = fields.Char("Product")
    to_add = fields.Boolean("Add")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    wizard_id = fields.Many2one('advanced.product.filter.wizard', string="Wizard", ondelete='cascade')



