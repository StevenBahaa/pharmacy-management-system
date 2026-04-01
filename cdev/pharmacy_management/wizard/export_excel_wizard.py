# # -*- coding: utf-8 -*-
# from odoo import models


# DOSAGE_FORM_MAP = {
#     'tablet': 'Tablet', 'tablet_er': 'Tablet, Extended Release',
#     'tablet_ec': 'Tablet, Enteric Coated', 'capsule': 'Capsule',
#     'capsule_er': 'Capsule, Extended Release', 'powder_oral': 'Powder for Oral Solution',
#     'granule': 'Granules', 'syrup': 'Syrup', 'suspension_oral': 'Oral Suspension',
#     'solution_oral': 'Oral Solution', 'drops_oral': 'Oral Drops',
#     'effervescent': 'Effervescent Tablet', 'injection_iv': 'Injection — Intravenous',
#     'injection_im': 'Injection — Intramuscular', 'injection_sc': 'Injection — Subcutaneous',
#     'infusion': 'Infusion (IV Bag)', 'powder_inj': 'Powder for Injection',
#     'cream': 'Cream', 'ointment': 'Ointment', 'gel': 'Gel',
#     'patch': 'Transdermal Patch', 'lotion': 'Lotion', 'spray_topical': 'Topical Spray',
#     'inhaler_mdi': 'Metered Dose Inhaler (MDI)', 'inhaler_dpi': 'Dry Powder Inhaler (DPI)',
#     'nebulizer': 'Nebulizer Solution', 'eye_drops': 'Eye Drops',
#     'eye_ointment': 'Eye Ointment', 'ear_drops': 'Ear Drops',
#     'nasal_spray': 'Nasal Spray', 'nasal_drops': 'Nasal Drops',
#     'suppository': 'Suppository', 'enema': 'Enema',
#     'vaginal_tab': 'Vaginal Tablet', 'vaginal_cream': 'Vaginal Cream',
#     'lozenge': 'Lozenge / Troche', 'sublingual': 'Sublingual Tablet',
#     'implant': 'Implant', 'other': 'Other',
# }

# ROUTE_MAP = {
#     'oral': 'Oral (PO)', 'sublingual': 'Sublingual (SL)', 'buccal': 'Buccal',
#     'intravenous': 'Intravenous (IV)', 'intramuscular': 'Intramuscular (IM)',
#     'subcutaneous': 'Subcutaneous (SC)', 'intradermal': 'Intradermal (ID)',
#     'inhalation': 'Inhalation', 'topical': 'Topical', 'transdermal': 'Transdermal',
#     'ophthalmic': 'Ophthalmic', 'otic': 'Otic', 'nasal': 'Nasal',
#     'rectal': 'Rectal (PR)', 'vaginal': 'Vaginal', 'epidural': 'Epidural',
#     'intrathecal': 'Intrathecal', 'other': 'Other',
# }

# STORAGE_MAP = {
#     'room': 'Room Temperature (15–25 °C)', 'cool': 'Cool (8–15 °C)',
#     'refrig': 'Refrigerated (2–8 °C)', 'frozen': 'Frozen (≤ −10 °C)',
#     'protect': 'Protect from Light', 'dry': 'Store Dry (< 40% RH)',
#     'other': 'See Labeling',
# }

# SCHEDULE_MAP = {
#     'otc': 'OTC', 'rx': 'Rx', 'ci': 'Schedule I',
#     'cii': 'Schedule II', 'ciii': 'Schedule III',
#     'civ': 'Schedule IV', 'cv': 'Schedule V',
# }

# HEADERS = [
#     ('Product Name',            24),
#     ('INN / Generic Name',      24),
#     ('Brand Name',              20),
#     ('ATC Code',                14),
#     ('Dosage Form',             22),
#     ('Strength',                18),
#     ('Route of Administration', 24),
#     ('Manufacturer',            24),
#     ('Storage Condition',       24),
#     ('Shelf Life (months)',      16),
#     ('Prescription Status',     22),
#     ('Min Stock Qty',           14),
#     ('Expiry Date',             16),
#     ('Sale Price',              12),
#     ('Cost Price',              12),
#     ('Current Stock',           14),
# ]


# class MedicineXlsxReport(models.AbstractModel):
#     _name = 'report.pharmacy_management.report_medicine_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#     _description = 'Medicine Excel Export Report'

#     def generate_xlsx_report(self, workbook, data, records):

