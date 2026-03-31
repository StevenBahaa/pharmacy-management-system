from odoo import models , fields , api
from odoo.exceptions import UserError , ValidationError


class Prescription(models.Model):
    _name='prescription'
    _description='Prescription'
    _inherit=['mail.thread' , 'mail.activity.mixin']

    name=fields.Char(string='Name' , readonly=True , default='New') 

    patient_id = fields.Many2one(
    comodel_name='res.partner',
    string='Patient',
    required=True
    )

    doctor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Doctor'
    )

    date = fields.Date(string='Date' , tracking=True , default=fields.Date.today)

    state=fields.Selection(
        selection=[
            ('draft' , 'draft'),
            ('confirmed' , 'confirmed'),
            ('delivered' , 'delivered')
        ], string='State' , default='draft' , tracking=True
    )

    total_amount=fields.Float(string='Total' , compute='_compute_total_amount' , tracking=True)
    line_ids = fields.One2many(
        comodel_name='prescription.line',
        inverse_name='prescription_id',
        string='Medicine Lines'
    )

    def action_confirm(self):
        for rec in self:    
            if not rec.line_ids:
                raise UserError("You cannot confirm a prescription with no medicines.")
            
            for line in rec.line_ids:
                if not line.product_id:
                    raise UserError("All lines must have a medicine selected.")
                
                if line.quantity <= 0:
                    raise UserError(
                        f"Medicine '{line.product_id.name}' has an invalid quantity."
                    )
                
                if line.quantity > line.product_id.qty_available:
                    raise UserError(
                        f"Not enough stock for '{line.product_id.name}'.\n"
                        f"Requested: {line.quantity} | "
                        f"Available: {line.product_id.qty_available}"
                    )
        self.state = 'confirmed'

    def action_deliver(self):
        self.state = 'delivered'
