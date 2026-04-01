from datetime import timedelta

from odoo import models, fields, api, _


class StockLot(models.Model):
    _inherit = 'stock.lot'

    x_expiry_notified = fields.Boolean(
        string='Expiry Warning Sent',
        default=False
    )
    x_expired_notified = fields.Boolean(
        string='Expired Warning Sent',
        default=False
    )

    x_is_expired = fields.Boolean(
        string='Expired',
        compute='_compute_expiry_flags',
        store=True
    )
    x_is_expiring_soon = fields.Boolean(
        string='Expiring Soon',
        compute='_compute_expiry_flags',
        store=True
    )

    @api.depends('expiration_date')
    def _compute_expiry_flags(self):
        today = fields.Date.today()
        warning_limit = today + timedelta(days=30)

        for rec in self:
            rec.x_is_expired = bool(
                rec.expiration_date and rec.expiration_date < today
            )
            rec.x_is_expiring_soon = bool(
                rec.expiration_date and today <= rec.expiration_date <= warning_limit
            )

    @api.model
    def cron_check_medicine_expiry(self):
        today = fields.Date.today()
        warning_limit = today + timedelta(days=30)

        activity_type = self.env.ref(
            'mail.mail_activity_data_todo',
            raise_if_not_found=False
        )

        users = self.env['res.users'].search([('share', '=', False)])

        lots = self.search([
            ('product_id.is_medicine', '=', True),
            ('expiration_date', '!=', False),
        ])

        product_template_model_id = self.env['ir.model']._get_id('product.template')

        for lot in lots:
            expiry_date = lot.expiration_date.date()
            if not expiry_date:
                continue

            product_tmpl = lot.product_id.product_tmpl_id

            # 1) Already expired
            if expiry_date < today and not lot.x_expired_notified:
                message = _(
                    "Urgent: This medicine has already expired and must be removed "
                    "from stock immediately.\n\n"
                    "Medicine: %s\n"
                    "Batch: %s\n"
                    "Expiry Date: %s"
                ) % (
                    lot.product_id.display_name,
                    lot.name,
                    expiry_date
                )

                # notification on lot
                lot.message_post(body=message)

                # notification on medicine record itself
                product_tmpl.message_post(body=message)

                # To-Do notifications for all internal users
                if activity_type:
                    for user in users:
                        self.env['mail.activity'].create({
                            'res_model_id': product_template_model_id,
                            'res_id': product_tmpl.id,
                            'activity_type_id': activity_type.id,
                            'summary': _('Expired Medicine Batch'),
                            'note': message,
                            'date_deadline': today,
                            'user_id': user.id,
                        })

                lot.x_expired_notified = True
                continue

            # 2) Expiring within 30 days
            if today <= expiry_date <= warning_limit and not lot.x_expiry_notified:
                message = _(
                    "To-Do: This medicine is expiring soon.\n\n"
                    "Medicine: %s\n"
                    "Batch: %s\n"
                    "Expiry Date: %s"
                ) % (
                    lot.product_id.display_name,
                    lot.name,
                    expiry_date
                )

                # notification on lot
                lot.message_post(body=message)

                # notification on medicine record itself
                product_tmpl.message_post(body=message)

                # To-Do notifications for all internal users
                if activity_type:
                    for user in users:
                        self.env['mail.activity'].create({
                            'res_model_id': product_template_model_id,
                            'res_id': product_tmpl.id,
                            'activity_type_id': activity_type.id,
                            'summary': _('Medicine Expiring Soon'),
                            'note': message,
                            'date_deadline': expiry_date,
                            'user_id': user.id,
                        })

                lot.x_expiry_notified = True