#         # ── Formats ──────────────────────────────────────────────────────────
#         title_fmt = workbook.add_format({
#             'bold': True, 'font_name': 'Arial', 'font_size': 14,
#             'font_color': '#FFFFFF', 'bg_color': '#1F7A4A',
#             'align': 'center', 'valign': 'vcenter',
#         })
#         subtitle_fmt = workbook.add_format({
#             'italic': True, 'font_name': 'Arial', 'font_size': 9,
#             'font_color': '#FFFFFF', 'bg_color': '#1E4A8C',
#             'align': 'center', 'valign': 'vcenter',
#         })
#         header_fmt = workbook.add_format({
#             'bold': True, 'font_name': 'Arial', 'font_size': 10,
#             'font_color': '#FFFFFF', 'bg_color': '#1E4A8C',
#             'align': 'center', 'valign': 'vcenter',
#             'border': 1, 'text_wrap': True,
#         })
#         body_fmt = workbook.add_format({
#             'font_name': 'Arial', 'font_size': 10,
#             'align': 'left', 'valign': 'vcenter', 'border': 1,
#         })
#         number_fmt = workbook.add_format({
#             'font_name': 'Arial', 'font_size': 10,
#             'align': 'right', 'valign': 'vcenter',
#             'border': 1, 'num_format': '#,##0.00',
#         })
#         low_stock_fmt = workbook.add_format({
#             'bold': True, 'font_name': 'Arial', 'font_size': 10,
#             'font_color': '#FFFFFF', 'bg_color': '#C0392B',
#             'align': 'right', 'valign': 'vcenter',
#             'border': 1, 'num_format': '#,##0.00',
#         })
#         summary_fmt = workbook.add_format({
#             'bold': True, 'font_name': 'Arial', 'font_size': 10,
#             'font_color': '#FFFFFF', 'bg_color': '#1F7A4A',
#             'align': 'left', 'valign': 'vcenter', 'border': 1,
#         })

#         # ── Worksheet ────────────────────────────────────────────────────────
#         ws = workbook.add_worksheet('Medicine Export')
#         ws.freeze_panes(4, 0)
#         ws.set_zoom(90)

#         col_count = len(HEADERS)

#         # Row 0 — Title
#         ws.merge_range(0, 0, 0, col_count - 1,
#                        'Al-Shifa Pharmacy — Medicine Export', title_fmt)
#         ws.set_row(0, 36)

#         # Row 1 — Subtitle
#         ws.merge_range(1, 0, 1, col_count - 1,
#                        'Exported from Odoo 18 — Pharmacy Management System',
#                        subtitle_fmt)
#         ws.set_row(1, 20)

#         # Row 2 — blank spacer
#         ws.set_row(2, 6)

#         # Row 3 — Column headers
#         ws.set_row(3, 36)
#         for col, (header, width) in enumerate(HEADERS):
#             ws.write(3, col, header, header_fmt)
#             ws.set_column(col, col, width)

#         # Rows 4+ — Medicine records only
#         medicine_records = records.filtered(lambda r: r.is_medicine)

#         for row_idx, rec in enumerate(medicine_records, start=4):
#             ws.set_row(row_idx, 20)
#             is_low = rec.qty_available < rec.x_min_stock_qty
#             qty_fmt = low_stock_fmt if is_low else number_fmt

#             ws.write(row_idx, 0,  rec.name or '',                                   body_fmt)
#             ws.write(row_idx, 1,  rec.inn_name or '',                               body_fmt)
#             ws.write(row_idx, 2,  rec.brand_name or '',                             body_fmt)
#             ws.write(row_idx, 3,  rec.atc_code or '',                               body_fmt)
#             ws.write(row_idx, 4,  DOSAGE_FORM_MAP.get(rec.dosage_form, ''),        body_fmt)
#             ws.write(row_idx, 5,  rec.strength or '',                               body_fmt)
#             ws.write(row_idx, 6,  ROUTE_MAP.get(rec.route_of_administration, ''),  body_fmt)
#             ws.write(row_idx, 7,  rec.manufacturer_name or '',                      body_fmt)
#             ws.write(row_idx, 8,  STORAGE_MAP.get(rec.storage_condition, ''),      body_fmt)
#             ws.write(row_idx, 9,  rec.shelf_life_months or 0,                       number_fmt)
#             ws.write(row_idx, 10, SCHEDULE_MAP.get(rec.prescription_status, ''),   body_fmt)
#             ws.write(row_idx, 11, rec.x_min_stock_qty or 0,                         number_fmt)
#             ws.write(row_idx, 12,
#                      rec.x_expiry_date.strftime('%Y-%m-%d') if rec.x_expiry_date else '',
#                      body_fmt)
#             ws.write(row_idx, 13, rec.list_price or 0,                              number_fmt)
#             ws.write(row_idx, 14, rec.standard_price or 0,                          number_fmt)
#             ws.write(row_idx, 15, rec.qty_available or 0,                           qty_fmt)

