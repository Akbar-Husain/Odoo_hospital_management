from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT
import time
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
import json, ast


selection_time = [
    ('8_9', '08-09 AM'),('9_10','09-10 AM'),
    ('10_11','10-11 AM'),('11_12','11-12 AM'),
    ('12_13','12-01 PM'),('13_14','01-02 PM'),
    ('14_15','02-03 PM'),('15_16','03-04 PM'),
    ('16_17','04-05 PM'),('17_18','05-06 PM'),
    ('18_19','06-07 PM'),('19_20','07-08 PM'),
    ('20_21','08-09 PM'),('21_22','09-10 PM'),
    ('22_23','10-11 PM'),('23_24','11-12 PM'),
    ('24_1','12-01 AM'),('1_2','01-02 AM'),
    ('2_3','02-03 AM'),('3_4','03-04 AM'),
    ('4_5','04-05 AM'),('5_6','05-06 AM'),
    ('6_7','06-07 AM'),('7_8','07-08 AM')
]
# selection_time_key = ['8_9', '9_10', '10_11',
#     '11_12', '12_13', '13_14', '14_15', '15_16',
#     '16_17', '17_18', '18_19', '19_20', '20_21',
#     '21_22', '22_23', '23_24', '24_1', '1_2', '2_3',
#     '3_4', '4_5', '5_6', '6_7', '7_8']


# class AccountInvoiceLine(models.Model):
#     _inherit = 'account.invoice.line'

#     doctor_visit_charges = fields.Many2many('icu.doctors.visit.sheet', 'icu_doctors_visit_sheet_inv_line_rel', 'sheet_id', 'inv_line_id', string="Doctor Charges Sheet")
#     patient_service_values = fields.Many2many('patient.service.value', 'patient_service_value_inv_line_rel',  'inv_line_id', 'sheet_id', string="ICU Charges")
#     patient_doctor_visit_charges = fields.Many2many('icu.doctors.visit.sheet', 'icu_doctors_visit_sheet_inv_patient_line_rel', 'inv_line_id', 'sheet_id', string="Patient Doctor Charges Sheet")

# class AccountDueAmount(models.Model):
#     _inherit = 'account.invoice'

#     @api.depends('amount_total','residual')
#     def _due_amount(self):
#         for value in self:
#             value.payment_due = value.amount_total - value.residual

#     # @api.one
#     # @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice')
#     # def _compute_amount(self):
#     #     self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
#     #     self.amount_tax = sum(line.amount for line in self.tax_line_ids)

#     #     self.amount_total = self.amount_untaxed + self.amount_tax - self.amount_discount
#     #     amount_total_company_signed = self.amount_total
#     #     amount_untaxed_signed = self.amount_untaxed
#     #     if self.currency_id and self.currency_id != self.company_id.currency_id:
#     #         currency_id = self.currency_id.with_context(date=self.date_invoice)
#     #         amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
#     #         amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
#     #     sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
#     #     self.amount_total_company_signed = amount_total_company_signed * sign
#     #     self.amount_total_signed = self.amount_total * sign
#     #     self.amount_untaxed_signed = amount_untaxed_signed * sign

#     payment_due = fields.Float(string='Due Amount',compute='_due_amount')
#     credit = fields.Monetary(related="partner_id.credit", string="Credit")
#     amount_discount = fields.Float('Discount',default=0.0)
#     # If this comment is removed the program will blow up whole Accounting, So Do not touch.
#     # amount_total = fields.Float(string="Total", compute='_compute_amount')
#     patient_name = fields.Char(string='Hospitalization #')
#     bed_id = fields.Char(string='Bed No.')
#     expected_stay = fields.Char('Expected Day')
#     hospitalization_date = fields.Datetime(string='Hospitalization Date')
#     discharge_date = fields.Datetime (string='Discharge date')


# class AccountInvocieLine(models.Model):
#     _inherit = 'account.invoice.line'
    
#     patient_id = fields.Many2one('hms.patient', string="Patient")

# class DiabeticProtocol(models.Model):
#     _name = 'hms.diabetic.protocol'

#     icu_chart_id = fields.Many2one('hms.icu.chart', string="Patient")


# class DiabeticProtocolLine(models.Model):
#     _name = 'hms.diabetic.protocol.line'
#     _rec_name = 'inpatient_id'

#     inpatient_id = fields.Many2one('hms.icu.chart', string="InPatient")

# class product_template(models.Model):
#     _inherit = "product.template"

#     hospital_product_type = fields.Selection(selection_add=[('doctor_visit_sheet','Doctors Visit Sheet'),('icu_patient_services','ICU Patient Services')])

class Inpatient(models.Model):
    _inherit = 'inpatient.registration'

#     icu_welcome_line_ids = fields.One2many('hms.icu.welcome', 'inpatient_id' , 'Inpatient Welcome')
#     chart_ids = fields.One2many('hms.icu.chart', 'inpatient_id' , 'Inpatient Welcome')
    doctors_visit_sheet_ids = fields.One2many('icu.doctors.visit.sheet','hospitalization_id','Doctor Visit Sheet')
#     invoice_id = fields.Many2one('account.invoice', string='ICU Invoice', ondelete='cascade', copy=False)
    patient_service_ids = fields.One2many('patient.service.value','patient_service_value_id',string='Patient Service')

#     @api.multi
#     def view_doctor_visit_invoice(self):
#         invoice_line = self.env['account.invoice.line'].search([('doctor_visit_charges', 'in', self.doctors_visit_sheet_ids.ids)])
#         invoice_ids = [x.invoice_id.id for x in invoice_line]
#         invoice_ids = self.env['account.invoice'].browse(invoice_ids)
#         action = self.env.ref('account.action_invoice_tree2')
#         result = action.read()[0]
#         result['context'] = {'type': 'in_invoice', 'default_doctor_visit_charges': self.id}
#         if not invoice_ids:
#             journal_domain = [
#                 ('type', '=', 'purchase'),
#                 ('company_id', '=', self.company_id.id),
#             ]
#             default_journal_id = self.env['account.journal'].search(journal_domain, limit=1)
#             if default_journal_id:
#                 result['context']['default_journal_id'] = default_journal_id.id
#         else:
#             result['context']['default_journal_id'] = invoice_ids[0].journal_id.id
#         if len(invoice_ids) != 1:
#             result['domain'] = "[('id', 'in', " + str(invoice_ids.ids) + ")]"
#         elif len(invoice_ids) == 1:
#             res = self.env.ref('account.invoice_supplier_form', False)
#             result['views'] = [(res and res.id or False, 'form')]
#             result['res_id'] = invoice_ids.id
#         return result

#     @api.multi
#     def create_doctor_visit_invoice(self):        
#         invoice_line = self.env['account.invoice.line']
#         product_obj = self.env['product.product']
#         invoice_obj = self.env['account.invoice']
#         fiscal_obj = self.env['account.fiscal.position']
#         doctor_obj = self.env['hms.physician']
#         patient_obj = self.env['inpatient.registration']

#         journal_domain = [
#             ('type', '=', 'purchase'),
#             ('company_id', '=', self.company_id.id),
#         ]
#         fpos = self.invoice_id.fiscal_position_id
#         self._cr.execute("""select visit_specification, doctor_id, count(visit_specification),
#             sum(visit_charge) from
#             icu_doctors_visit_sheet where
#             invoiced=False and hospitalization_id=%s group by
#             visit_specification, doctor_id"""%(self.id))
#         visits = self._cr.fetchall()
#         default_journal_id = self.env['account.journal'].search(journal_domain, limit=1)
#         invoices = {}
#         for sheet in visits:
#             self._cr.execute("""select id from icu_doctors_visit_sheet where
#                 hospitalization_id=%s and
#                 visit_specification=%s and doctor_id=%s"""%(self.id, sheet[0], sheet[1]))
#             charges_ids = self._cr.fetchall()
#             self._cr.execute("update icu_doctors_visit_sheet set invoiced=True where invoiced=False and hospitalization_id=%s and visit_specification=%s and doctor_id=%s"%(self.id, sheet[0], sheet[1]))
#             doctor_visit_charges = [(4, x[0]) for x in charges_ids]
#             product_id = product_obj.search([('id', '=', sheet[0])])
#             if invoices.get(sheet[1], None):
#                 invoices[sheet[1]].append((0, 0, {
#                     'name': product_id.name,
#                     'origin': self.name,
#                     'uom_id': product_id.uom_po_id.id,
#                     'product_id': product_id.id,
#                     'patient_id': self.patient_id.id,
#                     'price_unit': self.company_id.currency_id.compute(sheet[3]/int(sheet[2]), self.company_id.currency_id, round=False),
#                     'quantity': int(sheet[2]),
#                     'discount': 0.0,
#                     'account_id': invoice_line.get_invoice_line_account('in_invoice', product_id, fiscal_obj, self.company_id).id,
#                     'invoice_line_tax_ids': product_id.taxes_id.ids,
#                 }))
#             else:
#                 invoices[sheet[1]] = [(0, 0, {
#                     'name': product_id.name,
#                     'origin': self.name,
#                     'uom_id': product_id.uom_po_id.id,
#                     'product_id': product_id.id,
#                     'patient_id': self.patient_id.id,
#                     'account_id': invoice_line.with_context({'journal_id': default_journal_id.id, 'type': 'in_invoice'})._default_account(),
#                     'price_unit': self.company_id.currency_id.compute(sheet[3]/int(sheet[2]), self.company_id.currency_id, round=False),
#                     'account_id': invoice_line.get_invoice_line_account('in_invoice', product_id, fiscal_obj, self.company_id).id,
#                     'quantity': int(sheet[2]),
#                     'discount': 0.0,
#                     'invoice_line_tax_ids': product_id.taxes_id.ids,
#                     'doctor_visit_charges': doctor_visit_charges,
#                 })]

