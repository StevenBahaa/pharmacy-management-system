# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PharmacyInsuranceProgram(models.Model):
    _name = 'pharmacy.insurance.program'
    _description = 'Insurance Program'

    name = fields.Char(string='Program Name', required=True)
    discount = fields.Float(string='Discount (%)', required=True)
    valid_until = fields.Date(string='Valid Until')
    active = fields.Boolean(string='Active', default=True)

    @api.constrains('discount')
    def _check_discount(self):
        for rec in self:
            if rec.discount <= 0 or rec.discount > 100:
                raise ValidationError(
                    "Discount must be between 0 and 100."
                )