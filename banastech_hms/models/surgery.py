from odoo import api, fields, models
from odoo.tools.translate import _

class HMSDietplan(models.Model):
    _name = "hms.dietplan"
    _description = "Dietplan"

    name = fields.Char(string='Name', required=True)

class HMSSurgery(models.Model):
    _name = "hms_surgery"
    _description = "Surgery"

    name= fields.Char(string='Surgery Code', help="Procedure Code, for example ICD-10-PCS Code 7-character string")
    description=  fields.Char(string='Surgery Name', size=128)
    diseases= fields.Many2one('banas.hms.diseases', ondelete='restrict', string='Base condition', help="Base Condition / Reason")
    dietplan = fields.Many2one('hms.dietplan', ondelete='set null', string='Diet Plan')
    surgery_product_id = fields.Many2one('product.product', ondelete='cascade',string= "Surgery Product", required=True)
 #   # speciality = fields.Many2one('physician.specialty', ondelete='set null', string='Speciality')
 #   # sub_speciality = fields.Many2one('physician.specialty', string='Sub-Speciality')
    diagnosis = fields.Text(string="Diagnosis")
    clinincal_history = fields.Text(string="Clinical History")
    examination_id = fields.Text(string="Examination")
    investigation_id = fields.Text(string="Investigation")
    adv_on_dis = fields.Text(string="Advice on Discharge")
    # notes = fields.Text(string='Operative Notes')
    classification = fields.Selection([('o','Optional'),('r','Required'),('u','Urgent')], string='Surgery Classification', select=True)
    surgeon = fields.Many2one('banas.hms.doctor', ondelete='restrict', string=' Primary Surgeon', help="Surgeon who did the procedure")
    date = fields.Datetime(string='Date')
    age = fields.Char(string='Patient age',size=3,help='Patient age at the moment of the surgery. Can be estimative')
    extra_info = fields.Text(string='Extra Info')
    # special_precautions_id = fields.Text(string="Special Precautions")