#         for key, value in invoices.items():
#             doctor_id = doctor_obj.search([('id', '=', key)])
#             invoice_obj.create({
#                     'partner_id': doctor_id.user_id.partner_id.id,
#                     'journal_id': default_journal_id.id,
#                     'type': 'in_invoice',
#                     'invoice_line_ids': value,
#                 })

#     @api.multi
#     def view_icu_patient_invoice(self):
#         invoice_line = self.env['account.invoice.line'].search(['|', ('patient_service_values', 'in', self.patient_service_ids.ids), ('patient_doctor_visit_charges', 'in', self.doctors_visit_sheet_ids.ids)])
#         invoice_ids = [x.invoice_id.id for x in invoice_line]
#         invoice_ids = self.env['account.invoice'].browse(invoice_ids)
#         action = self.env.ref('account.action_invoice_tree1')
#         result = action.read()[0]
#         result['context'] = {'type': 'in_invoice', 'default_patient_service_values': self.id}
#         if not invoice_ids:
#             journal_domain = [
#                 ('type', '=', 'sale'),
#                 ('company_id', '=', self.company_id.id),
#             ]
#             default_journal_id = self.env['account.journal'].search(journal_domain, limit=1)
#             if default_journal_id:
#                 result['context']['default_journal_id'] = default_journal_id.id
#         else:
#             result['context']['default_journal_id'] = invoice_ids[0].journal_id.id
#         if len(invoice_ids) != 1:
#             result['domain'] = "[('id', 'in', " + str(invoice_ids.ids) + ")]"
#         elif len(invoice_ids) == 1:
#             res = self.env.ref('account.invoice_form', False)
#             result['views'] = [(res and res.id or False, 'form')]
#             result['res_id'] = invoice_ids.id
#         return result

#     @api.one
#     def create_icu_patient_invoice(self):
#         inv_obj = self.env['account.invoice']
#         ir_property_obj = self.env['ir.property']
#         fiscal_obj = self.env['account.fiscal.position']
#         product_obj = self.env['product.product']
#         physician_obj = self.env['hms.physician']
#         inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
#         account_id = fiscal_obj.map_account(inc_acc).id if inc_acc else False

#         if not account_id:
#             raise UserError(
#                 _('You may have to install a chart of account from Accounting app, settings menu.'))

#         self._cr.execute("""select visit_specification, count(visit_specification), sum(visit_charge), doctor_id
#             from icu_doctors_visit_sheet 
#             where patient_invoiced=False and hospitalization_id=%s group by visit_specification, doctor_id"""%(self.id))
#         visits = self._cr.fetchall()

#         invoice_lines = []
#         for visit in visits:
#             product_id = product_obj.search([('id', '=', visit[0])])
#             self._cr.execute("""select id from 
#                 icu_doctors_visit_sheet where 
#                 patient_invoiced=False and hospitalization_id=%s 
#                 and visit_specification=%s and doctor_id=%s"""%(self.id, visit[0], visit[3]))
#             product_charges_ids = self._cr.fetchall()
#             patient_doctor_visit_charges = [(4, x[0]) for x in product_charges_ids]
#             physician_id  = physician_obj.search([('id', '=', visit[3])])
#             invoice_lines.append((0, 0, {
#                 'name': product_id.name + physician_id.name,
#                 'doctor_id': physician_id.id,
#                 'origin': self.name,
#                 'uom_id': product_id.uom_po_id.id,
#                 'product_id': product_id.id,
#                 'account_id': account_id,
#                 'price_unit': self.company_id.currency_id.compute(visit[2]/int(visit[1]), self.company_id.currency_id, round=False),
#                 'quantity': int(visit[1]),
#                 'discount': 0.0,
#                 'patient_doctor_visit_charges': patient_doctor_visit_charges
#             }))

#         self._cr.execute("""update icu_doctors_visit_sheet set patient_invoiced=True 
#             where patient_invoiced=False and hospitalization_id=%s"""%(self.id))


#         self._cr.execute("""select service_name, sum(service_qty), sum(service_total_amount)/sum(service_qty) 
#             from patient_service_value where 
#             invoiced=False and patient_service_value_id=%s group by service_name"""%(self.id))
#         charges_ids = self._cr.fetchall()
#         self._cr.execute("""update patient_service_value set invoiced=True where 
#             invoiced=False and patient_service_value_id=%s"""%(self.id))

#         for charge in charges_ids:
#             self._cr.execute("""select id from patient_service_value where 
#                 patient_service_value_id=%s and service_name=%s"""%(self.id, charge[0]))
#             product_charges_ids = self._cr.fetchall()
#             product_charges_ids = [(4, x[0]) for x in product_charges_ids]
#             product_id = product_obj.browse([charge[0]])
#             if product_id:
#                 name = product_id.name_get()[0][1]
#                 if product_id.description_sale:
#                     name += '\n' + product_id.description_sale
#                 invoice_lines.append((0, 0, {
#                     'name': name,
#                     'price_unit': charge[2],
#                     'account_id': account_id,
#                     'quantity': charge[1],
#                     'discount': 0.0,
#                     'uom_id': product_id.uom_id.id,
#                     'product_id': product_id.id,
#                     'account_analytic_id': False,
#                     'patient_service_values': product_charges_ids,
#                 }))
#         if not invoice_lines:
#             raise ValidationError(
#                 _('Not have any report Unpaid'))

#         invoice = inv_obj.create({
#             'name': 'Patient',
#             'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
#             'partner_id': self.patient_id.partner_id.id,
#             'patient_id': self.patient_id.id,
#             'origin': 'Patient Charges:'+self.name,
#             'type': 'out_invoice',
#             'currency_id': self.env.user.company_id.currency_id.id,
#             'invoice_line_ids': invoice_lines,
#             'report_type': 'inpatient',
#             'patient_name':self.name,
#             'hospitalization_date':self.hospitalization_date,
#             'discharge_date':self.discharge_date,
#             'bed_id':self.bed_id.name,
#             'stay_day':self.expected_stay,
#         })
#         return invoice

#     @api.multi
#     def action_inpatient_icu(self):
#         action = self.env.ref('hms_icu.action_icu_welcome')
#         result = action.read()[0]
#         result['context'] = {'default_inpatient_id': self.id, 'default_patient_id': self.patient_id.id}
#         if len(self.icu_welcome_line_ids) != 1:
#             result['domain'] = "[('id', 'in', " + str(self.icu_welcome_line_ids.ids) + ")]"
#         elif len(self.icu_welcome_line_ids) == 1:
#             res = self.env.ref('hms_icu.view_hms_icu_welcome_form', False)
#             result['views'] = [(res and res.id or False, 'form')]
#             result['res_id'] = self.icu_welcome_line_ids.id
#         return result

#     @api.multi
#     def action_icu_chart1(self):
#         action = self.env.ref('hms_icu.action_icu_chart1')
#         result = action.read()[0]
#         result['context'] = {'default_inpatient_id': self.id, 
#                             'default_patient_id': self.patient_id.id,
#                             'form_view_ref':'hms_icu.view_hms_icu_chart1_form',
#                             'default_type':'chart1'}
#         result['domain'] = [('patient_id', '=', self.patient_id.id), ('inpatient_id', '=', self.id)]
#         chart_ids = self.env['hms.icu.chart'].search(result['domain'])
#         if len(chart_ids) == 1:
#             res = self.env.ref('hms_icu.view_hms_icu_chart1_form', False)
#             result['views'] = [(res and res.id or False, 'form')]
#             result['res_id'] = chart_ids.id
#         return result    

#     @api.multi
#     def action_icu_chart2(self):
#         action = self.env.ref('hms_icu.action_icu_chart2')
#         result = action.read()[0]
#         result['context'] = {'default_inpatient_id': self.id,
#                             'default_patient_id': self.patient_id.id,
#                             'tree_view_ref':'hms_icu.view_hms_icu_chart2_tree',
#                             'form_view_ref':'hms_icu.view_hms_icu_chart2_form',
#                             'default_type':'chart2',
#         }
#         result['domain'] = [('patient_id', '=', self.patient_id.id), ('inpatient_id', '=', self.id)]
#         chart_ids = self.env['hms.icu.chart'].search(result['domain'])
#         if len(chart_ids) == 1:
#             res = self.env.ref('hms_icu.view_hms_icu_chart2_form', False)
#             result['views'] = [(res and res.id or False, 'form')]
#             result['res_id'] = chart_ids.id
#         return result

#     @api.multi
#     def indimedi_devasya_treatment(self):
#         return {
#             'name': _('Treatment Sheet'),
#             'view_type': 'form',
#             'view_mode': 'form,tree',
#             'res_model': 'hms.treatment',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id','=',self.id)],
#             'context': {
#                 'default_patient_id': self.id,
#                 'form_view_ref': 'hms_treatment.view_devasya_hms_treatment_form'
#             },
#         }

