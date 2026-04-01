from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    insurance_program_id = fields.Many2one(
        comodel_name='pharmacy.insurance.program',
        string='Insurance Program',
        domain=[('active', '=', True)],
    )