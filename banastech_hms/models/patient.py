import time
from datetime import datetime
from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


# class ResArea(models.Model):
#     _name = "res.area"

#     name = fields.Char('Area Name', size=64, required=True)
#     city_id = fields.Many2one('res.city', 'City')
#     state_id = fields.Many2one(related='city_id.state_id', string='State')
#     country_id = fields.Many2one(related='city_id.state_id.country_id', string='Country')
#     zip = fields.Char('Zip', size=64)



class HMSDepartment(models.Model):
    _name = "banas.hms.department"
    _description = "HMS Department"
    _rec_name = 'name'

    department_name = fields.Selection([('general','General'),('orthopedic', 'Orthopedic'),('paediatric', 'Paediatric'),('cardiology', 'Cardiology'),('gastroenterology', 'Gastroenterology'),('gynaecology', 'Gynaecology')], string="Linked Department")
    doctor_ids = fields.Many2many('banas.hms.doctor', string='Doctor', required=True)
    name = fields.Char('Department', size=64, required=True)
    active = fields.Boolean("Active", default=True)


class HMSPatientInsurance(models.Model):
    _name = 'banas.hms.patient.insurance'
    _description = "HMS Patient's Insurance"

    patient_id = fields.Many2one('banastech.hms.patient', string='Patient')
    insurance_company = fields.Many2one('res.partner', string ="Insurance Company", domain=[('is_company', '=', True)])
    policy_number = fields.Char(string ="Policy Number")
    insured_value = fields.Float(string ="Insured Value")
    validity = fields.Date(string ="Validity")
    active = fields.Boolean(string ="Active")


    @api.constrains('insured_value')
    def _check_insured_value(self):
        for rec in self:
            if rec.insured_value <= 0.0:
                raise ValidationError("Insured value must be greater than zero !")



class ResPartnerPatient(models.Model):
    _inherit = 'res.partner'
    _description = 'HMS Patient Partner'

    dob = fields.Date(string='Date of Birth')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    age = fields.Char(string='Age')
    language = fields.Selection([('hindi', 'Hindi'),('english', 'English'),('gujarati', 'Gujarati')], string="Languages", default='english')
    marital_status = fields.Selection([('m', 'Married'),
                                       ('u', 'Unmarried'),
                                       ('w', 'Widowed'),
                                       ('d', 'Divorced'),
                                       ('x', 'Separated'),
                                       ('z', 'Live In Relationship'),
                                       ('s', 'Single'),
                                       ],
                                       string='Marital Status', states={'verified': [('readonly', True)]})



