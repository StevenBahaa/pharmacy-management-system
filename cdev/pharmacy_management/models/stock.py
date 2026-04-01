from datetime import timedelta
from odoo import models, fields, api, _


class StockLot(models.Model):
    _inherit = 'stock.lot'

    x_expiry_notified  = fields.Boolean(string='Expiry Warning Sent',  default=False, store=True)
    x_expired_notified = fields.Boolean(string='Expired Warning Sent', default=False, store=True)

    is_expired = fields.Boolean(
        string='Expired',
        compute='_compute_is_expired',
        store=True
    )

    @api.depends('expiration_date')
    def _compute_is_expired(self):
        now = fields.Datetime.now()
        for rec in self:
            rec.is_expired = bool(
                rec.expiration_date and rec.expiration_date < now
            )

    @api.model
    def cron_check_medicine_expiry(self):
        today         = fields.Date.today()
        warning_limit = today + timedelta(days=30)

        activity_type = self.env.ref(
            'mail.mail_activity_data_todo', raise_if_not_found=False)

        responsible = self.env.ref('base.user_admin')

        lots = self.search([
            ('product_id.is_medicine', '=', True),
            ('expiration_date', '!=', False),
        ])

        for lot in lots:
            if not lot.expiration_date:
                continue

            expiry_date = lot.expiration_date.date()

            # Already expired
            if expiry_date < today and not lot.x_expired_notified:
                message = (
                    f"Urgent: Batch '{lot.name}' of medicine "
                    f"'{lot.product_id.display_name}' expired on {expiry_date}. "
                    f"Remove from stock immediately."
                )
                lot.message_post(body=message)
                if activity_type:
                    self.env['mail.activity'].create({
                        'res_model_id': self.env['ir.model']._get_id('product.template'),
                        'res_id':       lot.product_id.id,
                        'activity_type_id': activity_type.id,
                        'summary':          _('Expired Medicine Batch'),
                        'note':             message,
                        'date_deadline':    today,
                        'user_id': self.env.user.id,
                    })
                lot.x_expired_notified = True
                continue

            # Expiring within 30 days
            if today <= expiry_date <= warning_limit and not lot.x_expiry_notified:
                message = (
                    f"Reminder: Batch '{lot.name}' of medicine "
                    f"'{lot.product_id.display_name}' will expire on {expiry_date}."
                )
                lot.message_post(body=message)
                if activity_type:
                    self.env['mail.activity'].create({
                        'res_model_id': self.env['ir.model']._get_id('product.template'),
                        'res_id':       lot.product_id.id,
                        'activity_type_id': activity_type.id,
                        'summary':          _('Medicine Expiring Soon'),
                        'note':             message,
                        'date_deadline':    expiry_date,
                        'user_id': self.env.user.id,
                    })
                lot.x_expiry_notified = True