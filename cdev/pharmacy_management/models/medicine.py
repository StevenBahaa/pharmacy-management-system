from odoo import models, fields, api, _
from odoo.exceptions import ValidationError , UserError
from datetime import date
import re

DOSAGE_FORM_SELECTION = [
    # Solid oral
    ('tablet',          'Tablet'),
    ('tablet_er',       'Tablet, Extended Release'),
    ('tablet_ec',       'Tablet, Enteric Coated'),
    ('capsule',         'Capsule'),
    ('capsule_er',      'Capsule, Extended Release'),
    ('powder_oral',     'Powder for Oral Solution'),
    ('granule',         'Granules'),
    # Liquid oral
    ('syrup',           'Syrup'),
    ('suspension_oral', 'Oral Suspension'),
    ('solution_oral',   'Oral Solution'),
    ('drops_oral',      'Oral Drops'),
    ('effervescent',    'Effervescent Tablet'),
    # Parenteral
    ('injection_iv',    'Injection — Intravenous'),
    ('injection_im',    'Injection — Intramuscular'),
    ('injection_sc',    'Injection — Subcutaneous'),
    ('infusion',        'Infusion (IV Bag)'),
    ('powder_inj',      'Powder for Injection'),
    # Topical / Transdermal
    ('cream',           'Cream'),
    ('ointment',        'Ointment'),
    ('gel',             'Gel'),
    ('patch',           'Transdermal Patch'),
    ('lotion',          'Lotion'),
    ('spray_topical',   'Topical Spray'),
    # Inhalation
    ('inhaler_mdi',     'Metered Dose Inhaler (MDI)'),
    ('inhaler_dpi',     'Dry Powder Inhaler (DPI)'),
    ('nebulizer',       'Nebulizer Solution'),
    # Ophthalmic / Otic / Nasal
    ('eye_drops',       'Eye Drops'),
    ('eye_ointment',    'Eye Ointment'),
    ('ear_drops',       'Ear Drops'),
    ('nasal_spray',     'Nasal Spray'),
    ('nasal_drops',     'Nasal Drops'),
    # Rectal / Vaginal
    ('suppository',     'Suppository'),
    ('enema',           'Enema'),
    ('vaginal_tab',     'Vaginal Tablet'),
    ('vaginal_cream',   'Vaginal Cream'),
    # Other
    ('lozenge',         'Lozenge / Troche'),
    ('sublingual',      'Sublingual Tablet'),
    ('implant',         'Implant'),
    ('other',           'Other (specify in notes)'),
]

ROUTE_SELECTION = [
    ('oral',            'Oral (PO)'),
    ('sublingual',      'Sublingual (SL)'),
    ('buccal',          'Buccal'),
    ('intravenous',     'Intravenous (IV)'),
    ('intramuscular',   'Intramuscular (IM)'),
    ('subcutaneous',    'Subcutaneous (SC)'),
    ('intradermal',     'Intradermal (ID)'),
    ('inhalation',      'Inhalation'),
    ('topical',         'Topical'),
    ('transdermal',     'Transdermal'),
    ('ophthalmic',      'Ophthalmic'),
    ('otic',            'Otic'),
    ('nasal',           'Nasal'),
    ('rectal',          'Rectal (PR)'),
    ('vaginal',         'Vaginal'),
    ('epidural',        'Epidural'),
    ('intrathecal',     'Intrathecal'),
    ('other',           'Other'),
]

SCHEDULE_SELECTION = [
    ('otc',    'OTC — Over the Counter'),
    ('rx',     'Rx — Prescription Only'),
    ('ci',     'Schedule I — High Abuse Potential, No Accepted Use'),
    ('cii',    'Schedule II — High Abuse Potential, Accepted Use'),
    ('ciii',   'Schedule III — Moderate Abuse Potential'),
    ('civ',    'Schedule IV — Low Abuse Potential'),
    ('cv',     'Schedule V — Lowest Abuse Potential'),
]