class HMSPatient(models.Model):
    _name = 'banastech.hms.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {
          'res.partner': 'partner_id',
          # 'res.users': 'user_id',
    }
    _description = 'HMS Patient'
    _rec_name = 'name'


    @api.model
    def _get_department(self):
        dept = self.env['banas.hms.department'].search([('department_name','=','gastroenterology')],limit=1)
        if dept:
            return dept[0]
        else:
            return False

    @api.model
    def create(self, values):
        if values.get('code', 'New') == 'New':
            values['code'] = self.env['ir.sequence'].next_by_code('banastech.hms.patient') or ''
        res = super(HMSPatient, self).create(values)
        return res


    old_id = fields.Integer(string='Old ID')
    code = fields.Char(string='Patient ID', required=True, default=lambda self: _('New'), track_visibility="onchange", help='Patient Identifier provided by the Health Center.Is not the Social Security Number')
    aadhar_no = fields.Char(string='Aadhar No.', states={'verified': [('readonly', True)]}, track_visibility="onchange")
    active = fields.Boolean(string='Active', states={'verified': [('readonly', True)]}, track_visibility="onchange", help="If unchecked, it will allow you to hide the patient without removing it.",default=True)
    product_id = fields.Many2one('product.template', 'Product', states={'verified': [('readonly', True)]})
    # invoice_id = fields.Many2one('account.invoice',string='Invoice',ondelete='restrict', states={'verified': [('readonly', True)]})
    # total_invoiced = fields.Float(compute="_invoice_total", string="Total Invoiced",groups='base.group_user,account.group_account_invoice')
    is_corpo_tieup = fields.Boolean(string='Corporate Tie-Up', states={'verified': [('readonly', True)]}, track_visibility="onchange", help="If not checked, these Corporate Tie-Up Group will not be visible at all.")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id, track_visibility="onchange",states={'verified': [('readonly', True)]})
    emp_code = fields.Char(string='Employee ID', states={'verified': [('readonly', True)]}, track_visibility="onchange")
    insurance_ids = fields.One2many('banas.hms.patient.insurance','patient_id', string='Insurance', states={'verified': [('readonly', True)]})
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, track_visibility="onchange", states={'verified': [('readonly', True)]})
    user_id = fields.Many2one('res.users', string='Related User', help='User-related data of the patient', track_visibility="onchange")
    image = fields.Image(string='Img', states={'verified': [('readonly', True)]}, track_visibility="onchange")
    age = fields.Char(string='Age', compute='_compute_age', store=True, track_visibility="onchange")
    dob = fields.Date(string='Date Of Birth', states={'verified': [('readonly', True)]}, track_visibility="onchange")
    primary_doctor_id = fields.Many2one('banas.hms.doctor', string="Primary doctor", states={'verified': [('readonly', True)]}, track_visibility="onchange")
    ref_doctor = fields.Many2many('banas.hms.referring.doctor', 'rel_doc_pat', 'doc_id', 'patient_id', string="Referring Doctor", states={'verified': [('readonly', True)]}, track_visibility="onchange")
    refer_type1 = fields.Selection([('advertisement','Advertisement'),
                                    ('camp','Camp'),
                                    ('employee','Employee'),
                                    ('friend','Friend'),
                                    ('patient','Patient'),
                                    ('ref. Dr.','Ref. Dr.'),
                                    ('relative','Relative'),
                                    ('self','Self'),
                                    ('website','Website'),
                                ], string='Referred Type', track_visibility="onchange", states={'verified': [('readonly', True)]})
    #For Basic Medical Info
    blood_group = fields.Selection([('A+', 'A+'),
                                    ('A-', 'A-'),
                                    ('B+', 'B+'),
                                    ('B-', 'B-'),
                                    ('AB+', 'AB+'),
                                    ('AB-', 'AB-'),
                                    ('O+', 'O+'),
                                    ('O-', 'O-')
                                ], string='Blood Group', track_visibility="onchange", states={'verified': [('readonly', True)]})
    critical_info = fields.Text(string='Important disease, allergy or procedures information', track_visibility="onchange", states={'verified': [('readonly', True)]}, help='Write any important information on the patient\'s disease, surgeries, allergies, ...')
    #Diseases
    medical_history = fields.Text(string="Past Medical History", track_visibility="onchange", states={'verified': [('readonly', True)]})
    patient_diseases = fields.One2many('banas.hms.diseases', 'category', string='Diseases', states={'verified': [('readonly', True)]}, help='Mark if the patient has died')
    # Family Form Tab
    genetic_risks = fields.Char(string="Genetic Risks", states={'verified': [('readonly', True)]})
    family_history = fields.Char(string="Family History", states={'verified': [('readonly', True)]}, track_visibility="onchange")
    department_id = fields.Many2one('banas.hms.department', string="Department Id", track_visibility="onchange")
    #language selection
    # language = fields.Many2many('banastech.hms.patient.language', 'banastech_hms_patient_banastech_hms_patient_language_rel', 'banastech_hms_patient_id', 'banastech_hms_patient_language_id', string="Language", track_visibility="onchange", states={'verified': [('readonly', True)]})
    language = fields.Selection([('hindi', 'Hindi'),
                                 ('english', 'English'),
                                 ('gujarati', 'Gujarati')
                                ], string="Language", default='english',  track_visibility="onchange", states={'verified': [('readonly', True)]})
    # area_id = fields.Char(string='Area')
    city_id = fields.Char(string='City', track_visibility="onchange")
    findings = fields.Text(string='Findings', track_visibility="onchange")
    visits = fields.Integer(string='Visits', track_visibility="onchange")
    gender = fields.Selection([('m', 'Male'),
                               ('f', 'Female'),
                               ('o', 'Other')
                            ], string='Gender', track_visibility="onchange", states={'verified': [('readonly', True)]})
    state = fields.Selection([('draft',"Draft"),
                              ('verified',"Verified"),
                            ], string="Status",default="draft",required=True, track_visibility="onchange")
    feet = fields.Float(string='Height(feet)',default=0, states={'verified': [('readonly', True)]}, track_visibility="onchange")
    inch = fields.Float(string='Height(inch)',default=0, states={'verified': [('readonly', True)]}, track_visibility="onchange")
    occupation = fields.Many2one('banastech.hms.patient.occupation', string='Occupation', states={'verified': [('readonly', True)]}, track_visibility="onchange")
    clinical_research = fields.Boolean(string='Clinical Research', states={'verified': [('readonly', True)]}, track_visibility="onchange")
    pan_no = fields.Char(string='PAN No', states={'verified': [('readonly', True)]}, track_visibility="onchange")
    bmi_line_ids = fields.One2many('bmi.records', 'patient_id', string="BMI Records", states={'verified': [('readonly', True)]})
    # mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone", states={'verified': [('readonly', True)]}, track_visibility="onchange")
    email = fields.Char(string="Email", states={'verified': [('readonly', True)]}, track_visibility="onchange")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', track_visibility="onchange")



    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['banastech.hms.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count


    def action_open_banastech_hms_appointment(self):
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'Appointments',
            'res_model' : 'banastech.hms.appointment',
            'domain' : [('patient_id', '=', self.id)],
            'view_mode' : 'tree,form',
            'target' : 'current',
        }

    def create_appointment(self):
        return {
            'res_model' : 'banastech.hms.appointment',
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'view_id' : self.env.ref('banastech_hms.view_banastech_hms_appointment_form').id,
            # 'patient_id': fields.Many2one('Patient', {'readonly': True}),
            # 'attrs' : {'readonly': [('patient_id', '=', True)]},
        }

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            b_date = rec.dob
            delta = relativedelta(datetime.now(), b_date)
            if rec.dob:
                age = _("%sYears %sMonths %sDays") % (delta.years, delta.months, delta.days)
            else:
                age = _("%sYears") % (delta.years)
            rec.age = age

    @api.constrains('dob')
    def check_dob(self):
        for date in self:
            if date.dob >= fields.Datetime.now().date():
                raise ValidationError(_("Date of birth must be greater than or equal to today!"))

    @api.constrains('pan_no')
    def _check_pan_no(self):
        for rec in self:
            if rec.pan_no:
                a = rec.pan_no[0:5]
                b = rec.pan_no[5:9]
                c = rec.pan_no[9:10]
                if rec.pan_no and len(rec.pan_no) == 10:
                    if rec.pan_no.isupper() != True or a.isalpha() != True or c.isalpha() != True or b.isdigit() != True:
                        raise ValidationError(_("Please enter valid format of Pan Card No."))
                else:
                    raise ValidationError(_("Please check the length of Pan Card No."))

    @api.constrains('aadhar_no')
    def _check_aadhar_no(self):
        for rec in self:
            if rec.aadhar_no and len(rec.aadhar_no) != 12:
                raise ValidationError(_("Please enter valid Aadhar Card No."))

    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone and len(rec.phone) != 8:
                raise ValidationError(_("Please enter exact 8 digit number in 'Phone No.'"))

    @api.constrains('mobile')
    def _check_mobile(self):
        for rec in self:
            if rec.mobile and len(rec.mobile) != 10:
                raise ValidationError(_("Please enter exact 10 digit number in 'Mobile No.'"))

    def verified_state(self):
        for rec in self:
            rec.state = 'verified'

    def draft_state(self):
        for rec in self:
            rec.state = 'draft'

    # def write(self, values):
    #     if not self.ref_doctor and not values.get('ref_doctor'):
    #         values['ref_doctor'] =
    #     return super(HMSPatient, self).write(values)