class ICUDoctorsVisitSheet(models.Model):
    _name = 'icu.doctors.visit.sheet'

    visit_datetime = fields.Datetime('Date',default=fields.Datetime.now)
    doctor_id = fields.Many2one('hms.physician',string='Doctor')
    visit_specification = fields.Many2one('product.product',string='Specify Details of Visit',domain=[('hospital_product_type', '=', 'doctor_visit_sheet')],context={'default_hospital_product_type': 'doctor_visit_sheet'}, required="True")
    visit_charge = fields.Integer(string='Charges')
    hosp_id = fields.Many2one('inpatient.registration',string='Hospitalization')
    hospitalization_id = fields.Many2one('inpatient.registration',string='Hospitalization')
    invoiced = fields.Boolean("Invoiced", default=False)
    patient_invoiced = fields.Boolean("Patient Invoiced", default=False)


class PatientServiceValue(models.Model):
    _name = 'patient.service.value'

    service_datetime = fields.Datetime('Date',default=fields.Datetime.now)
    service_name = fields.Many2one('product.product',string='Services',domain=[('hospital_product_type', '=', 'icu_patient_services')],context={'default_hospital_product_type': 'icu_patient_services'},required="True")
    service_charges = fields.Integer('Fees')
    service_qty = fields.Integer('Qty',digits=dp.get_precision('Quantity'), default=1)
    service_total_amount = fields.Integer('Total')
    patient_service_value_id = fields.Many2one('icu.patient.service',string='Patient Service')
    invoiced = fields.Boolean("Invoiced")

#     @api.onchange('service_charges','service_qty')
#     def onchange_services_total(self):
#         self.service_total_amount = self.service_charges * self.service_qty


# class ICUHospitalization(models.Model):
#     _inherit = 'hms.patient'

#     @api.multi
#     def indimedi_patient_icu_welcome(self):
#         return {
#             'name': _('ICU HMS'),
#             'view_type': 'form',
#             'view_mode': 'form,tree',
#             'res_model': 'inpatient.registration',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id','=',self.id)],
#             'context': {
#                 'default_patient_id': self.id,
#                 'form_view_ref': 'hms_icu_insurance.view_inpatient_registration_icu_form'
#             },
#         }

   
class ICUWelcome(models.Model):
    _name = 'hms.icu.welcome'
    _rec_name = 'name'

    name = fields.Char("ID", default=lambda self: _('New one'))
    patient_id = fields.Many2one('banastech.hms.patient', string="Patient", required=True)
    inpatient_id = fields.Many2one('inpatient.registration', string="InPatient")
    image = fields.Binary(related='patient_id.image',string='Image')
    age =  fields.Char(related='patient_id.age', string='Age')
    gender =  fields.Selection(related='patient_id.gender', string='Gender')
    blood_group = fields.Selection(related='patient_id.blood_group', string='Blood Group')
    cm = fields.Float(string="Height(Cms)")
    weight = fields.Float(string='Weight(kgs)')
    complain_ids = fields.One2many('hms.icu.welcome.complain.line', 'welcome_complain_id', 'Chief Complain')
    temp = fields.Char(string="Temp(F)")
    pulse = fields.Char(string="Pulse(/min)")
    bph = fields.Char(string="BP(mmHg)")
    bpl = fields.Char(string="BP")
    rr = fields.Char(string="RR(/min)")
    spo2 = fields.Char(string="SPO2(%)")
    anemia = fields.Boolean('Anemia')
    cyanosis = fields.Boolean('Cyanosis')
    jaundice = fields.Boolean('Jaundice')
    lymphadenopathy = fields.Boolean('Lymphadenopathy')
    edema = fields.Boolean('Edema')
    edema_note = fields.Char('Edema Note')
    clubbing = fields.Boolean('Clubbing')
    clubbing_note = fields.Char('Clubbing Note')
    ge_other = fields.Boolean('Other')
    ge_other_note = fields.Char('Other Note')
#     ########SYSTEMIC EXAMINATION:
#     #RESPIRATORY:
    asthma = fields.Boolean('Asthma')
    copd = fields.Boolean('COPD')
    bronchitis = fields.Boolean('Bronchitis')
    dyspnoea = fields.Boolean('Dyspnoea')
    orthopnoea = fields.Boolean('Orthopnoea')
    pneumonia = fields.Boolean('Pneumonia')
    productive_cough = fields.Boolean('Productive Cough')
    urti = fields.Boolean('URTI')
    shortness_of_breaths = fields.Boolean('Shortness of breaths')
    tuberculosis = fields.Boolean('Tuberculosis')
    wnl_respiratory = fields.Boolean('WNL')
#     #CARDIOVASCULAR:
    hypertension = fields.Boolean('Hypertension')
    mi = fields.Boolean('MI')
    angina = fields.Boolean('Angina')
    murmur = fields.Boolean('Murmur')
    chf = fields.Boolean('CHF')
    abnormal_ECG = fields.Boolean('Abnormal ECG')
    dysrhythmia = fields.Boolean('Dysrhythmia')
    rheumatic_fever = fields.Boolean('Rheumatic Fever')
    valvular_heart_disease = fields.Boolean('Valvular Heart Disease')
    exercise_tolerance = fields.Boolean('Exercise Tolerance')
    exercise_tolerance_note = fields.Char('Exercise Tolerance Note')
    wnl_cardiov = fields.Boolean('WNL')
#     #GASTROINTESTINAL and LIVER:
    nausea = fields.Boolean('Nausea')
    vomiting = fields.Boolean('Vomiting')
    ulcer = fields.Boolean('Ulcer')
    diarrhoea = fields.Boolean('Diarrhoea')
    hematemesis = fields.Boolean('Hematemesis')
    melena = fields.Boolean('Melena')
    bowel_obstruction = fields.Boolean('Bowel obstruction')
    hepatitis = fields.Boolean('Hepatitis')
    cirrhosis = fields.Boolean('Cirrhosis')
    jaundice = fields.Boolean('Jaundice')
    reflux_ds = fields.Boolean('Reflux D`s')
#     WNL_gast_liver = fields.Boolean('WNL')
#     #RENAL / ENDOCRINAL:
    diabetes = fields.Boolean('Diabetes')
    thyroid_ds = fields.Boolean('Thyroid D`s')
    renal_failure = fields.Boolean('Renal Failure')
    dialysis = fields.Boolean('Dialysis')
    urinary_retention = fields.Boolean('Urinary Retention')
    uti = fields.Boolean('UTI')
    weight_loss_Gain = fields.Boolean('Weight Loss/Gain')
    edema = fields.Boolean('Edema')
    wnl_renal_endoc = fields.Boolean('WNL')
#     #NEUROMUSCULAR:
    arthritis = fields.Boolean('Arthritis')
    muscle_weakness = fields.Boolean('Muscle Weakness')
    back_problems = fields.Boolean('Back Problems')
    paralysis = fields.Boolean('Paralysis')
    paraesthesia = fields.Boolean('Paraesthesia')
    syncope = fields.Boolean('Syncope')
    seizures = fields.Boolean('Seizures')
    headache = fields.Boolean('Headache')
    raised_icp = fields.Boolean('Raised ICP')
    loss_of_cons = fields.Boolean('Loss of Consciousness')
    cva_stroke_tias = fields.Boolean('CVA/Stroke/TIAs')
    wnl_neuromuscular = fields.Boolean('WNL')
#     #Other
    anemia = fields.Boolean('Anemia')
    bleeding_tendencies = fields.Boolean('Bleeding Tendencies')
    immunosuppressed = fields.Boolean('Immunosuppressed')
    cancer = fields.Boolean('Cancer')
    chemotherapy = fields.Boolean('Chemotherapy')
    dehydration = fields.Boolean('Dehydration')
    haemophilia = fields.Boolean('Haemophilia')
    pregnancy = fields.Boolean('Pregnancy')
    recent_steroids = fields.Boolean('Recent Steroids')
    wnl_other = fields.Boolean('WNL')
#     #Specific Comments:
    specific_comments = fields.Text('On RX and Specific Comments')
#     #H/O
    icu_ho_addiction_ids = fields.One2many('hms.icu.addiction.ho', 'icu_ho_addiction_id', '(On RX and Comments ICU)')
#     #H/o Allergy:
    ho_allergy = fields.Boolean('Not Known To Drug Allergy')
    ho_allergy_note = fields.Char('Not Known To Drug Allergy Note')
#     #Airway/Teeth/Head and Neck:
    mp_grading = fields.Char('M.P Grading')
    neck_movement = fields.Char('Neck Movement')
    thyromental_distance = fields.Char('Thyromental Distance')
    mouth_opening = fields.Char('Mouth Opening')
    tm_joint_movement = fields.Char('T-M joint Movement')
    air_teeth = fields.Char('Teeth')
    air_other = fields.Char('Other')
#     #H/o Blood transfusion
    ho_blood_transfusion = fields.Text('H/o Blood Transfusion or BTR')
#     #BTR Family/H:
    btr_family = fields.Text('Family/H')
#     #INVESTIGATIONS:
#     #Haemogram:
    hb = fields.Char('HB')
    tlc = fields.Char('TLC')
    dc = fields.Char('DC')
    platelet = fields.Char('Platelet')
    pcv = fields.Char('PCV')
    rbc = fields.Char('RBC')
#     #RFT and Electrolytes:
    s_urea = fields.Char('S. Urea')
    s_cr = fields.Char('S. Cr.')
    s_na = fields.Char('S. Na +')
    s_k = fields.Char('S.K +')
    mg_plus_plus = fields.Char(string='Mg++')
    ca_plus_plus = fields.Char(string='Ca++')
    phosphorus = fields.Char(string='Phosphorus')
    cl_negative = fields.Char(string='Cl-')
    rbs = fields.Char('RBS')
    elec_blood_group1 = fields.Selection(related='patient_id.blood_group', string='Blood Group',readonly=True)
