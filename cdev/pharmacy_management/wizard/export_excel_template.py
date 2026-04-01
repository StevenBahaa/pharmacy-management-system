# -*- coding: utf-8 -*-
from odoo import models


class PrescriptionXlsxReport(models.AbstractModel):
    _name = 'report.pharmacy_management.report_prescription_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Prescription Excel Export Report'

    def generate_xlsx_report(self, workbook, data, records):

        from_date    = data.get('from_date')
        to_date      = data.get('to_date')
        state_filter = data.get('state_filter', 'all')

        # Build domain
        domain = [
            ('date', '>=', from_date),
            ('date', '<=', to_date),
        ]
        if state_filter == 'delivered':
            domain.append(('state', '=', 'delivered'))
        elif state_filter == 'confirmed':
            domain.append(('state', '=', 'confirmed'))

        prescriptions = self.env['prescription'].search(
            domain, order='date asc'
        )

        # ── Formats ──────────────────────────────────────────────────────────
        title_fmt = workbook.add_format({
            'bold': True, 'font_name': 'Arial', 'font_size': 14,
            'font_color': '#FFFFFF', 'bg_color': '#1F7A4A',
            'align': 'center', 'valign': 'vcenter',
        })
        subtitle_fmt = workbook.add_format({
            'italic': True, 'font_name': 'Arial', 'font_size': 9,
            'font_color': '#FFFFFF', 'bg_color': '#1E4A8C',
            'align': 'center', 'valign': 'vcenter',
        })
        header_fmt = workbook.add_format({
            'bold': True, 'font_name': 'Arial', 'font_size': 10,
            'font_color': '#FFFFFF', 'bg_color': '#1E4A8C',
            'align': 'center', 'valign': 'vcenter',
            'border': 1, 'text_wrap': True,
        })
        body_fmt = workbook.add_format({
            'font_name': 'Arial', 'font_size': 10,
            'align': 'left', 'valign': 'vcenter', 'border': 1,
        })
        money_fmt = workbook.add_format({
            'font_name': 'Arial', 'font_size': 10,
            'align': 'right', 'valign': 'vcenter',
            'border': 1, 'num_format': '#,##0.00',
        })
        summary_fmt = workbook.add_format({
            'bold': True, 'font_name': 'Arial', 'font_size': 10,
            'font_color': '#FFFFFF', 'bg_color': '#1F7A4A',
            'align': 'left', 'valign': 'vcenter', 'border': 1,
        })

        # ── Worksheet ────────────────────────────────────────────────────────
        ws = workbook.add_worksheet('Prescriptions')
        ws.freeze_panes(4, 0)
        ws.set_zoom(90)

        HEADERS = [
            ('Reference',    20),
            ('Patient',      24),
            ('Doctor',       24),
            ('Date',         14),
            ('State',        16),
            ('Total Amount', 16),
        ]
        col_count = len(HEADERS)

        # Row 0 — Title
        ws.merge_range(0, 0, 0, col_count - 1,
                       'Al-Shifa Pharmacy — Prescriptions Report', title_fmt)
        ws.set_row(0, 36)

        # Row 1 — Subtitle
        ws.merge_range(1, 0, 1, col_count - 1,
                       f'Period: {from_date}  →  {to_date}   |   '
                       f'Filter: {state_filter.title()}', subtitle_fmt)
        ws.set_row(1, 20)

        # Row 2 — blank spacer
        ws.set_row(2, 6)

        # Row 3 — Headers
        ws.set_row(3, 32)
        for col, (header, width) in enumerate(HEADERS):
            ws.write(3, col, header, header_fmt)
            ws.set_column(col, col, width)

        # Rows 4+ — Data
        state_labels = {
            'draft': 'Draft',
            'confirmed': 'Confirmed',
            'delivered': 'Delivered',
        }

        for row_idx, rec in enumerate(prescriptions, start=4):
            ws.set_row(row_idx, 20)
            ws.write(row_idx, 0, rec.name or '',                        body_fmt)
            ws.write(row_idx, 1, rec.patient_id.name or '',             body_fmt)
            ws.write(row_idx, 2, rec.doctor_id.name or '',              body_fmt)
            ws.write(row_idx, 3, str(rec.date) if rec.date else '',     body_fmt)
            ws.write(row_idx, 4, state_labels.get(rec.state, ''),       body_fmt)
            ws.write(row_idx, 5, rec.total_amount or 0.0,               money_fmt)

        # Summary row
        total = sum(rec.total_amount for rec in prescriptions)
        last_row = len(prescriptions) + 4
        ws.merge_range(
            last_row, 0, last_row, col_count - 1,
            f'Total Prescriptions: {len(prescriptions)}   |   '
            f'Grand Total: {total:,.2f}',
            summary_fmt,
        )