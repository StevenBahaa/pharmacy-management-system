from odoo import models , fields , api
from odoo.exceptions import UserError , ValidationError
class PrescriptionLine(models.Model):
    _name='prescription.line'
    _description='Prescription Line'
    

    prescription_id = fields.Many2one(comodel_name='prescription' , string='Prescription')
    product_id = fields.Many2one(comodel_name='product.template' , string='Product')
    quantity =fields.Integer(string='Quantity')
    price_unit= fields.Float(string= 'Uint Price' , related='product_id.list_price' , readonly=True , store=False)
    subtotal = fields.Float(string='Total' , compute='_compute_subtotal' , store=True)

    lot_id = fields.Many2one(
        comodel_name='stock.lot',
        string='Batch Number',
        domain="[('product_id.product_tmpl_id', '=', product_id)]"
    )

    @api.depends('quantity' , 'price_unit')
    def _compute_subtotal (self):
        for rec in self :
            rec.subtotal = rec.quantity * rec.price_unit