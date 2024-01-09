import time
from datetime import date
from odoo import api, fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import SUPERUSER_ID, models
import odoo


class HMSDoctorSpeciality(models.Model):
    _name = 'doctor.speciality'
    _description = "HMS Doctor's Speciality"

    code = fields.Char(size=256, string='Code')
    name = fields.Char(size=256, string='Speciality', required=True, translate=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]


class HMSDoctorDegree(models.Model):
    _name = 'banas.hms.doctor.degree'
    _description = "HMS Doctor's Degree"

    name = fields.Char(string='Degree')


class HMSDoctors(models.Model):
    _name = 'banas.hms.doctor'
    _inherits = {
        'res.partner' : 'partner_id'
    }
    _description = "HMS Doctor"

    user_id = fields.Many2one('res.users', string='Related User', required=False, help='User-related data of the doctor')
    partner_id = fields.Many2one('res.partner', string='Related Partner', required=False, help='Partner-related data of the doctor')
    code = fields.Char(string='Code', readonly=True, default=lambda self: _('New'))
    active = fields.Boolean(string='Active', help="If unchecked, it will allow you to hide the physician without removing it.", default=True)
    age = fields.Char(string='Age')
    relation = fields.Char(string='Husband of / Wife of')
    degree_ids = fields.Many2many('banas.hms.doctor.degree', 'banas_hms_doctor_degree_rel', 'doctor_id' 'degree_ids', string='Tags')
    speciality = fields.Many2one('doctor.speciality', ondelete='set null', string='Speciality', help='Speciality Code')
    government_id = fields.Char(string='Government ID')
    patient_id = fields.Many2one('banastech.hms.patient', ondelete='restrict', string='Patient')
    consul_service = fields.Many2one('product.product', ondelete='restrict', string='Consultation Service')
    consul_charge = fields.Integer('Consultation Charge')
    is_primary_surgeon = fields.Boolean(string='Primary Surgeon')
    is_consultation_doctor = fields.Boolean(string='Consultation Doctor')
    signature = fields.Binary('Signature')
    department_ids = fields.Many2many('banas.hms.department', 'banas_hms_doctor_department_rel', 'doctor_id', 'department_id', string='Departments')
    reg_number = fields.Char(string='Reg. No.')
    image = fields.Image(string='Image')
    cabin_no = fields.Selection([
                                 ('1','1'),
                                 ('2','2'),
                                 ('3','3'),
                                 ('4','4'),
                                 ('5','5'),
                                 ('6','6')
                                 ], string='Cabin')
    type = fields.Selection([
                             ('standard','Standard'),
                             ('outside','Outside'),
                             ('specialist','Specialist')
                             ],string="Type", copy=False)
    special_ids = fields.One2many('banas.hms.special.service', 'doctor_id', string="Special Services")
    designation = fields.Char(string='Designation',)
    highest_qualification_id= fields.Many2one('banas.hms.doctor.degree', string='Highest Qualification')
    city_id = fields.Char(string='City')


    @api.model
    def create(self, values):
        if values.get('code', 'New') == 'New':
            values['code'] = self.env['ir.sequence'].next_by_code('banas.hms.doctor') or ''
        res = super(HMSDoctors, self).create(values)
        return res

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

    # @api.model
    # def test_amount_to_text(self):
    #     print (">>>>>>>>>>>>>>>>>>>>>>>>>>>",)
    #     word_1=amount_to_text_en.amount_to_text(self.consul_charge,lang='en_IN', currency='Rupees')
    #     check_amount_in_words = word_1.replace(' and Zero Cent', '')
    #     return [{'amount_text':check_amount_in_words}]


class SpecialServices(models.Model):
    _name = 'banas.hms.special.service'
    _description = 'HMS Special Services'

    product_id = fields.Many2one('product.product', string="Service")
    hospital_share = fields.Float('Hospital Share')
    ksga_share = fields.Float('KSGA Share')
    amount = fields.Float('Amount')
    doctor_id = fields.Many2one('banas.hms.doctor', string="Doctor")


class ReferringDoctors(models.Model):
    _name = 'banas.hms.referring.doctor'
    _description = "HMS Doctor Reference"

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    address = fields.Char(string='Address')
    street = fields.Char(string='Street')
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State')
    city_id = fields.Char(string='City')
    zip = fields.Char(string='Zip', size=64)
    refer_type = fields.Selection([
                                  ('advertisement','Advertisement'),
                                  ('camp','Camp'),('employee','Employee'),
                                  ('friend','Friend'),
                                  ('patient','Patient'),
                                  ('ref. Dr.','Ref. Dr.'),
                                  ('relative','Relative'),
                                  ('self','Self'),
                                  ('website','Website'),
                                ], string='Referred Type')
    state_ref = fields.Char(string='State')


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


    # @api.onchange('city_id')
    # def onchange_city_id(self):
    #     if self.city_id:
    #         self.state_id = self.city_id.state_id.id


    # @api.onchange('state_id')
    # def onchange_state_id(self):
    #     if self.city_id.state_id != self.state_id:
    #         self.city_id = False
    #     if self.state_id:
    #         self.country_id = self.state_id.country_id.id


    # @api.onchange('country_id')
    # def _onchange_country_id(self):
    #     res = {'domain': {'state_id': []}}
    #     if self.country_id:
    #         res['domain']['state_id'] = [('country_id', '=', self.country_id.id)]
    #     return res
