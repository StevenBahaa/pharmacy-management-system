from datetime import timedelta
from odoo.exceptions import UserError
from odoo import fields ,models ,api

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
    insurance_program_id = fields.Many2one(
        comodel_name='pharmacy.insurance.program',
        string='Insurance Program',
        readonly=True,
    )
    discount = fields.Float(
        string='Discount (%)',
        default=0.0,
        readonly=True,
    )
    amount_discount = fields.Float(
        string='Discount Amount',
        compute='_compute_amounts',
        store=True,
    )
    total_after_discount = fields.Float(
        string='Total After Discount',
        compute='_compute_amounts',
        store=True,
    )

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', 'New') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'pharmacy.prescription.sequence'
            ) or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        today = fields.Date.today()
        limit_date = today + timedelta(days=2)

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
                product = line.product_id.product_variant_id
                available = product.qty_available
                if line.quantity > available:
                    raise UserError(
                        f"Not enough stock for '{line.product_id.name}'.\n"
                        f"Requested: {line.quantity} | Available: {available}"
                    )
                if line.lot_id:
                    if not line.lot_id.expiration_date:
                        raise UserError(
                            f"Lot '{line.lot_id.name}' of '{line.product_id.name}' "
                            f"has no expiry date set."
                        )
                    lot_expiry = fields.Date.to_date(line.lot_id.expiration_date)
                    if lot_expiry <= limit_date:
                        raise UserError(
                            f"Lot '{line.lot_id.name}' of '{line.product_id.name}' "
                            f"is expired or expiring within 2 days ({lot_expiry})."
                        )

            # ── Get discount from patient insurance program ──────────────
            discount = 0.0
            program = rec.patient_id.insurance_program_id
            if program and program.active:
                if not program.valid_until or program.valid_until >= today:
                    discount = program.discount
                    rec.insurance_program_id = program.id
                    rec.discount = discount

            # ── Apply discount to all lines ──────────────────────────────
            for line in rec.line_ids:
                line.discount = discount

            # ── Create Sale Order ────────────────────────────────────────
            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.company.id)], limit=1
            )
            sale_order = self.env['sale.order'].create({
                'partner_id': rec.patient_id.id,
                'warehouse_id': warehouse.id,
                'order_line': [
                    (0, 0, {
                        'product_id':      line.product_id.product_variant_id.id,
                        'product_uom_qty': line.quantity,
                        'price_unit':      line.price_unit,
                        'discount':        line.discount,
                    }) for line in rec.line_ids
                ]
            })
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
    
    @api.depends('line_ids.subtotal', 'discount')
    def _compute_amounts(self):
        for rec in self:
            subtotal = sum(rec.line_ids.mapped('subtotal'))
            rec.amount_discount    = subtotal * rec.discount / 100
            rec.total_after_discount = subtotal - rec.amount_discount

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('subtotal'))

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        today = fields.Date.today()
        if self.patient_id and self.patient_id.insurance_program_id:
            program = self.patient_id.insurance_program_id
            # Check program is still valid
            if not program.valid_until or program.valid_until >= today:
                self.insurance_program_id = program.id
                self.discount = program.discount
            else:
                self.insurance_program_id = False
                self.discount = 0.0
        else:
            self.insurance_program_id = False
            self.discount = 0.0

        # Propagate discount to all lines
        for line in self.line_ids:
            line.discount = self.discount
    
    