from odoo import api, fields, models
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta
from datetime import datetime


class HMSPatientMedication(models.Model):
    _name = 'banastech.hms.patient.medication'

    patient_id = fields.Many2one('banastech.hms.patient', string='Patient')
#     #name = fields.Many2one('hms.patient', string='Patient',readonly=True )
    doctor = fields.Many2one('banas.hms.doctor', string='Doctor',help='Physician who prescribed the medicament')
    adverse_reaction = fields.Text(string='Adverse Reactions',help='Side effects or adverse reactions that the patient experienced')
    notes = fields.Text(string='Extra Info')
    is_active = fields.Boolean(string='Active', help='Check if the patient is currently taking the medication')
    course_completed = fields.Boolean(string='Course Completed')
    template = fields.Many2one('product.template',string='Medication Template', )
    discontinued_reason = fields.Char(size=256,string='Reason for discontinuation',help='Short description for discontinuing the treatment')
    discontinued = fields.Boolean(string='Discontinued')


# class IndimediDiseases(models.Model):
#     _inherit = 'hms.diseases'

#     patient_id = fields.Many2one('banastech.hms.patient', string='Patient', help='Patient')


class HMSEthnicity(models.Model):
    _name = 'banastech.hms.ethnicity'

    notes = fields.Char(size=256, string='Notes')
    code = fields.Char(size=256, string='Code')
    name = fields.Char(size=256, string='Name', required=True ,translate=True)

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]


class HMSVaccination(models.Model):
    _name = 'banastech.hms.vaccination'

    name = fields.Char(size=256, string='Name')
    vaccine_lot = fields.Char(size=256, string='Lot Number', help='Please check on the vaccine (product) production lot numberand'\
    ' tracking number when available !')
    patient_id = fields.Many2one('banastech.hms.patient', string='Patient')
    vaccine = fields.Many2one('product.product', help='Vaccine Name. Make sure that the vaccine (product) has all the'\
    ' proper information at product level. Information such as provider,'\
    ' supplier code, tracking number, etc.. This  information must always'\
    ' be present. If available, please copy / scan the vaccine leaflet'\
    ' and attach it to this record')
    dose = fields.Integer(string='Dose #')
    observations = fields.Char(size=256, string='Observations',required=True)
    date = fields.Datetime(string='Date')
    institution = fields.Char(string='Institution')
    next_dose_date = fields.Datetime(string='Next Dose')


class HMSPatient(models.Model):
    _inherit='banastech.hms.patient'

#     family = fields.Many2one('indimedi.family', string='Family', help='Family Code')
#     primary_care_doctor = fields.Many2one('hms.physician',string='Primary Care Doctor', help='Current primary care / family doctor')
#     childbearing_age = fields.Boolean(string='Potential for Childbearing')
#     medications = fields.One2many('banastech.hms.patient.medication', 'patient_id', string='Medications')
#     #evaluations = fields.One2many('hms.patient.evaluation', 'patient_id', string='Evaluations')
#     critical_info = fields.Text( string='Important disease, allergy or procedures information', help='Write any important information on the patient\'s disease, surgeries, allergies, ...')
#     diseases = fields.One2many('hms.diseases', 'patient_id', string='Diseases', help='Mark if the patient has died')
    ethnic_group = fields.Many2one('banastech.hms.ethnicity', string='Ethnic group')
#     vaccinations = fields.One2many('indimedi.vaccination', 'patient_id',string='Vaccinations')
#     cod = fields.Many2one('hms.diseases', string='Cause of Death')
    presc_count = fields.Integer(string="Prescription Count", compute='_compute_prescription_count')

    def _compute_prescription_count(self):
        for rec in self:
            presc_count = self.env['prescription.order'].sudo().search_count([('patient_id', '=', rec.id)])
            rec.presc_count = presc_count

    def action_prescription(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Prescriptions'),
            'res_model': 'prescription.order',
            'domain': [('patient_id','=',self.id)],
            'view_mode': 'tree,form',
        }