#     #Liver Function Test:
    s_bilirubin = fields.Char('S.Bilirubin')
    s_direct = fields.Char('S.Direct')
    s_indirect = fields.Char('S.Indirect')
    sgpt = fields.Char('SGPT')
    alp = fields.Char('ALP')
#     #Coagulation Profile
    pt_coagulation = fields.Boolean('PT')
    pt_test_note = fields.Char(string='Test')
    pt_control_note = fields.Char(string='Control')
    pt_inr_note = fields.Char(string='INR')
    aptt_coagulation = fields.Boolean('aPTT')
    aptt_test_note = fields.Char(string='Test')
    aptt_control_note = fields.Char(string='Control')
    aptt_inr_note = fields.Char(string='INR')
    bt = fields.Char('BT')
    ct = fields.Char('CT')
#     #Serological study
    hiv = fields.Selection([('hiv_negative','ve-'),('hiv_positive','ve+'),('hiv_reactive','Reactive'),('hiv_no_reactive','Non Reactive'),],string = "HIV")
    hbsag = fields.Selection([('hbsag_negative','ve-'),('hbsag_positive','ve+'),('hbsag_reactive','Reactive'),('hbsag_no_reactive','Non Reactive'),],string = "HBsAg")
    anti_hcv = fields.Selection([('anti_hcv_negative','ve-'),('anti_hcv_positive','ve+'),('anti_hcv_reactive','Reactive'),('anti_hcv_no_reactive','Non Reactive'),],string = "Anti HCV")
#     #Cardiac study
    cs_ecg = fields.Text('ECG')
    d_echo = fields.Text('2D-ECHO:')
#     #IMAGING STUDY:
    x_Ray = fields.Text('X-Ray')
    usg = fields.Text('USG')
    ct_mri = fields.Text('CT/MRI')
#     #Monitoring and Equipment:
    ecg = fields.Boolean('ECG')
    nibp = fields.Boolean('NIBP')
    spO2 = fields.Boolean('SPO2')
    etco2 = fields.Boolean('EtCO2')
    temp1 = fields.Boolean('Temp')
    respiration = fields.Boolean('Respiration')
    urine_output = fields.Boolean('Urine Output')
    ibp = fields.Boolean('IBP')
    cv_line= fields.Boolean('CV Line')
    ng_og_tube= fields.Boolean('NG/OG Tube')
    foleys_catheter = fields.Boolean('Foley`s Catheter')
    iv_line = fields.Boolean('IV Line')
    iv_line_note = fields.Char('IV Note')
    arterial_line= fields.Boolean('Arterial Line')
    arterial_line_note = fields.Char('Arterial Note')
    other = fields.Boolean('Other')
    other_note = fields.Char('Other Note')
#     #Advices:
    advices_1 = fields.Boolean('W/f hourly Temperature,Pulse, Blood Pressure, SPO2, Respiration, Cyanosis.')
    advices_2 = fields.Boolean('W/f Urine output, I/O Charting.')
    advices_3 = fields.Boolean('W/f Drain output.')
    advices_4 = fields.Boolean('O2 Therapy @')
    o2_theory_note = fields.Char('O2 Theory Note')
    mask_O2 = fields.Boolean('Mask O2')
    nasal_cannula = fields.Boolean('Nasal Cannula')
    t_piece = fields.Boolean('T-piece')
    oral_nasal_airway = fields.Boolean('Oral/Nasal Airway')
    ett = fields.Boolean('ETT/Tracheostomy Care')
    t_stomy = fields.Boolean('T-stomy')
    diet = fields.Boolean('Diet')
    diet_liquid_ml = fields.Char('Liquid')
    diet_liquid_hr = fields.Char('Liquid')
    diet_semisolid_ml = fields.Char('Semi-Solid')
    diet_semisolid_hr = fields.Char('Semi-Solid')
    diet_solid_ml = fields.Char('Solid')
    diet_solid_hr = fields.Char('Solid')
    nbm = fields.Boolean('NBM')
    nbm_note = fields.Char('NBM Value')
    oral = fields.Boolean('Oral')
    ryles_tube = fields.Boolean('Ryle`s Tube')
    ryles_tube_note = fields.Char('Ryles Tube Value')
    transparent = fields.Boolean('Transparent')
    non_transparent = fields.Boolean('Non Transparent')
    solids = fields.Boolean('Solids')
    ad_card_supt = fields.Boolean('Cardiorespiratory Support')
    ad_card_supt_note = fields.Char('Cardiorespiratory Support Note')
    ad_infusions = fields.Boolean('Infusions')
    ad_infusions_note = fields.Char('Advice Infusions Note')
    ad_other = fields.Boolean('Other')
    ad_other_note = fields.Char('Advice Other Note')
    #IV Fluids
    iv_fluids = fields.Boolean('IV Fluids')
    iv_fluids_note = fields.Char('IV Fluids Note')
    iv_fluids_note1 = fields.Char('IV Fluids Note 1')
#     #Ix Advised:
    ix_advised = fields.Boolean('Ix Advised')
    ix_advised_note = fields.Text('Ix Advised Note')
#     #References:
    references = fields.Boolean('References')
    references_note = fields.Text('References Note')
    eye_value = fields.Selection([
        ('spotaneously', 'Spotaneously'),
        ('to_speech', 'To Speech'),
        ('to_pain', 'To Pain'),
        ('no_response', 'No Response'),
    ], string='Eye', default = 'spotaneously')
    eye_score = fields.Integer('Score')
    best_verbal_value = fields.Selection([
        ('oriented_time_person', 'Oriented to time, Place & Person'),
        ('confused', 'Confused'),
        ('inappropriated_words', 'Inappropriated Words'),
        ('incomprehensible_sounds', 'Incomprehensible Sounds'),
        ('no_response','No Response'),
    ], string='Verbal',default = 'oriented_time_person')
    best_verbal_score = fields.Integer('Score')
    best_motor_value = fields.Selection([
        ('obeys_commands', 'Obeys Commands'),
        ('moves_localized', 'Moves to Localized Pain '),
        ('flexion_drawal', 'Flexion withdrawal From Pain'),
        ('abnornal_flexion', 'Abnormal Flexion'),
        ('abnormal_extension','Abnormal Extension'),
        ('no_response','No Response'),
    ], string='Motor',default = 'obeys_commands')
    best_motor_score = fields.Integer('Score')
    gcs_final_total = fields.Integer('GCS Total Score',compute='_gcs_total')
    msg = fields.Char('Message')
    pupil_note = fields.Text('Pupile Note')


    @api.model
    def create(self, vals):
        res = super(ICUWelcome, self).create(vals)
        res.name = self.env['ir.sequence'].next_by_code('hms.icu.welcome') or ''
        return res

    @api.onchange('eye_value')
    def onchange_eye_selection(self):
            if self.eye_value == "spotaneously":
                self.eye_score = '4'
            if self.eye_value == "to_speech":
                self.eye_score = '3'
            if self.eye_value == "to_pain":
                self.eye_score = '2'
            if self.eye_value == "no_response":
                self.eye_score = '1'

    @api.onchange('best_verbal_value')
    def onchange_verbal_selection(self):
            if self.best_verbal_value == "oriented_time_person":
                self.best_verbal_score = '5'
            if self.best_verbal_value == "confused":
                self.best_verbal_score = '4'
            if self.best_verbal_value == "inappropriated_words":
                self.best_verbal_score = '3'
            if self.best_verbal_value == "incomprehensible_sounds":
                self.best_verbal_score = '2'
            if self.best_verbal_value == "no_response":
                self.best_verbal_score = '1'


    @api.onchange('best_motor_value')
    def onchange_motor_selection(self):
            if self.best_motor_value == "obeys_commands":
                self.best_motor_score = '6'
            if self.best_motor_value == "moves_localized":
                self.best_motor_score = '5'
            if self.best_motor_value == "flexion_drawal":
                self.best_motor_score = '4'
            if self.best_motor_value == "abnornal_flexion":
                self.best_motor_score = '3'
            if self.best_motor_value == "abnormal_extension":
                self.best_motor_score = '2'
            if self.best_motor_value == "no_response":
                self.best_motor_score = '1'

    @api.depends('eye_value','best_verbal_value','best_motor_value')
    def _gcs_total(self):
        self.gcs_final_total = self.eye_score + self.best_verbal_score + self.best_motor_score


    @api.onchange('gcs_final_total')
    def onchange_gcs_msg(self):
        if self.gcs_final_total <= 8:
            self.msg = _('GCS Value is Low to the Minimum Value')
        else:
            self.msg = ''

    @api.model
    def icu_welcome_doctor(self, fields):
        return {
            'name': _('Doctor Chart'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'hms.icu.chart',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.patient_id.id), ('inpatient_id', '=', self.inpatient_id.id)],
            'context': {
                        'default_inpatient_id': self.inpatient_id.id,
                        'default_patient_id': self.patient_id.id,
                        'form_view_ref':'hms_icu.view_hms_icu_chart1_form',
                        'default_type':'chart1',
                    },
        }

class Complain(models.Model):
    _name = 'hms.icu.welcome.complain.line'

    name = fields.Many2one('hms.icu.complain', 'Name')
    days = fields.Char('Day(Duration)')
    welcome_complain_id = fields.Many2one('hms.icu.welcome', 'Appointment Id', ondelete='cascade')


class Complain(models.Model):
    _name = 'hms.icu.complain'

    name = fields.Char('Name')