#         # Summary row
#         last_row = len(medicine_records) + 4
#         ws.merge_range(
#             last_row, 0, last_row, col_count - 1,
#             f'Total Medicines Exported: {len(medicine_records)}   |   '
#             f'Low Stock Items: {sum(1 for r in medicine_records if r.qty_available < r.x_min_stock_qty)}',
#             summary_fmt,
#         )

# wizard/prescription_export_wizard.py
# import base64
# from io import BytesIO

# from odoo import models, fields, api, _
# from odoo.exceptions import ValidationError


# class PrescriptionExportWizard(models.TransientModel):
#     _name = 'prescription.export.wizard'
#     _description = 'Export Prescriptions to Excel'

#     from_date = fields.Date(string='From Date', required=True)
#     to_date = fields.Date(string='To Date', required=True)
#     state_filter = fields.Selection([
#         ('all', 'All Prescriptions'),
#         ('delivered', 'Delivered Only'),
#         ('confirmed', 'Confirmed Only'),
#     ], string='Prescription Filter', default='all', required=True)

#     file_data = fields.Binary(string='Excel File', readonly=True)
#     file_name = fields.Char(string='File Name', readonly=True)
#     file_ready = fields.Boolean(string='File Ready', default=False, readonly=True)

#     @api.constrains('from_date', 'to_date')
#     def _check_dates(self):
#         for rec in self:
#             if rec.from_date and rec.to_date and rec.from_date > rec.to_date:
#                 raise ValidationError(_("From Date cannot be after To Date."))

#     def action_export_excel(self):
#         self.ensure_one()
#         domain = [
#             ('date', '>=', self.from_date),
#             ('date', '<=', self.to_date),
#         ]
#         if self.state_filter == 'delivered':
#             domain.append(('state', '=', 'delivered'))
#         elif self.state_filter == 'confirmed':
#             domain.append(('state', '=', 'confirmed'))

#         prescriptions = self.env['prescription'].search(domain, order='date asc')

#         if not prescriptions:
#             raise ValidationError("No prescriptions were found for the selected period and filter.")

#         output = BytesIO()
#         workbook = None

#         try:
#             import xlsxwriter
#             workbook = xlsxwriter.Workbook(output, {'in_memory': True})
#             sheet = workbook.add_worksheet('Prescriptions')

#             header_format = workbook.add_format({
#                 'bold': True,
#                 'border': 1,
#                 'align': 'center',
#                 'valign': 'vcenter',
#             })

#             cell_format = workbook.add_format({
#                 'border': 1,
#             })

#             date_format = workbook.add_format({
#                 'border': 1,
#                 'num_format': 'yyyy-mm-dd',
#             })

#             money_format = workbook.add_format({
#                 'border': 1,
#                 'num_format': '#,##0.00',
#             })

#             headers = [
#                 'Reference',
#                 'Patient Name',
#                 'Doctor',
#                 'Date',
#                 'State',
#                 'Total Amount',
#             ]

#             for col, header in enumerate(headers):
#                 sheet.write(0, col, header, header_format)

#             row = 1
#             for rec in prescriptions:
#                 sheet.write(row, 0, rec.name or '', cell_format)
#                 sheet.write(row, 1, rec.patient_id.name or '', cell_format)
#                 sheet.write(row, 2, rec.doctor_id.name or '', cell_format)
#                 if rec.date:
#                     sheet.write(row, 3, str(rec.date), cell_format)
#                 else:
#                     sheet.write(row, 3, '', cell_format)
#                 sheet.write(row, 4, dict(rec._fields['state'].selection).get(rec.state, rec.state or ''), cell_format)
#                 sheet.write(row, 5, rec.total_amount or 0.0, money_format)
#                 row += 1

#             sheet.set_column('A:A', 20)
#             sheet.set_column('B:B', 25)
#             sheet.set_column('C:C', 25)
#             sheet.set_column('D:D', 15)
#             sheet.set_column('E:E', 20)
#             sheet.set_column('F:F', 15)
#             sheet.set_column('G:G', 15)

#             workbook.close()

#             file_content = output.getvalue()
#             filename = 'prescriptions_%s_to_%s.xlsx' % (self.from_date, self.to_date)

#             self.write({
#                 'file_data': base64.b64encode(file_content),
#                 'file_name': filename,
#                 'file_ready': True,
#             })

#         finally:
#             if workbook:
#                 pass
#             output.close()

#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'prescription.export.wizard',
#             'view_mode': 'form',
#             'res_id': self.id,
#             'target': 'new',
#         }

#     def action_close(self):
#         return {'type': 'ir.actions.act_window_close'}

# -*- coding: utf-8 -*-
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