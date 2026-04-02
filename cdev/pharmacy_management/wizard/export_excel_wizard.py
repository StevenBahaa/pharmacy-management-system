from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PrescriptionExportWizard(models.TransientModel):
    _name = 'prescription.export.wizard'
    _description = 'Export Prescriptions to Excel'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    state_filter = fields.Selection([
        ('all', 'All Prescriptions'),
        ('confirmed', 'Confirmed Only'),
        ('delivered', 'Delivered Only'),
    ], string='Filter By State', default='all', required=True)

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for rec in self:
            if rec.from_date and rec.to_date and rec.from_date > rec.to_date:
                raise ValidationError("From Date cannot be after To Date.")

    def action_export(self):
        self.ensure_one()
        data = {
            'from_date': str(self.from_date),
            'to_date':   str(self.to_date),
            'state_filter': self.state_filter,
        }
        return self.env.ref(
            'pharmacy_management.action_report_prescription_xlsx'
        ).report_action(self, data=data)