class ICUAddictionHO(models.Model):
    _name = 'hms.icu.addiction.ho'

    ho_addiction_name = fields.Selection([
        ('smoking', 'H/O Smoking'),
        ('tobacco', 'H/O Tobacco'),
        ('alcoholism', 'H/O Alcoholism'),
        ('street_drugs', 'H/O Street Drugs'),
    ], string='Addiction')
    ho_addiction_value = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Yes/No')
    ho_other_value = fields.Char('Frequency')
    icu_ho_addiction_id = fields.Many2one('hms.icu.welcome', 'HO Addiction Id')


class ICUDiagnosis(models.Model):
    _name = 'hms.icu.diagnosis'
    
    diagnosis_id = fields.Many2one('hms.diseases', 'Diagnosis')
    diagnosiss_id = fields.Many2one('hms.icu.chart', 'Diagnosiss Id', ondelete='cascade')


class ICUChart(models.Model):
    _name = 'hms.icu.chart'
    _order = 'icu_chart_date desc'

    def _get_intake_ids(self):
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result

    def _get_output_ids(self):
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result

    def _get_vitals_ids(self): 
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result

    def _get_infusion_pumps_ids(self):
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result

    def _get_venti_setting_ids(self):
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result

    def _get_pts_entilatory_ids(self):
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result

    def _get_icu_chart_other_ids(self):
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result

    name = fields.Char(string="ID",default=lambda self: _('New')) #default=lambda self: _('New')
    icu_chart_date = fields.Datetime('Date',default=fields.Datetime.now)
    type = fields.Selection([('chart1','ICU Nursing Chart'),('chart2','Doctor Chart')], string="Type")
    patient_id = fields.Many2one('banastech.hms.patient', string="Patient", required=True)
    code = fields.Char(related='patient_id.code',size=256, string='Patient ID')
    inpatient_id = fields.Many2one('inpatient.registration', string="InPatient")
    image = fields.Binary(related='patient_id.image',string='Image')
    age =  fields.Char(related='patient_id.age', string='Age', readonly=True)
    gender =  fields.Selection(related='patient_id.gender', string='Gender', readonly=True)
    chart_blood_group = fields.Selection(related='patient_id.blood_group', string='Blood Group',readonly=True)
    cm = fields.Float(string="Height(cm)")
    weight = fields.Float(string='Weight')
    intake_ids = fields.One2many('hms.icu.intake', 'intake_id', 'Intake', default=lambda self: self._get_intake_ids())
    output_ids = fields.One2many('hms.icu.intack.output','output_id','Output', default=lambda self: self._get_output_ids())
    tpn_orders_ids = fields.One2many('hms.icu.tpn.order','tpn_order_id','TPN Orders')
    fluid_orders_ids = fields.One2many('hms.icu.fluid.order','fluid_order_id','FLUID Orders')
    infusion_orders_ids = fields.One2many('hms.icu.infusion.orders','infusion_order_id','Infusion Orders')
    parent_id = fields.Many2one('hms.icu.chart', string="Past Record")
    parent_id2 = fields.Many2one('hms.icu.chart', string="Past Record")
    in_iv = fields.Float('IV',compute='_get_intake_total',track_visibility='onchange',store=False)
    in_oral = fields.Float('Oral',compute='_get_intake_total',track_visibility='onchange',store=False)
    in_rtf = fields.Float('RTF',compute='_get_rtoral_total',track_visibility='onchange',store=False)
    in_infusion = fields.Float('Infusion',compute='_get_intake_total',track_visibility='onchange',store=False)
    in_other = fields.Float('Other',compute='_get_intake_total',track_visibility='onchange',store=False)
    in_total_intake = fields.Float('Total Intake',compute='_get_intake_total',track_visibility='onchange',store=False)
    ot_uo = fields.Float('UO',compute='_get_output_total',track_visibility='onchange')
    ot_rta = fields.Float('RTA',compute='_get_output_total',track_visibility='onchange')
    ot_blood_loss = fields.Char('Blood Loss')
    ot_dialysis = fields.Char('Dialysis')
    ot_stool = fields.Float('Stool',compute='_get_output_total',track_visibility='onchange')
    ot_vomiting = fields.Char('Vomiting')
    ot_do = fields.Char('D/o')
    ot_drain1 = fields.Char('Drain-1')
    ot_drain2 = fields.Char('Drain-2')
    ot_ileostomy = fields.Char('Ileostomy')
    ot_total_output = fields.Float('Total Output',compute='_get_output_total',track_visibility='onchange')
    in_ot_balance = fields.Float('Balance',compute='_in_ot_balance_value')
    diagnosis_ids = fields.One2many('hms.icu.diagnosis','diagnosiss_id','Diagnosis')
    prescription_ids = fields.One2many('hms.icu.prescription','prescription_id','Prescription')
    other_rx_ids = fields.One2many('hms.icu.other.rx','other_rx_id','Other Rx')
    rt_oral_feeding = fields.Text('Note')
    rt_oral_dietplan_ids = fields.One2many('hms.icu.rtoral.dietplan','rtoral_dietplan_id','Diet Plan')
    rt_oral_feeding_ids = fields.One2many('hms.icu.rtoral.feeding','rt_oral_feeding_id','RT/Oral Feeding')
#     rt_oral_feeding_total = fields.Float('RT/Oral Total')
    once_only_drug_ids = fields.One2many('hms.icu.once.only.drug','once_only_drug_id','Once Only Drug')
    prescription_diabetes_ids = fields.One2many('hms.icu.prescription.diabetes','prescription_diabetes_id','Diabetes')
#     #ICU Chart 2 General Informatoin
    icu_generalinf_date = fields.Datetime(string='Date',default=fields.Datetime.now)
    icu_post_op_day = fields.Char('Post Op Day')
    icu_stay_day = fields.Char('Stay Day')
    icu_iv_line  = fields.Char('IV Line')
    icu_cpv_dlc  = fields.Char('CVP/DLC Line')
    icu_ett_trac = fields.Char('ETT/Tracheostomy Care')
    icu_foleys_cath = fields.Char('Foleys Catheter No.')
    icu_ryles_tube_no = fields.Char('Ryles Tube No.')
    icu_arterial_line = fields.Char('Arterial Line')
#     general_information_id = fields.Many2one('hms.icu.chart', 'General Info', ondelete='cascade')
    past_post_op_day = fields.Char(related="parent_id2.icu_post_op_day", string='Post Op Day',compute='_get_generalinformation',track_visibility='onchange')
    past_stay_day = fields.Char(related="parent_id2.icu_stay_day", string='Stay Day',compute='_get_generalinformation',track_visibility='onchange')
    past_iv_line  = fields.Char(related="parent_id2.icu_iv_line", string='IV Line',compute='_get_generalinformation',track_visibility='onchange')
    past_cpv_dlc  = fields.Char(related="parent_id2.icu_cpv_dlc", string='CVP/DLC Line',compute='_get_generalinformation',track_visibility='onchange')
    past_ett_trac = fields.Char(related="parent_id2.icu_ett_trac", string='ETT/Tracheostomy Care',compute='_get_generalinformation',track_visibility='onchange')
    past_foleys_cath = fields.Char(related="parent_id2.icu_foleys_cath", string='Foleys Catheter No.',compute='_get_generalinformation',track_visibility='onchange')
    past_ryles_tube_no = fields.Char(related="parent_id2.icu_ryles_tube_no", string='Ryles Tube No.',compute='_get_generalinformation',track_visibility='onchange')
    past_arterial_line = fields.Char(related="parent_id2.icu_arterial_line", string='Arterial Line',compute='_get_generalinformation',track_visibility='onchange')
    oral_care_1 = fields.Char('ORAL CARE')
    oral_care_2 = fields.Char('ORAL CARE')
    sponge_bath_1 = fields.Char('Sponge BATH/ BATH')
    sponge_bath_2 = fields.Char('Sponge BATH/ BATH')
    back_care_1 = fields.Char('Back Care')
    back_care_2 = fields.Char('Back Care')
    urinary_cath_care_1 = fields.Char('Urinary Catheter Care')
    urinary_cath_care_2 = fields.Char('Urinary Catheter Care')
    hair_care_1 = fields.Char('Hair Care')
    hair_care_2 = fields.Char('Hair Care')
    surgical_wound_desg_1 = fields.Char('Surgical Wound Dressing')
    surgical_wound_desg_2 = fields.Char('Surgical Wound Dressing')
#     #Vital Signs.
    vitals_ids = fields.One2many('hms.icu.vitals','vitals_id','Vitals',default=lambda self: self._get_vitals_ids())
#     #Infusion Pumps
    inf_pump_value_day_ids = fields.One2many('infusion.pumps.value.day','inf_pump_value_id_day','Inf.Pumps')
    inf_pump_value_night_ids = fields.One2many('infusion.pumps.value.night','inf_pump_value_id_night','Inf.Pumps')
#     #Venti Setting
    venti_setting_ids = fields.One2many('hms.icu.venti.setting','venti_setting_id','Venti Setting',default=lambda self: self._get_venti_setting_ids())
#     #PTs Entilatory
    pts_entilatory_ids = fields.One2many('hms.icu.pts.entilatory','pts_entilatory_id','PTs Entilatory',default=lambda self: self._get_pts_entilatory_ids())
#     #Other
    icu_chart_other_ids = fields.One2many('hms.icu.chart.other','chart_other_id','Other',default=lambda self: self._get_icu_chart_other_ids())
    special_inst = fields.Text('Special Instructions')
