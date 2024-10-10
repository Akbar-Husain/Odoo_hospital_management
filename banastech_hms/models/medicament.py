from odoo import api, fields, models
from odoo.tools.translate import _

class HMSMedicamentGroupLine(models.Model):
    _name = "banas.hms.medicament.group.line"
    _rec_name = 'line_id'

    line_id = fields.Many2one('medicament.group', string='Medicament Group')
    abbriviation_code = fields.Char(related="line_id.name",string="Med Group Name",store=True)
    template = fields.Many2one('product.template', ondelete='restrict', string='Medicine Name')
    template_name = fields.Char(related='template.name',string="Template")
    product_id = fields.Many2one('product.product', string='Medicine Name',domain=[('hospital_product_type', '=', 'medicament')])
    indication = fields.Many2one('banas.hms.diseases', ondelete='cascade',string='Disease', help='Choose a disease for this medicament from the disease list. It'\
    ' can be an existing disease of the patient or a prophylactic.')
    allow_substitution = fields.Boolean(string='Allow substitution')
    prnt = fields.Boolean(string='Print', help='Check this box to print this line of the prescription.')
    quantity = fields.Integer(string='Units',  help="Number of units of the medicament. Example : 30 capsules of amoxicillin")
    active_component_ids = fields.Many2many('banas.hms.active.comp','medica_group_comp_rel','medica_id','group_id',string='Active Component')
    start_treatment = fields.Datetime(string='Start Date')
    end_treatment = fields.Datetime(string='End Date')
    dose = fields.Float(string='Dosage', digits=(16, 2), help="Amount of medication (eg, 250 mg) per dose")
#     dose_unit = fields.Many2one('product.uom', ondelete='restrict', string='Dosage Unit', help='Amount of medication (eg, 250 mg) per dose')
    qty = fields.Integer(string='x')
    form = fields.Many2one('drug.form', string='Form', help='Drug form, such as tablet or gel')
    route = fields.Many2one('drug.route', string='Route', help='Drug route, such as tablet or gel')
    common_dosage = fields.Many2one('banas.hms.medication.dosage', string='Frequency', help='Drug form, such as tablet or gel')
    admin_times = fields.Char(string='Admin Hours', size=255)
    frequency = fields.Integer(string='Frequency')
    frequency_unit = fields.Selection([
    ('none', '-'),
    ('seconds', 'seconds'),
    ('minutes', 'minutes'),
    ('hours', 'hours'),
    ('days', 'days'),
    ('weeks', 'weeks'),
    ('wr', 'when required'),
    ],string='Unit')
    frequency_prn = fields.Boolean(string='Frequency prn', help='')
    duration = fields.Integer(string='Treatment duration')
    duration_period = fields.Selection([
        ('none', '-'),
        ('minutes', 'minutes'),
        ('hours', 'hours'),
        ('days', 'days'),
        ('months', 'months'),
        ('years', 'years'),
        ('indefinite', 'indefinite')],string='Treatment period')
    refills = fields.Integer(string='Refills #')
    review = fields.Datetime(string='Review')
    short_comment = fields.Char(size=256, string='Comment', help='Short comment on the specific drug')
    days = fields.Integer('Days', default=0)

    @api.onchange('product_id','common_dosage','days')
    @api.model
    def onchange_product_id(self):
        if self.product_id:
            self.common_dosage = self.product_id.common_dosage.id 
            self.days = self.product_id.days 
            self.quantity = float(self.common_dosage.code) * self.days


class HMSMedicamentGroup(models.Model):
    _name = "medicament.group"
    _rec_name = 'name'

    @api.model
    def _merge_name_prescription(self):
        score_details = []
        for data in self.medicine_list:
            if data.product_id:
                score_details.append(data.product_id.name)
        score_details = ','.join(score_details)
        self.display_name = score_details

    name = fields.Char(string='Group Name', required=True)
    doctor_id = fields.Many2one('banas.hms.doctor', ondelete='set null', string='Doctor')
    diseases_id = fields.Many2one('banas.hms.diseases', ondelete='set null', string='Diseases')
    medicine_list = fields.One2many('banas.hms.medicament.group.line', 'line_id', string='Medicament line')
    limit = fields.Integer('Limit')
    display_name = fields.Char(compute=_merge_name_prescription, string='Display')


