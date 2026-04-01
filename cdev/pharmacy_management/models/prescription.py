from odoo import models, fields ,api
from odoo.exceptions import UserError

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

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        readonly=True
    )

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', 'New') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'pharmacy.prescription.sequence'
            ) or 'New'
        return super().create(vals_list)


    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('subtotal'))

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
                available = line.product_id.product_variant_id.qty_available
                if line.quantity > available:
                    raise UserError(
                        f"Not enough stock for '{line.product_id.name}'.\n"
                        f"Requested: {line.quantity} | "
                        f"Available: {available}"
                    )

            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.company.id)],
                limit=1
            )

            sale_order = self.env['sale.order'].create({
                'partner_id': rec.patient_id.id,

                'order_line': [
                    (0, 0, {
                        'product_id': line.product_id.product_variant_id.id,
                        'product_uom_qty': line.quantity,
                        'price_unit': line.price_unit,
                    }) for line in rec.line_ids
                ]
            })

            # Confirm sale order → generates delivery in Ready state
            sale_order.action_confirm()
            rec.sale_order_id = sale_order.id
            rec.state = 'confirmed'


    def action_deliver(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError("Only confirmed prescriptions can be delivered.")

            if not rec.sale_order_id:
                raise UserError("No sale order linked to this prescription.")

            picking = rec.sale_order_id.picking_ids.filtered(
                lambda p: p.state not in ('done', 'cancel')
            )

            if not picking:
                raise UserError("No pending delivery found.")

            for pick in picking:
                for move in pick.move_ids:
                    line = rec.line_ids.filtered(
                        lambda l: l.product_id.product_variant_id == move.product_id
                    )[:1]

                    move.quantity = move.product_uom_qty

                    if move.product_id.tracking != 'none' and line and line.lot_id:
                        move.move_line_ids.write({'lot_id': line.lot_id.id})
                    elif move.product_id.tracking != 'none' and not line.lot_id:
                        raise UserError(
                            f"Please select a Batch Number for '{move.product_id.name}' "
                            f"before delivering."
                        )

                pick.with_context(skip_immediate=True).button_validate()

            rec.state = 'delivered'

    def action_print_invoice(self):
        self.ensure_one()
        return self.env.ref(
            'pharmacy_management.action_report_prescription_receipt'
        ).report_action(self)