#     #TODAYS INVESTIGATION - REPORTS
    hb = fields.Char('HB')
    tc = fields.Char('TC')
    dc = fields.Char('DC')
    platelet = fields.Char('Platelet Count')
    urea = fields.Char('UREA')
    creatinine = fields.Char('Creatinine')
    pt = fields.Char('PT')
    aptt = fields.Char('APTT')
    bt_ct = fields.Char('BT,CT')
    blood_group = fields.Selection(related='patient_id.blood_group', string='Blood Group')
    crp = fields.Char('CRP')
    abg_1 = fields.Char('ABG')
    abg_2 = fields.Char('ABG')
    abg_3 = fields.Char('ABG')
    ph_1 = fields.Char('PH')
    ph_2 = fields.Char('PH')
    ph_3 = fields.Char('PH')
    paco2_1 = fields.Char('PaCO2')
    paco2_2 = fields.Char('PaCO2')
    paco2_3 = fields.Char('PaCO2')
    pao2_1 = fields.Char('PaO2')
    pao2_2 = fields.Char('PaO2')
    pao2_3  = fields.Char('PaO2')
    tco2_1 = fields.Char('TCO2')
    tco2_2 = fields.Char('TCO2')
    tco2_3 = fields.Char('TCO2')
    hco2_1 = fields.Char('HCO3')
    hco2_2 = fields.Char('HCO3')
    hco2_3 = fields.Char('HCO3')
    be_1 = fields.Char('Be')
    be_2 = fields.Char('Be')
    be_3 = fields.Char('Be')
    sao2_1 = fields.Char('SaO2')
    sao2_2 = fields.Char('SaO2')
    sao2_3 = fields.Char('SaO2')
    fio2_1 = fields.Char('FIO2')
    fio2_2 = fields.Char('FIO2')
    fio2_3 = fields.Char('FIO2')
    ti_ecg = fields.Char('ECG')
    elec_note = fields.Text('Viral Marker')
    xray_note = fields.Text('Comment')
    sgpt = fields.Char('SGPT')
    sgot = fields.Char('SGOT')
    s_alk = fields.Char('S.Alk')
    s_bil_total = fields.Char('S.Bil.Total')
    s_bil_direct = fields.Char('S.Bil.Direct')
    s_bil_indirect = fields.Char('S.Bil.Indirect')
    s_protein_total = fields.Char('S.Protein Total')
    s_protein_ab = fields.Char('S.Protein Ab')
    s_protein_glob = fields.Char('S.Protein Glob')
    any_other_ixs = fields.Char('Any Other ixs')
    na_plus = fields.Char('Na+')
    k_plus = fields.Char('K+')
    cl_plus = fields.Char('Cl+')
    ca_pplus = fields.Char('Ca++')
    mgpplus = fields.Char('Mg++')
    elec_blood_group = fields.Char(string='Blood Group')
      
#     #DIABETIC FLOW CHART
    diabetic_chart_flow_ids = fields.One2many('hms.icu.diabetic.chart.flow','diabetic_chart_flow_id','Diabetic Flow Chart')
#     #Importand Events and Todays Plan
    note_1 = fields.Text('Note:-1')
    note_2 = fields.Text('Note:-2')
    ref_1 = fields.Char('References:-1')
    ref_2 = fields.Char('References:-2')
    ref_3 = fields.Char('References:-3')
    created_by = fields.Char('Created By')
    create_timestamp = fields.Datetime('Created Date', default=lambda self: time.strftime('%Y-%m-%d %H:%M:%S'))
#     admission_reason = fields.Many2one ('hms.diseases', ondelete="restrict", string='Reason for Admission', help="Reason for Admission")
#     attending_physician_ids = fields.Many2many('hms.physician','hosp_pri_att_doc_rel','hosp_id','doc_id',string='Attending Physician')
#     rbs_total = fields.Float('RBS Total',compute='_get_rbs_total')
    state = fields.Selection([('draft', 'IN ICU'),('done', 'Done'),],default='draft',string='State')
#     is_max = fields.Integer(compute='_compute_is_max', string="Max")