class product_template(models.Model):
    _inherit = "product.template"

    side = fields.Selection([('none', 'None'), ('right', 'Right'), ('left', 'Left'), ('both', 'Both')], default="none", help="Radiology Attribute")
    plate = fields.Selection([('8x10', '08 x 10'), ('14x11', '14 x 11'), ('paper', 'Paper'), ('other', 'Other')], default="8x10", help="Radiology Attribute")
    suffix_frequency_id = fields.Many2one('banas.hms.medication.dosage', string='Suffix Frequency')
    content_ids = fields.Many2many('banas.hms.medicament.content', 'medicament_content_rel', 'template_id', 'content_id', 'Generic')
    days = fields.Integer('Days', default=0)
    special_day_price = fields.Float('Special Day Charges(-)')
    reg_spe_price = fields.Float('Regular or Special Charges(-)')
    day_price = fields.Float("Day Emergency")
    night_price = fields.Float("Night Emergency")
    # attend_std_price = fields.Float('Attending Standard Charges')
#     std_disc = fields.Float('Standard Charges Disc.(%)')
#     attend_outside_price = fields.Float('Attending Outside Charges')
#     outside_disc = fields.Float('Outside Charges Disc.(%)')
#     attend_doctor_price = fields.Float('Attending Doctor Charges')
#     doctor_disc = fields.Float('Doctor Charges Disc.(%)')
#     treat_std_price = fields.Float('Treating Standard Charges')
#     treat_outside_price = fields.Float('Treating Outside Charges')
#     treat_doctor_price = fields.Float('Treating Doctor Charges')
#     ksga_price = fields.Float('KSGA')
#     hospital_share = fields.Float('Hospital Share')
    file_price = fields.Float("File Opinion")
    is_medicines = fields.Boolean(string='Medicines', help='Check if the product is a medicament')
    is_bed = fields.Boolean(string='Bed', help='Check if the product is a bed on the gnuhealth.center')
    is_vaccine = fields.Boolean(string='Vaccine', help='Check if the product is a vaccine')
    is_medical_supply = fields.Boolean(string='Medical Supply', help='Check if the product is a medical supply')
    is_insurance_plan = fields.Boolean(string='Insurance Plan', help='Check if the product is an insurance plan')
    hospital_product_type = fields.Selection([('medicament','Medicament'),
                                                 ('prescription','Prescription'),
                                                 ('registration', 'Registration'),
                                                 ('msupply', 'Medical Supply'),
                                                 ('bed', 'Bed'), 
                                                 ('consultation','Consultation'),
                                                 ('surgery', 'Surgery'), 
                                                 ('procedure', 'Procedure'),
                                                 ('fdrinks', 'Food & Drinks'),
                                                 ('lithotripsy', 'Lithotripsy'),
                                                 ('physiotherapy','Physiotherapy'),
                                                 ('vaccination','Vaccination'),
                                                 ('pathology', 'Pathology'), 
                                                 ('radiology', 'Radiology'),
                                                 ('manometry', 'Manometry'),
                                                 ('endoscopy', 'Endoscopy'),
                                                 ('os', 'Other Service'),
                                                 ('consultation_paediatric','Consultation Paediatric')], 
                                             string="Hospital Product Type",default='medicament')
    #Medicamnet relate fields
    active_component = fields.Char(string='Active component', help='Active Component')
    indications = fields.Text(string='Indication', help='Indications') 
    therapeutic_action = fields.Char(size=256, string='Therapeutic Effect', help='Therapeutic action')
    pregnancy_category = fields.Selection([
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('X', 'X'),
    ('N', 'N'),
    ], string='Pregnancy Category', 
    help='** FDA Pregancy Categories ***\n'\
    'CATEGORY A :Adequate and well-controlled human studies have failed'\
    ' to demonstrate a risk to the fetus in the first trimester of'\
    ' pregnancy (and there is no evidence of risk in later'\
    ' trimesters).\n\n'\
    'CATEGORY B : Animal reproduction studies have failed todemonstrate a'\
    ' risk to the fetus and there are no adequate and well-controlled'\
    ' studies in pregnant women OR Animal studies have shown an adverse'\
    ' effect, but adequate and well-controlled studies in pregnant women'\
    ' have failed to demonstrate a risk to the fetus in any'\
    ' trimester.\n\n'
    'CATEGORY C : Animal reproduction studies have shown an adverse'\
    ' effect on the fetus and there are no adequate and well-controlled'\
    ' studies in humans, but potential benefits may warrant use of the'\
    ' drug in pregnant women despite potential risks. \n\n '\
    'CATEGORY D : There is positive evidence of human fetal  risk based'\
    ' on adverse reaction data from investigational or marketing'\
    ' experience or studies in humans, but potential benefits may warrant'\
    ' use of the drug in pregnant women despite potential risks.\n\n'\
    'CATEGORY X : Studies in animals or humans have demonstrated fetal'\
    ' abnormalities and/or there is positive evidence of human fetal risk'\
    ' based on adverse reaction data from investigational or marketing'\
    ' experience, and the risks involved in use of the drug in pregnant'\
    ' women clearly outweigh potential benefits.\n\n'\
    'CATEGORY N : Not yet classified')

    overdosage = fields.Char(string='Overdosage', help='Overdosage')
    pregnancy_warning = fields.Boolean(string='Pregnancy Warning',help='The drug represents risk to pregnancy or lactancy')
    notes = fields.Text(string='Extra Info')
    storage = fields.Char(string='Storage')
    adverse_reaction = fields.Char(string='Adverse Reactions')
    dosage = fields.Float(string='Dosage', help='Dosage')
