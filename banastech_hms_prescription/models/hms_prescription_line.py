from datetime import datetime
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import math

class HMSPrescriptionLine(models.Model):
    _name = 'prescription.line'
    _order = 'sequence,id'

    prescription_id = fields.Many2one('prescription.order', ondelete="cascade", string='Prescription ID', )
    patient_id = fields.Many2one('banastech.hms.patient', related="prescription_id.patient_id", string='Patient')
#     #ipmr_line_id = fields.Many2one('indoor.patient.medicine.request', string='IPMR Line')
#     #Removed because not use any where in  module.
#     #name_for_hospitalize_id = fields.Many2one('inpatient.registration', string='Medicaments for next 24 Hours')
#     name_for_surgery_id = fields.Many2one('hms_surgery', ondelete="cascade", string='Medicaments for next 24 Hours')
    product_id = fields.Many2one('product.product', ondelete="cascade", string='Product', required=True, ) #domain=[('hospital_product_type', '=', 'medicament')]
    indication = fields.Many2one('banas.hms.diseases', ondelete="restrict", string='Disease', help='Choose a disease for this medicament from the disease list. It'\
            ' can be an existing disease of the patient or a prophylactic.')
    allow_substitution = fields.Boolean(string='Allow Substitution')
    prnt = fields.Boolean(string='Print', help='Check this box to print this line of the prescription.',default=True)
    quantity = fields.Float(string='Units', digits=(4, 0), help="Number of units of the medicament. Example : 30 capsules of amoxicillin",default=1.0)
    active_component_ids = fields.Many2many('banas.hms.active.comp','product_pres_comp_rel','product_id','pres_id','Active Component')
    start_treatment = fields.Datetime(string='Start Date')
    end_treatment = fields.Datetime(string='End Date')
#     consumption_time = fields.Datetime(string='Consumption Time')
    dose = fields.Float('Quantity', digits=(16, 2), help="Amount of medication (eg, 250 mg) per dose",default=1.0)
    dose_unit = fields.Many2one('product.uom', ondelete="restrict", string='Dosage Unit', help='Amount of medication (eg, 250 mg) per dose')
#     qty = fields.Integer('x')
    form = fields.Many2one('banas.hms.drug.form',related='product_id.form_id', string='Form',help='Drug form, such as tablet or gel')
    route = fields.Many2one('banas.hms.drug.route', ondelete="cascade", string='Route', help='Drug form, such as tablet or gel')
    common_dosage = fields.Many2one('banas.hms.medication.dosage', ondelete="cascade", string='Frequency', help='Drug form, such as tablet or gel')
#     medicine_type = fields.Many2one('banas.hms.drug.form', string='Type')
#     suffix_freq_id = fields.Many2one('banas.hms.medication.dosage', string='Advice')
    time_interval = fields.Char(string='Day')
    sub_frequency_id = fields.Many2one('banas.hms.medication.dosage', string="Instruction")
#     admin_times = fields.Char('Admin Hours', size=255)
#     frequency = fields.Integer('Frequency')
#     temp_patient_id = fields.Many2one('hms.patient','Temp Patient')
#     frequency_unit = fields.Selection([
#         ('', 'None'),
#         ('seconds', 'seconds'),
#         ('minutes', 'minutes'),
#         ('hours', 'hours'),
#         ('days', 'days'),
#         ('weeks', 'weeks'),
#         ('wr', 'when required')],'Unit')
#     frequency_prn = fields.Boolean(string='Frequency prn', help='')
    duration = fields.Integer('Treatment duration')
    duration_period = fields.Selection([
        ('', 'None'),
        ('minutes', 'minutes'),
        ('hours', 'hours'),
        ('days', 'days'),
        ('months', 'months'),
        ('years', 'years'),
        ('indefinite', 'indefinite')],'Treatment period')
#     refills = fields.Integer(string='Refills #')
    review = fields.Datetime(string='Review')
#     actual_time = fields.Datetime(string='Actual Time')
#     administered_by = fields.Many2one('res.users', ondelete="restrict", string='Administered by')
    short_comment = fields.Char(size=256, string='Comment', help='Short comment on the specific drug')
    batch_no = fields.Many2one("stock.production.lot", ondelete="restrict", string="Batch Number")
    exp_date = fields.Datetime("Expiry Date")
#     state = fields.Selection([
#         ('pending', 'Pending'),
#         ('missed', 'Missed'),
#         ('delayed', 'Delayed'),
#         ('delivered', 'Delivered')], 'Status', default='pending')
    days = fields.Integer("Days", default=1)
    appointment_id = fields.Many2one('banastech.hms.appointment', ondelete="restrict", string='Appointment')
#     hos_appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
    stat = fields.Boolean('Stat')
    completed = fields.Boolean('Completed')
    t1 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T1")
    t2 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T2")
    t3 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T3")
    t4 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T4")
    sequence = fields.Integer(default=99)

    @api.onchange('batch_no')
    def onchange_batch(self):
        if self.batch_no:
            self.exp_date = self.batch_no.use_date

    @api.onchange('stat')
    def onchange_batch(self):
        if self.stat:
            self.t1 = str(int(math.ceil(float(datetime.now().time().hour) + 5.5)))

    @api.model
    def medicine_done(self, values):
        self.completed = True

    @api.model
    def medicine_undone(self, values):
        self.completed = False

#     @api.onchange('product_id')
#     def onchange_product(self):
#         if self.product_id:
#             self.sub_frequency_id = self.product_id and self.product_id.suffix_frequency_id and self.product_id.suffix_frequency_id.id or False
#             self.common_dosage = self.product_id.common_dosage and self.product_id.common_dosage or False
#             self.active_component_ids = [(6, 0, [x.id for x in self.product_id.active_component_ids])]
#             self.indication = self.product_id.indications,
#             self.form = self.product_id.form and self.product_id.form.id or False,
#             self.dose_unit = self.product_id.dose_unit and self.product_id.dose_unit.id or False,
#             self.days = self.appointment_id and self.appointment_id.days_1 or self.product_id.days
#             self.quantity = float(self.common_dosage.code) * int(self.days) or 1
#             if self.product_id.product_exception=='yes':
#                 self.quantity = self.product_id.no_per_pack

    @api.onchange('common_dosage','days')
    def onchange_common_dosage(self):
        if self.common_dosage:
            if not self.stat:
                self.t1 = self.common_dosage.t1
            self.t2 = self.common_dosage.t2
            self.t3 = self.common_dosage.t3
            self.t4 = self.common_dosage.t4
            self.quantity = float(self.common_dosage.code) * int(self.days) or 1
            if self.product_id.product_exception == 'yes':
                self.quantity = self.product_id.no_per_pack
            self.dose = float(self.common_dosage.code) * int(self.time_interval) or 1

    @api.onchange('time_interval')
    def onchange_timeinterval(self):
        if self.time_interval:
            self.dose = float(self.common_dosage.code) * int(self.time_interval) or 1