STORAGE_TEMP_SELECTION = [
    ('room',    'Room Temperature (15–25 °C)'),
    ('cool',    'Cool (8–15 °C)'),
    ('refrig',  'Refrigerated (2–8 °C)'),
    ('frozen',  'Frozen (≤ −10 °C)'),
    ('protect', 'Protect from Light'),
    ('dry',     'Store Dry (< 40% RH)'),
    ('other',   'See Labeling'),
]

REGISTRATION_AUTHORITY_SELECTION = [
    ('fda_us',  'FDA — United States'),
    ('ema',     'EMA — European Medicines Agency'),
    ('who',     'WHO Prequalification'),
    ('mhra',    'MHRA — United Kingdom'),
    ('tga',     'TGA — Australia'),
    ('pmda',    'PMDA — Japan'),
    ('nmpa',    'NMPA — China'),
    ('local',   'Local National Authority'),
    ('other',   'Other'),
]

class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_medicine_category = fields.Boolean(string='Is Medicine Category', default=False, help='Check if this category classifies medicines.')
    code = fields.Char(string='ATC Code Prefix', help='ATC code reference (e.g., N02).')
    requires_prescription = fields.Boolean(string='Requires Prescription', default=False)
    is_controlled = fields.Boolean(string='Is Controlled Substance', default=False)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_medicine = fields.Boolean(
        string='Is Medicine',
        default=False,
        index=True,
        help='Enable pharmaceutical fields for this product.',
    )

    medicine_category_id = fields.Many2one(
        'product.category',
        string='Medicine Category',
        domain="[('is_medicine_category', '=', True)]",
        index=True,
        ondelete='restrict',
        help='ATC-aligned medicine category shown in POS button grid.',
    )

    inn_name = fields.Char(
        string='INN / Generic Name',
        index=True,
        help='WHO International Nonproprietary Name (generic, non-branded).',
    )

    brand_name = fields.Char(
        string='Brand / Trade Name',
        help='Proprietary name as registered by the manufacturer.',
    )

    atc_code = fields.Char(
        string='ATC Code',
        size=10,
        help='Full WHO ATC code (e.g. A02BC01 = Omeprazole).',
    )

    dosage_form = fields.Selection(
        selection=DOSAGE_FORM_SELECTION,
        string='Dosage Form',
        help='Physical form as per WHO/FDA classification.',
    )

    active_ingredient = fields.Text(
        string='Active Ingredient(s)',
        help='List each ingredient with quantity per unit dose.',
    )

    excipients = fields.Text(
        string='Excipients / Inactive Ingredients',
        help='Relevant excipients — especially those with known risk (e.g. lactose, benzyl alcohol).',
    )

    route_of_administration = fields.Selection(
        selection=ROUTE_SELECTION,
        string='Route of Administration',
        help='Primary route; add secondary in notes if applicable.',
    )

    registration_authority = fields.Selection(
        selection=REGISTRATION_AUTHORITY_SELECTION,
        string='Registration Authority',
    )

    registration_number = fields.Char(
        string='Registration / MA Number',
        help='Marketing Authorisation or Drug Registration Number.',
    )

    manufacturer_name = fields.Char(
        string='Manufacturer',
        help='Full legal name of the manufacturing entity.',
    )

    manufacturer_country = fields.Many2one(
        'res.country',
        string='Country of Manufacture',
    )

    strength = fields.Char(
        string='Strength / Concentration',
        help='USP convention: "500 mg", "10 mg/5 mL", "0.1% w/v".',
    )
    
    storage_condition = fields.Selection(
        selection=STORAGE_TEMP_SELECTION,
        string='Storage Condition',
        help='ICH Q1A(R2) compliant storage requirement.',
    )

    shelf_life_months = fields.Integer(
        string='Shelf Life (months)',
        help='Approved shelf life from manufacture date.',
    )

    storage_notes = fields.Char(
        string='Additional Storage Notes',
        help='e.g. "Keep away from children", "Do not freeze after reconstitution".',
    )

    expiry_warning_days = fields.Integer(
        string='Expiry Warning (days before)',
        default=90,
        help='System alert N days before expiry date.',
    )

    pack_size = fields.Char(
        string='Pack Size / Quantity',
        help='e.g. "30 tablets", "100 mL", "10 × 1 mL ampoules".',
    )

    prescription_status = fields.Selection(
        selection=SCHEDULE_SELECTION,
        string='Prescription / Schedule Status',
        default='otc',
        help='Regulatory classification for dispensing control.',
    )

    pregnancy_category = fields.Selection(
        selection=[
            ('a',   'Category A — No risk in controlled studies'),
            ('b',   'Category B — No risk in animal studies'),
            ('c',   'Category C — Risk cannot be ruled out'),
            ('d',   'Category D — Evidence of risk'),
            ('x',   'Category X — Contraindicated in pregnancy'),
            ('na',  'N/A'),
        ],
        string='Pregnancy Category',
        default='na',
    )
    
    is_controlled_substance = fields.Boolean(
        string='Controlled',
        compute='_compute_controlled_substance',
        store=True,
    )

    medicine_display_name = fields.Char(
        string='Display',
        compute='_compute_medicine_display_name',
        store=True,
    )

    requires_double_check = fields.Boolean(string='Requires Double Check')


    x_min_stock_qty = fields.Float(string='Minimum Stock Quantity')
    x_requires_prescription = fields.Boolean(string='Requires Prescription')
    x_is_low_stock = fields.Boolean(
        compute="_compute_is_low_stock",
        store=True
    )

    @api.constrains('x_min_stock_qty')
    def _check_min_stock_qty(self):
        for rec in self :
            if rec.x_min_stock_qty and rec.x_min_stock_qty < 0 :
                raise UserError("The Minimum Stock Quantity should not be negative")


    @api.constrains('x_expiry_date')
    def _check_expiry_date(self):
        today = date.today()
        for rec in self:
            if rec.x_expiry_date and rec.x_expiry_date < today : 
                raise UserError("The expire date cannot be in the past")

    @api.depends('qty_available', 'x_min_stock_qty')
    def _compute_is_low_stock(self):
        for rec in self:
            rec.x_is_low_stock = (
                rec.is_medicine and rec.qty_available < rec.x_min_stock_qty
            )


    @api.depends('prescription_status')
    def _compute_controlled_substance(self):
        controlled = {'ci', 'cii', 'ciii', 'civ', 'cv'}
        for rec in self:
            rec.is_controlled_substance = rec.prescription_status in controlled

    @api.depends('inn_name', 'brand_name', 'strength', 'dosage_form')
    def _compute_medicine_display_name(self):
        form_map = dict(DOSAGE_FORM_SELECTION)
        for rec in self:
            if not rec.is_medicine:
                rec.medicine_display_name = rec.name
                continue
            parts = filter(None, [
                rec.inn_name or rec.brand_name,
                rec.strength,
                form_map.get(rec.dosage_form, ''),
            ])
            rec.medicine_display_name = ' '.join(parts) or rec.name

    @api.onchange('inn_name')
    def _onchange_inn_name(self):
        """Auto-fill product name from INN if name field is still blank."""
        if self.inn_name and not self.name:
            self.name = self.inn_name.strip().title()

    @api.onchange('medicine_category_id', 'is_medicine')
    def _onchange_medicine_category(self):
        """Inherit prescription default from category."""
        if self.medicine_category_id:
            if self.medicine_category_id.requires_prescription:
                self.prescription_status = 'rx'
            if self.medicine_category_id.is_controlled:
                self.requires_double_check = True
            # Sync ATC category code hint
            if self.medicine_category_id.code and not self.atc_code:
                self.atc_code = self.medicine_category_id.code
            
            # Use the selected medicine category as the main product category
            self.categ_id = self.medicine_category_id
        elif self.is_medicine:
            # Fallback to the base medicine category if no specific one is chosen
            self.categ_id = self.env.ref('pharmacy_management.product_category_medicine', raise_if_not_found=False)

    @api.onchange('tracking')
    def _onchange_lot_tracking(self):
        """Enforce lot tracking for controlled substances."""
        # Note: product.template has 'tracking' natively instead of 'lot_tracking' in recent versions.
        if self.is_controlled_substance and self.tracking == 'none':
            self.tracking = 'lot'
            return {
                'warning': {
                    'title': _('Lot Tracking Required'),
                    'message': _(
                        'Controlled substances must have lot/batch tracking enabled '
                        'to comply with regulatory chain-of-custody requirements.'
                    ),
                }
            }

    @api.constrains('is_medicine', 'inn_name', 'dosage_form',
                    'strength', 'route_of_administration', 'medicine_category_id',
                    'manufacturer_name')
    def _check_medicine_completeness(self):
        required_map = {
            'inn_name':                 'INN / Generic Name',
            'dosage_form':              'Dosage Form',
            'strength':                 'Strength / Concentration',
            'route_of_administration':  'Route of Administration',
            'medicine_category_id':     'Medicine Category',
            'manufacturer_name':        'Manufacturer',
        }
        for rec in self:
            if not rec.is_medicine:
                continue
            missing = [
                label for field, label in required_map.items()
                if not getattr(rec, field)
            ]
            if missing:
                raise ValidationError(
                    _('The following required pharmaceutical fields are missing for "%s":\n• %s')
                    % (rec.name or '(unnamed)', '\n• '.join(missing))
                )

    @api.constrains('inn_name')
    def _check_inn_name_quality(self):
        for rec in self:
            if not rec.inn_name:
                continue
            cleaned = rec.inn_name.strip()
            if cleaned != rec.inn_name:
                raise ValidationError(
                    _('INN name must not have leading or trailing whitespace: "%s"') % rec.inn_name
                )
            if '®' in cleaned or '™' in cleaned:
                raise ValidationError(
                    _('INN / Generic name must not contain trademark symbols (® ™). '
                      'Use Brand Name field for trade names: "%s"') % cleaned
                )
            if len(cleaned) < 2:
                raise ValidationError(
                    _('INN name is too short: "%s"') % cleaned
                )

    @api.constrains('strength')
    def _check_strength_format(self):
        pattern = re.compile(
            r'^\d+(\.\d+)?\s*'          # leading number
            r'(mg|g|mcg|µg|mmol|mEq|'   # mass units
            r'mL|L|IU|units?|%|'         # volume / percent
            r'mg/\d+\s*mL|'             # concentration
            r'\d+:\d+)',                  # ratio
            re.IGNORECASE
        )
        for rec in self:
            if rec.is_medicine and rec.strength:
                if not pattern.match(rec.strength.strip()):
                    raise ValidationError(
                        _('Strength "%s" does not match pharmaceutical convention.\n'
                          'Expected formats: "500 mg", "10 mg/5 mL", "0.1%% w/v".')
                        % rec.strength
                    )

    @api.constrains('atc_code')
    def _check_atc_code_format(self):
        pattern = re.compile(r'^[A-Z]\d{2}[A-Z]{2}\d{2}$')
        for rec in self:
            if rec.atc_code:
                code = rec.atc_code.strip().upper()
                if not pattern.match(code):
                    raise ValidationError(
                        _('ATC code "%s" is invalid. '
                          'Full format: A02BC01 (1 letter, 2 digits, 2 letters, 2 digits).')
                        % rec.atc_code
                    )

    @api.constrains('shelf_life_months')
    def _check_shelf_life(self):
        for rec in self:
            if rec.is_medicine and rec.shelf_life_months and rec.shelf_life_months <= 0:
                raise ValidationError(
                    _('Shelf life must be a positive number of months.')
                    )
                
    @api.constrains('is_controlled_substance', 'tracking')
    def _check_controlled_lot_tracking(self):
        for rec in self:
            if rec.is_controlled_substance and rec.tracking == 'none':
                raise ValidationError(
                    _('Lot/Batch tracking is mandatory for controlled substances.')
                    )