class ResCity(models.Model):
    _name = "res.city"
    _description = "City"


    name = fields.Char(string='City Name')
    # state_id = fields.Many2one(related='name.state_id', string='State Name')
    # country_id = fields.Many2one(related='state_id.country_id', string='Country')


    @api.model
    def action_banastech_hms_appointment(self):
        return {
            'name': _('Appointments'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'banastech.hms.appointment',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id','=',self.id)],
            'context': {
                        'default_patient_id': self.id,
                        # 'default_physician_id':self.primary_doctor_id.id,
                        # 'default_urgency':'a',
                        'default_department_id':self.department_id.id,
                        # 'default_ref_doctor':self.ref_doctor[0].id,
                        },
        }

class BMIRecord(models.Model):
    _name = 'bmi.records'
    _description = 'BMI Record'

    patient_id = fields.Many2one('banastech.hms.patient', string="Patient")
    bmi_date = fields.Date(string="Date", default=datetime.now())
    weight = fields.Float('Weight(kg)')
    cm = fields.Float('Height(cm)', digits=(16,2))
    bmi = fields.Float('BMI', compute="_get_bmi", digits=(16,2), store=True)

    @api.depends('cm','weight')
    def _get_bmi(self):
        for rec in self:
            if rec.cm:
                rec.bmi = round((float(rec.weight) / ((float(rec.cm) / 100) ** 2)),2)

    @api.constrains('weight')
    def _check_weight(self):
        for rec in self:
            if rec.weight <= 0.0:
                raise ValidationError("Weight must be greater than zero !")

    @api.constrains('cm')
    def _check_height(self):
        for rec in self:
            if rec.cm <= 0.0:
                raise ValidationError("Height must be greater than zero !")


class HMSPatientOccupation(models.Model):
    _name = 'banastech.hms.patient.occupation'
    _description = "HMS Patient's Occupation"

    name = fields.Char('Occupation Name')


class HMSPatientLangauge(models.Model):
    _name = 'banastech.hms.patient.language'
    _description = "HMS Patient's Language"

    language = fields.Char('Language')