#     @api.multi
#     def indimedi_icu_chart_one(self):
#         action = self.env.ref('hms_icu.action_icu_chart1')
#         result = action.read()[0]
#         result['context'] = {'default_inpatient_id': self.inpatient_id.id,
#             'default_patient_id': self.patient_id.id,
#             'tree_view_ref':'hms_icu.view_hms_icu_chart1_tree',
#             'form_view_ref':'hms_icu.view_hms_icu_chart1_form',
#             'default_type':'chart1',
#         }
#         result['domain'] = [('patient_id', '=', self.patient_id.id), ('inpatient_id', '=', self.inpatient_id.id)]
#         if len(self) == 1:
#             res = self.env.ref('hms_icu.view_hms_icu_chart1_form', False)
#             result['views'] = [(res and res.id or False, 'form')]
#             result['res_id'] = self.id
#         return result


    #all code well
    @api.model
    def indimedi_icu_chart_two(self, fields):
        action = self.env.ref('hms_icu.action_icu_chart2')
        result = action.read()[0]
        result['context'] = {'default_inpatient_id': self.inpatient_id.id,
            'default_patient_id': self.patient_id.id,
            'tree_view_ref':'hms_icu.view_hms_icu_chart2_tree',
            'form_view_ref':'hms_icu.view_hms_icu_chart2_form',
            'default_type':'chart2',
        }
        result['domain'] = [('patient_id', '=', self.patient_id.id), ('inpatient_id', '=', self.inpatient_id.id)]
        if len(self) == 1:
            res = self.env.ref('hms_icu.view_hms_icu_chart2_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.id
        return result
   
#     @api.multi
#     def _compute_is_max(self):
#         for chart in self:
#             chart.is_max = self.venti_setting_ids.ids and max(self.venti_setting_ids.ids) or 0

    @api.model
    def create(self, vals):
        res = super(ICUChart, self).create(vals)
        res.name = self.env['ir.sequence'].next_by_code('hms.chart.icu') or ''
        return res


#     @api.model
#     def icu_schedluarr(self):
#         icu_scheduler_obj = self.env['hms.icu.chart']
#         domain = [
#             ('state','=','draft'),
#             ('icu_chart_date', '<', datetime.now().strftime('%Y-%m-%d 00:00:00'))
#         ]
#         scheduler_ids = icu_scheduler_obj.search(domain)
#         if scheduler_ids:
#             for scheduler_id in scheduler_ids:
#                 scheduler_id.write({'state': 'done'})
    
#     @api.model
#     def cron_create_icu_venti_setting_id(self):
#         domain = [
#             ('state','=','draft'),
#             ('icu_chart_date', '>=', datetime.now().strftime('%Y-%m-%d 00:00:00')),
#             ('icu_chart_date', '<=', datetime.now().strftime('%Y-%m-%d 23:59:59'))
#         ]

#         for chart in self.search(domain):
#             if chart.venti_setting_ids:
#                 domain_line = [('venti_setting_id', '=', chart.id),
#                 ('create_date', '<=', (datetime.now()+timedelta(hours=1)).strftime(DT)),
#                 ('copyed', '=', False)]
#                 scheduler_ids = chart.venti_setting_ids.search(domain_line)
#                 if scheduler_ids:
#                     max_id = max(scheduler_ids.ids)
#                     max_id = chart.venti_setting_ids.browse([max_id])
#                     flag = False
#                     val_index = None
#                     if max_id.time != '7_8':
#                         try:
#                             val_index = selection_time_key.index(str(max_id.time))
#                             max_id.copyed = True
#                             new_id = max_id.copy(default={'time': selection_time_key[val_index+1]})
#                         except:
#                             pass

#     @api.onchange('icu_chart_date', 'patient_id')
#     def onchange_icu_chart_date(self):
#         if self.icu_chart_date:
#             date_time = (datetime.strptime(self.icu_chart_date, DT)-timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
#             date_time2 = (datetime.strptime(self.icu_chart_date, DT)-timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')
#             domain = [('patient_id', '=', self.patient_id.id), 
#                 ('icu_chart_date', '>=', date_time),
#                 ('icu_chart_date', '<=', date_time2),
#                 ]
#             parent = self.search(domain, limit=1)
#             self.parent_id = parent.id
#             vals = []
#             if not self.diagnosis_ids:
#                 for diagnosis in parent.diagnosis_ids:
#                     vals.append((0, 0, {
#                         'diagnosis_id': diagnosis.diagnosis_id,
#                     }))
#                 self.diagnosis_ids = vals

#             vals = []
#             if not self.prescription_ids:
#                 for prescription in parent.prescription_ids:
#                     if prescription.product_id.id:
#                         vals.append((0, 0, {
#                             'day_no': prescription.day_no,
#                             'product_id': prescription.product_id.id,
#                             'pre_route': prescription.pre_route,
#                             'common_dosage': prescription.common_dosage,
#                             'pre_time_1': prescription.pre_time_1,
#                             'pre_time_2': prescription.pre_time_2,
#                             'pre_time_3': prescription.pre_time_3,
#                             'pre_time_4': prescription.pre_time_4,
#                         }))
#                 self.prescription_ids = vals 

#             vals = []
#             if not self.other_rx_ids:
#                 for other_rx in parent.other_rx_ids:
#                     if other_rx.product_id.id:
#                         vals.append((0, 0, {
#                             'product_id': other_rx.product_id.id,
#                             'common_dosage': other_rx.common_dosage,
#                             'rx_time_1': other_rx.rx_time_1,
#                             'rx_time_2': other_rx.rx_time_2,
#                             'rx_time_3': other_rx.rx_time_3,
#                             'rx_time_4': other_rx.rx_time_4,
#                         }))
#                 self.other_rx_ids = vals

#             vals = []
#             if not self.once_only_drug_ids:
#                 for once_only_drug in parent.once_only_drug_ids:
#                     if once_only_drug.product_id.id:
#                         vals.append((0, 0, {
#                             'product_id': once_only_drug.product_id.id,
#                             'common_dosage': once_only_drug.common_dosage,
#                             'dose': once_only_drug.dose,
#                             'route': once_only_drug.route,
#                             'time_given': once_only_drug.time_given,
#                             'nurse_name': once_only_drug.nurse_name,
#                         }))
#                 self.once_only_drug_ids = vals

#             vals = []
#             if not self.prescription_diabetes_ids:
#                 for pre_diabetes in parent.prescription_diabetes_ids:
#                     if pre_diabetes.diabetes_rbs:
#                         vals.append((0, 0, {
#                             'diabetes_rbs': pre_diabetes.diabetes_rbs,
#                             'diabetes_insulin': pre_diabetes.diabetes_insulin,
#                             'diabetes_msg': pre_diabetes.diabetes_msg,
#                         }))
#                 self.prescription_diabetes_ids = vals

#             vals = []
#             if not self.tpn_orders_ids:
#                 for tpn in parent.tpn_orders_ids:
#                     if tpn.tpn_drugs:
#                         vals.append((0, 0, {
#                             'tpn_date': tpn.tpn_date,
#                             'tpn_drugs': tpn.tpn_drugs,
#                             'tpn_rate': tpn.tpn_rate,
#                             'tpn_comments': tpn.tpn_comments,
#                         }))
#                 self.tpn_orders_ids = vals

#             vals = []
#             if not self.fluid_orders_ids:
#                 for fluid in parent.fluid_orders_ids:
#                     if fluid.fluid_drugs.id:
#                         vals.append((0, 0, {
#                             'fluid_date': fluid.fluid_date,
#                             'fluid_drugs': fluid.fluid_drugs,
#                             'fluid_rate': fluid.fluid_rate,
#                             'fluid_comments': fluid.fluid_comments,
#                         }))
#                 self.fluid_orders_ids = vals

#             vals = []
#             if not self.infusion_orders_ids:
#                 for infusion in parent.infusion_orders_ids:
#                     if infusion.infusion_orders_drugs.id:
#                         vals.append((0, 0, {
#                             'infusion_orders_date': infusion.infusion_orders_date,
#                             'infusion_orders_drugs': infusion.infusion_orders_drugs.id,
#                             'infusion_orders_dose': infusion.infusion_orders_dose,
#                             'infusion_orders_diluent': infusion.infusion_orders_diluent,
#                             'infusion_orders_rate': infusion.infusion_orders_rate,
#                             'infusion_orders_comments': infusion.infusion_orders_comments,
#                         }))
#                 self.infusion_orders_ids = vals
                
#             vals = []
#             if not self.rt_oral_feeding_ids:
#                 for rtoral in parent.rt_oral_feeding_ids:
#                     if rtoral.rt_of_ml:
#                         vals.append((0, 0, {
#                             'rt_of_feed': rtoral.rt_of_feed,
#                             'rt_of_ml': rtoral.rt_of_ml,
#                             'rt_of_time': rtoral.rt_of_time,
#                         }))
#                 self.rt_oral_feeding_ids = vals
#             # return {'domain': {'parent_id': domain}}

   
#     @api.depends('intake_ids')
#     def _get_intake_total(self):
#             for icu in self:
#                 for line in icu.parent_id.intake_ids:
#                     icu.in_iv += line.intake_hr_1
#                     icu.in_oral += line.intake_hr_2
#                     icu.in_infusion += line.intake_hr_3
#                     icu.in_other += line.intake_hr_4
#                     icu.in_total_intake += line.hourly_total

#     @api.depends('output_ids')
#     def _get_output_total(self):
#         for icu in self:
#                 for line in icu.parent_id.output_ids:
#                         icu.ot_uo += line.u_o
#                         icu.ot_rta += line.rta
#                         icu.ot_stool += line.stool
#                         icu.ot_total_output += line.total

#     @api.depends('in_total_intake','ot_total_output')
#     def _in_ot_balance_value(self):
#         for line in self:
#             line.in_ot_balance = line.in_total_intake - line.ot_total_output

#     @api.depends('rt_oral_feeding_ids')
#     def _get_rtoral_total(self):
#         for icu in self:
#                 for line in icu.parent_id.rt_oral_feeding_ids:
#                         icu.in_rtf += line.rt_of_ml
                      
   
#     @api.onchange('icu_generalinf_date', 'patient_id')
#     def onchange_icu_generalinf_date(self):
#         if self.icu_generalinf_date:
#             datetime1 = (datetime.strptime(self.icu_generalinf_date, DT)-timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
#             datetime2 = (datetime.strptime(self.icu_generalinf_date, DT)-timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')
#             domain = [('patient_id', '=', self.patient_id.id), 
#                 ('icu_generalinf_date', '>=', datetime1),
#                 ('icu_generalinf_date', '<=', datetime2),
#                 ]
#             self.parent_id2 = self.search(domain, limit=1).id

    
#     # @api.depends('diabetic_flow_chart_ids')
#     # def _get_rbs_total(self):
#     #     for icu in self:
#     #         for line in icu.diabetic_flow_chart_ids:
#     #             icu.rbs_total += line.rbs*100

    
#     @api.multi
#     def icu_treatment_sheet(self):
#         return {
#             'name': _('Treatment Sheet'),
#             'view_type': 'form',
#             'view_mode': 'form,tree',
#             'res_model': 'hms.treatment',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id','=',self.id)],
#             'context': {
#                 'default_patient_id': self.id,
#                 'form_view_ref': 'hms_treatment.view_devasya_hms_treatment_form'
#             },
#         }

class ICUDiabeticChartFlow(models.Model):
    _name = 'hms.icu.diabetic.chart.flow'
    
    time = fields.Selection(selection_time,'Time')
    bsl = fields.Char('BSL(mg/dl)')
    insulin = fields.Char('Insulin(unit)')
    diabetic_chart_flow_id = fields.Many2one('hms.icu.chart', 'Diabetic Flow Chart Id', ondelete='cascade')


class ICUChartIntake(models.Model):
    _name = 'hms.icu.intake'

    time = fields.Selection(selection_time,'Time')
    intake_hr_1 = fields.Float('IV')
    intake_hr_2 = fields.Float('Oral')
    intake_hr_3 = fields.Float('Infusion')
    intake_hr_4 = fields.Float('Other')
    hourly_total = fields.Float('Total')
    intake_id = fields.Many2one('hms.icu.chart', 'Intake Id', ondelete='cascade')

    @api.onchange('intake_hr_1','intake_hr_2','intake_hr_3','intake_hr_4')
    def on_total_hourly(self):
       self.hourly_total = float(self.intake_hr_1) + float(self.intake_hr_2) + float(self.intake_hr_3) + float(self.intake_hr_4)


class ICUChartIntake(models.Model):
    _name = 'hms.icu.intack.output'

    time = fields.Selection(selection_time,'Time')
    u_o = fields.Float('U/O')
    drain = fields.Float('Drain')
    rta = fields.Float('Rta')
    stool = fields.Float('stool')
    total = fields.Float('Total')
    output_id = fields.Many2one('hms.icu.chart', 'Output Id', ondelete='cascade')


    @api.onchange('u_o','drain','rta','stool')
    def onchange_total_output(self):
       self.total = float(self.u_o) + float(self.drain) + float(self.rta) + float(self.stool)


class ICUPrescription(models.Model):
    _name = 'hms.icu.prescription'

    day_no = fields.Integer('Day No.')
    product_id = fields.Many2one('product.product', string='Antibiotic')
    pre_route = fields.Char('Route')
    common_dosage = fields.Many2one('banas.hms.medication.dosage', ondelete='cascade', string='Frequency')
    pre_time_1 = fields.Selection(related='common_dosage.t1',string='Time')
    pre_time_2 = fields.Selection(related='common_dosage.t2',string='Time')
    pre_time_3 = fields.Selection(related='common_dosage.t3',string='Time')
    pre_time_4 = fields.Selection(related='common_dosage.t4',string='Time')
    prescription_id = fields.Many2one('hms.icu.chart', 'Prescription Id', ondelete='cascade')

class ICUOtherRx(models.Model):
    _name = 'hms.icu.other.rx'

    product_id = fields.Many2one('product.product','Drugs')
    common_dosage = fields.Many2one('banas.hms.medication.dosage', ondelete='cascade', string='Frequency')
    rx_time_1 = fields.Selection(related='common_dosage.t1',string='Time')
    rx_time_2 = fields.Selection(related='common_dosage.t2',string='Time')
    rx_time_3 = fields.Selection(related='common_dosage.t3',string='Time')
    rx_time_4 = fields.Selection(related='common_dosage.t4',string='Time')
    other_rx_id = fields.Many2one('hms.icu.chart', 'Prescription Id', ondelete='cascade')

class ICUOnceOnlyDrug(models.Model):
    _name = 'hms.icu.once.only.drug'

    product_id = fields.Many2one('product.product','Name of Drug')
    common_dosage = fields.Many2one('banas.hms.medication.dosage', ondelete='cascade', string='Frequency')
    dose = fields.Char('Dose')
    route = fields.Char('Route')
    time_given = fields.Selection(selection_time,'Time Given')
    nurse_name = fields.Char('Nurse Name')
    once_only_drug_id = fields.Many2one('hms.icu.chart', 'Once Only Drug Id', ondelete='cascade')

class ICUPrescriptionDiabetes(models.Model):
    _name = 'hms.icu.prescription.diabetes'

    diabetes_rbs = fields.Selection([('100_150','100-150'),('151_200','151-200'),('201_250','201-250'),
                                     ('251_300','251-300'),('301_350','301-350'),('morethan351','>351'),
                                     ('lessthan80','<80')
                                    ],string='RBS')
    diabetes_insulin = fields.Char(string='Insulin')
    diabetes_msg = fields.Char('Message')
    prescription_diabetes_id = fields.Many2one('hms.icu.chart','Prescription Diabetes',ondelete='cascade')

    @api.onchange('diabetes_rbs')
    def onchange_diabetes_rbs_value(self):
        if self.diabetes_rbs == "morethan351":
            self.diabetes_msg = 'Inform'
        elif self.diabetes_rbs == "lessthan80":
            self.diabetes_msg = 'Inform'
        else:
            self.diabetes_msg = ''

class ICUTPNOrder(models.Model):
    _name = 'hms.icu.tpn.order'

    tpn_date = fields.Datetime('Date',default=fields.Datetime.now)
    tpn_drugs = fields.Many2one('product.product','Drugs')
    tpn_rate = fields.Char('Rate(ml/Hr)')
    tpn_comments = fields.Char('Comments')
    tpn_order_id = fields.Many2one('hms.icu.chart', 'TPN Order Id', ondelete='cascade')


class ICUFluidOrder(models.Model):
    _name = 'hms.icu.fluid.order'

    fluid_date = fields.Datetime('Date',default=fields.Datetime.now)
    fluid_drugs = fields.Many2one('product.product','Drugs')
    fluid_rate = fields.Char('Rate(ml/Hr)')
    fluid_comments = fields.Char('Comments')
    fluid_order_id = fields.Many2one('hms.icu.chart', 'Fluid Order Id', ondelete='cascade')


class ICUInfusionOrder(models.Model):
    _name = 'hms.icu.infusion.orders'

    infusion_orders_date = fields.Datetime('Date',default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    infusion_orders_drugs = fields.Many2one('product.product','Drugs')
    infusion_orders_dose = fields.Char('Dose')
    infusion_orders_diluent = fields.Char('Diluent')
    infusion_orders_rate = fields.Char('Rate(ml/Hr)')
    infusion_orders_comments = fields.Char('Comments')
    infusion_order_id = fields.Many2one('hms.icu.chart', 'Infusion Order Id', ondelete='cascade')


class ICURtOralFeeding(models.Model):
    _name = 'hms.icu.rtoral.feeding'

    rt_of_feed = fields.Char('FEED')
    rt_of_ml = fields.Float('ML')
    rt_of_time = fields.Selection(selection_time,'Time')
    rt_oral_feeding_id = fields.Many2one('hms.icu.chart', 'RT/Oral Feeding Id', ondelete='cascade')

class ICURtoralDietPlan(models.Model):
    _name = 'hms.icu.rtoral.dietplan'

    dietplan_selection = fields.Selection([('full_diet','Full Diet'),('light_diet','Light Diet'),('blend_diet','Blend Diet'),
                                    ('liquid_diet','Liquid Diet'),('liquid_only','Liquid Only'),('clear_liquid','Clear Liquid')
                                    ,],string='Diet Plan')
    dietplan_value = fields.Many2many('icu.dietplan.value',string='Diet Value')
    rtoral_dietplan_id = fields.Many2one('hms.icu.chart','Diet Plan Id', ondelete='cascade')

class ICUDietValue(models.Model):
    _name = 'icu.dietplan.value'
    _rec_name = 'name'

    name = fields.Char(string='Diet Value')
    

class ICUVitals(models.Model):
    _name = 'hms.icu.vitals'

    time = fields.Selection(selection_time,'Time')
    vitals_temp = fields.Char('Temp(F)')
    vitals_rate = fields.Char('Heart Rate(/min)')
    vitals_nibp_ibp = fields.Char('NIBP/IBP(mmHg)')
    vitals_cvp = fields.Char('CVP')
    vitals_resp_rate = fields.Char('RESP. Rate(RR)')
    vitals_spo2 = fields.Char('SPO2')
    vitals_id = fields.Many2one('hms.icu.chart', 'Vitals Id', ondelete='cascade')


class ICUInfPumpValueDay(models.Model):
    _name = 'infusion.pumps.value.day'
    _rec_name = 'pumps_value_id'

    pumps_value_id = fields.Many2one('infusion.value.pumps','Infusion Pump')
    time_a = fields.Char('08-09 AM')
    time_b = fields.Char('09-10 AM')
    time_c = fields.Char('10-11 AM')
    time_d = fields.Char('11-12 AM')
    time_e = fields.Char('12-01 PM')
    time_f = fields.Char('01-02 PM')
    time_g = fields.Char('02-03 PM')
    time_h = fields.Char('03-04 PM')
    time_i = fields.Char('04-05 PM')
    time_j = fields.Char('05-06 PM')
    time_k = fields.Char('06-07 PM')
    time_l = fields.Char('07-08 PM')
    inf_pump_value_id_day = fields.Many2one('hms.icu.chart','INF Pump Value Day',ondelete='cascade')

class ICUInfPumpValueNight(models.Model):
    _name = 'infusion.pumps.value.night'
    _rec_name = 'pumps_value_id'

    pumps_value_id = fields.Many2one('infusion.value.pumps','Infusion Pump')
    time_m = fields.Char('08-09 PM')
    time_n = fields.Char('09-10 PM')
    time_o = fields.Char('10-11 PM')
    time_p = fields.Char('11-12 PM')
    time_q = fields.Char('12-01 AM')
    time_r = fields.Char('01-02 AM')
    time_s = fields.Char('02-03 AM')
    time_t = fields.Char('03-04 AM')
    time_u = fields.Char('04-05 AM')
    time_v = fields.Char('05-06 AM')
    time_w = fields.Char('06-07 AM')
    time_x = fields.Char('07-08 AM')
    inf_pump_value_id_night = fields.Many2one('hms.icu.chart','INF Pump Value Night',ondelete='cascade')


class ICUInfValuePump(models.Model):
    _name = 'infusion.value.pumps'
    _rec_name = 'pumps_value_name'

    pumps_value_name = fields.Char('Name')


class ICUVentiSetting(models.Model):
    _name = 'hms.icu.venti.setting'

    time = fields.Selection(selection_time,'Time', default='8_9')
    venti_mode = fields.Char('Mode')
    venti_fio2 = fields.Char('FiO2%')
    venti_tvml = fields.Char('TV ml[Pinsp/Phigh cm H2O][P high cm H2O]')
    venti_rate = fields.Char('Rate/min[P low cm H2O]')
    venti_ie = fields.Char('I:E|T insp s|T high s')
    venti_peep = fields.Char('PEEP cm H2O|T low s')
    venti_p_maxsupp = fields.Char('P max cm H2O|P supp cm H2O')
    venti_plimit = fields.Char('P limit')
    venti_trigger = fields.Char('Trigger')
    venti_setting_id = fields.Many2one('hms.icu.chart', 'Venti Setting Id', ondelete='cascade')
    is_max = fields.Boolean(compute='_get_is_max', string="Max")
    copyed = fields.Boolean('Copyed', default=False)

    @api.model
    def _get_is_max(self):
        for venti in self:
            if venti.venti_setting_id.is_max == venti.id:
                venti.is_max = True
            else:
                venti.is_max = False

    @api.model
    def action_one_hour_copy(self):
        self.copy(default={'venti_setting_id': self.venti_setting_id.id})


class ICUPtsEntilatory(models.Model):
    _name = 'hms.icu.pts.entilatory'

    time = fields.Selection(selection_time,'Time')
    ptsven_ppeak = fields.Char('P peak')
    ptsven_peepe = fields.Char('PEEPe')
    ptsven_mv = fields.Char('MVexp L/min')
    ptsven_rr = fields.Char('RR/min')
    ptsven_tv = fields.Char('TVexp ml')
    ptsven_compl = fields.Char('Compl ml/cm H2O')
    ptsven_raw = fields.Char('Raw cm H2O/L/S')
    ptsven_nebuliser = fields.Char('Nebuliser')
    pts_entilatory_id = fields.Many2one('hms.icu.chart', 'PTs Entilatory Id', ondelete='cascade')


class ICUChartOther(models.Model):
    _name = 'hms.icu.chart.other'

    time = fields.Selection(selection_time,'Time')
    bagg_suc_phy = fields.Char('Bagging|Suction|Physio')
    pt_position = fields.Selection([('supine','Supine'),('head_up','Head Up'),('foot_up','Foot Up'),
                                    ('right_lateral','Right Lateral'),('left_lateral','Left Lateral'),('prone','Prone'),
                                    ('head_low','Head Low'),('sitting','Sitting'),('cardial','Cardiac'),],string='PT.Position')
    gcs_emv = fields.Char('GCS E/V/M')
    ag = fields.Char('AG')
    other = fields.Char('Other')
    chart_other_id = fields.Many2one('hms.icu.chart', 'Other Id', ondelete='cascade')


# class ICUProgessNote(models.Model):
#     _name = 'hms.icu.progress.note'

#     name = fields.Char("Name", default="New")
#     patient_id = fields.Many2one('banastech.hms.patient', string="Patient", required=True)
#     image = fields.Binary(related='patient_id.image',string='Image')