#     dose_unit = fields.Many2one('product.uom', ondelete='restrict', string='Dosage Unit', help='Dose Unit')
    pregnancy = fields.Text(string='Pregnancy and Lactancy',help='Warnings for Pregnant Women')
    presentation = fields.Char(string='Presentation')
    composition = fields.Char(string='Composition')
    base_condition = fields.Many2one("banas.hms.diseases", ondelete='cascade', string="Base Condition")
    route = fields.Many2one('banas.hms.drug.route', string='Route', help='Drug route, such as tablet or gel')
    form = fields.Many2one('banas.hms.drug.form', string='Form',help='Drug form, such as tablet or gel')
    common_dosage = fields.Many2one('banas.hms.medication.dosage', ondelete='cascade', string='Frequency', help='Drug form, such as tablet or gel')
    department_type = fields.Selection([('orthopedic','Orthopedic'),
                                        ('pediatrics', 'Pediatrics'),
                                        ('both', 'Both'),
                                        ], string="Department",default='orthopedic')
    department_ids = fields.Many2many('banas.hms.department', 'medicament_department_rel', 'template_id', 'department_id', 'Departments')
# #     department_type = fields.Selection(related="department_id.department_name",string="Department")
    used_in = fields.Selection([('ipd','IPD'),
                                ('opd', 'OPD'),
                                ('both', 'Both')], string="Used In",default='opd')
    product_exception = fields.Selection([('yes','Yes'),('no','No')],string="Exception", default='no')
    # line_id = fields.Many2one('medicament.group', ondelete='restrict', string='Medicament Group')
    
    abbriviation_code = fields.Char(related="common_dosage.abbreviation",string="Abbriviation Code",store=True)
#     is_lactation = fields.Selection([('yes','Yes'),('no','No')],string="Lactation", default='yes')
#     is_pregnancy = fields.Selection([('yes','Yes'),('no','No')],string="Pregnancy", default='yes')
    no_per_pack = fields.Float('No per Pack')
    service_type_ids = fields.One2many('banas.hms.service.type','pro_id','Service Type')



class ProductProduct(models.Model):
    _inherit = "product.product"

    med_group_ids = fields.One2many('banas.hms.medicament.group.line', 'product_id', 'Medicament Groups')
    


class HMSServiceType(models.Model):
    _name="banas.hms.service.type"
    _description = 'HMS Service Type'
    
    service_type = fields.Selection([('hospital','Hospital'),
                                     ('primary_consultation','Primary Consultation'),
                                     ('secondary_consultation','Secondary Consultation'),
                                     ('referred','Referred')],'Service type')
    percent_service = fields.Float('Percent(%)')
    pro_id = fields.Many2one('product.template',string='Product')
