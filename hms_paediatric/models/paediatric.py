from odoo import api, fields, models
from datetime import date, datetime, timedelta
from odoo.tools.translate import _

# class MedContent(models.Model):
#     _inherit = 'banas.hms.medicament.content'

#     minimum = fields.Float('Minimum')
#     maximum = fields.Float('Maximum')

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for content in self:
    #         name = content.name
    #         if content.minimum:
    #             name += '[min:'+ str(content.minimum)
    #         if content.maximum:
    #             name += ', max:'+ str(content.maximum)
    #         if content.minimum or content.maximum:
    #             name += ']'
    #         result.append((content.id, name))
    #     return result


class NewbornExaminationsFollow(models.Model):
    _name = 'hms.appointment.newborn.examinations.follow'

    appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment', invisible=True)
    nnr = fields.Char('NNR')
    jaundice = fields.Char('Jaundice')
    conjuctivities = fields.Char('Conjuctivities')
    skin_eruption = fields.Char('Skin Eruption')
    ymbilical_cord = fields.Char('Umbilical Cord')
    cvs_murmurs = fields.Char('CVS-Murmurs')
    vaccination_advice = fields.Char('Vaccination Advice')


class ChildMilestoneTemplate(models.Model):
    _name = "child.milestone.template"
    _description = "Children Milestone Template"

    name = fields.Char("Milestone")
    min_val = fields.Float("Minimum Months")
    max_val = fields.Float("Maximum Months")
    note = fields.Text("Note")


class ChildMilestone(models.Model):
    _name = "child.milestone"
    _description = "Children Milestone"

    name = fields.Char("Milestone")
    min_val = fields.Float("Minimum Months")
    max_val = fields.Float("Maximum Months")
    value = fields.Float("Value")
    note = fields.Text("Note")
    patient_id = fields.Many2one('banastech.hms.patient', 'Patient')
    appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment')


class Patient(models.Model):
    _inherit = 'banastech.hms.patient'

    m_age = fields.Char('Age')
    m_para_gravida = fields.Char('Para/Gravida')
    m_blood_type = fields.Selection([('A', 'A'),('B', 'B'),('AB', 'AB'),('O', 'O'), ], string='Blood Type')
    m_rh = fields.Selection([('+', '+'),('-', '-'), ], string='Rh')
    m_aml = fields.Char('AML')
    m_antenatal_care = fields.Char('Antenatal Care')
    m_usg = fields.Char('USG')
    m_vaccination_advice = fields.Char('Vaccination Advice')
    m_medical_i_d_p = fields.Selection([
        ('ht', 'HT'),
        ('diabetes', 'Diabetes'),
        ('thyroid', 'Thyroid'),
        ('fever', 'Fever'),
        ('blding', 'Blding'),
        ('pv', 'P/V'),
        ('thallasaemia', 'Thallasaemia')], string="Medical Illness During Preg")
    m_previous_gynaec_history = fields.Char('Previous Gynaec History')
    m_delievery_details = fields.Selection([
        ('prom', ' PROM'),
        ('blding', 'Blding'),
        ('forceps', 'Forceps'),
        ('vaccum', 'Vaccum')], string="Delivery Detail")
    ft_pt = fields.Char('FT/PT')
    nd_cs = fields.Char('ND/CS')
#     wt_kg = fields.Float('Wt. in Kg')
    tl = fields.Char('TL')
    hc = fields.Char('HC')
#     blood_group = fields.Selection([
#            ('A+', 'A+'),
#            ('A-', 'A-'),
#            ('B+', 'B+'),
#            ('B-', 'B-'),
#            ('AB+', 'AB+'),
#            ('AB-', 'AB-'),
#            ('O+', 'O+'),
#            ('O-', 'O-')], string='Blood Group')
    eyes = fields.Selection([('discharge', 'Discharge'), ('squint', 'Squint'), ('cataract', 'Cataract')], 'Eyes')
    born_color = fields.Selection([('jaundice', 'Jaundice'), ('cyanosis', 'Cyanosis'), ('pallor', 'Pallor')], 'Color')
    cong = fields.Char('Cong. Malformations')
    pulsation = fields.Char('Pulsation')
    vital_data = fields.Char('Vital Data')
    skin_eruption = fields.Char('Skin Eruption')
    systemic_examination = fields.Char('Systemic Examination')
    nnr = fields.Char('NNR')
    appointment_ids = fields.One2many('banastech.hms.appointment', 'pae_product_id', string='Appointment', domain="[('patient_id', '=', id)]")
    milestone_ids = fields.One2many('child.milestone','patient_id', string="Milestons")

    # @api.model
    # def default_get(self, fields):
    #     res = super(Patient, self).default_get(fields)
    #     vals = []
    #     milestone_templates = self.env['child.milestone.template'].search([])
    #     for line in milestone_templates:
    #         vals.append((0,0,{
    #             'name':line.name,
    #             'min_val': line.min_val,
    #             'max_val': line.max_val,
    #             'note': line.note,
    #         }))
    #     res.update({'milestone_ids': vals})
    #     return res


# class PrescLine(models.Model):
#     _inherit = 'prescription.line'
#     pae_appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment')
#     minimum = fields.Float(compute="_get_min_max", string='Minimum')
#     maximum = fields.Float(compute="_get_min_max", string='Maximum')
#     content_id = fields.Many2one('banas.hms.medicament.content', string='Content')
#     drug_co_id = fields.Many2one('drug.company', 'Company')

#     @api.multi
#     def _get_min_max(self):
#         for line in self:
#             if line.pae_appointment_id:
#                 line.minimum = line.pae_appointment_id.weight * line.content_id.minimum
#                 line.maximum = line.pae_appointment_id.weight * line.content_id.maximum

#     @api.onchange('content_id', 'drug_co_id')
#     def onchange_min_max(self):
#         if self.content_id:
#             products = self.product_id.search([('content_ids', '=', self.content_id.id)])
#             co_ids = [x.drug_company_id.id for x in products]
#             return {'domain': {'drug_co_id': [('id', 'in', co_ids)]}}


class PaediatricAppoin(models.Model):
    _inherit = 'banastech.hms.appointment'

    # @api.model    commented for getting error
    # def _get_pae_service_id(self):
        # return self.pae_product_id.search([('hospital_product_type', '=', "consultation_paediatric")], limit=1).id


#     @api.depends('patient_id')
#     @api.onchange('patient_id')
#     def onchange_patient_id(self):
#         if self.patient_id.vaccination_line:
#             vaccination_line = []
#             for line in self.patient_id.vaccination_line:
#                 vaccination_line.append((0,0,{
#                     'product_id':line.product_id,
#                     'date_check_due':line.date_check_due,
#                     'check':line.check,
#                     'given_date':line.given_date,
#                     'batch':line.given_date,

#                 }))
#             self.update({'vaccination_line': vaccination_line})
#         if self.patient_id.milestone_ids:
#             milestone_lines = []
#             for miles in self.patient_id.milestone_ids:
#                 milestone_lines.append((0,0,{
#                     'name':miles.name,
#                     'min_val': miles.min_val,
#                     'max_val': miles.max_val,
#                     'note': miles.note,
#                 }))
#             self.update({'milestone_ids': milestone_lines})
#         res = super(PaediatricAppoin, self).onchange_patient_id()
#         return res

#     pae_prescription_line = fields.One2many('prescription.line', 'pae_appointment_id','Prescription', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # head_cir = fields.Float('Head Circumference')
    # height = fields.Float('Height')
#     paediatric_chief_complain_ids = fields.One2many('hms.appointment.chief.complain', 'appointment_id', 'Chief Complain', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     newborn_ex_follow_ids = fields.One2many('hms.appointment.newborn.examinations.follow', 'appointment_id', 'Newborn Examinations')
#     #Newborn examination fields
#     milestone = fields.Html('Milestone')
#     ft_pt = fields.Char(related="patient_id.ft_pt")
#     nd_cs = fields.Char(related="patient_id.nd_cs")
#     tl = fields.Char(related="patient_id.tl")
#     hc = fields.Char(related="patient_id.hc")
#     eyes = fields.Selection(related="patient_id.eyes")
#     born_color = fields.Selection(related="patient_id.born_color")
#     cong = fields.Char(related="patient_id.cong")
#     pulsation = fields.Char(related="patient_id.pulsation")
#     vital_data = fields.Char(related="patient_id.vital_data")
#     skin_eruption = fields.Char(related="patient_id.skin_eruption")
#     systemic_examination = fields.Char(related="patient_id.systemic_examination")
#     nnr = fields.Char(related="patient_id.nnr")
#     #Mother related fields
#     m_age = fields.Char(related="patient_id.m_age")
#     m_para_gravida = fields.Char(related="patient_id.m_para_gravida")
#     m_blood_type = fields.Selection(related="patient_id.m_blood_type")
#     m_rh = fields.Selection(related="patient_id.m_rh")
#     m_aml = fields.Char(related="patient_id.m_aml")
#     m_antenatal_care = fields.Char(related="patient_id.m_antenatal_care")
#     m_usg = fields.Char(related="patient_id.m_usg")
#     m_vaccination_advice = fields.Char(related="patient_id.m_vaccination_advice")
#     m_medical_i_d_p = fields.Selection(related="patient_id.m_medical_i_d_p")
#     m_previous_gynaec_history = fields.Char(related="patient_id.m_previous_gynaec_history")
#     m_delievery_details = fields.Selection(related="patient_id.m_delievery_details")
    pae_product_id = fields.Many2one('product.product', ondelete='restrict', string='Consultation Service', help="Consultation Services", domain=[('hospital_product_type', '=', "consultation_paediatric")], states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}) # default=_get_pae_service_id,
#     pae_special_price = fields.Float('Special Charges', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     pae_reg_spe = fields.Selection([('reg', 'Regular'), ('spe', 'Special')], 'Regular or Special', default='reg', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     pae_foc = fields.Boolean('FOC', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     pae_follow_foc = fields.Boolean('Followup FOC', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     pae_special_day = fields.Boolean('Special Day', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     vaccination_group_id = fields.Many2one('vaccination.group',string='Vaccination Group')
#     vaccination_line = fields.One2many('vaccination.vaccination','appointment_id', string='Vaccination')
#     milestone_ids = fields.One2many('child.milestone','appointment_id', string="Milestons")


    # @api.multi
    # def appointment_done(self):
    #     super(PaediatricAppoin, self).appointment_done()
    #     if self.pae_prescription_line:
    #         order = self.env['prescription.order'].create({
    #                 'patient_id': self.patient_id.id,
    #                 'appointment': self.id,
    #                 'language': self.language,
    #                 'physician_id': self.physician_id.id,
    #                 'notes': self.others,
    #             })
    #         for prescription in self.pae_prescription_line:
    #             prescription.write({'prescription_id': order.id})
    #     if self.vaccination_line:
    #         vacc_lines = []
    #         for vacc in self.vaccination_line:
    #             vacc_lines.append((0,0,{
    #                 'patient_id':self.patient_id.id,
    #                 'product_id': vacc.product_id.id,
    #                 'date_check_due': vacc.date_check_due,
    #                 'check': vacc.check,
    #                 'given_date': vacc.given_date,
    #                 'batch':vacc.batch,
    #             }))
    #         self.patient_id.vaccination_line = vacc_lines
    #     if self.milestone_ids:
    #         milestone_lines = []
    #         for miles in self.milestone_ids:
    #             milestone_lines.append((0,0,{
    #                 'name':miles.name,
    #                 'min_val': miles.min_val,
    #                 'max_val': miles.max_val,
    #                 'note': miles.note,
    #             }))
    #         self.patient_id.milestone_ids = milestone_lines              
    #     return self.action_list_appointment()

    # @api.onchange('pae_product_id','pae_reg_spe','pae_special_day','pae_foc','pae_follow_foc')
    # def onchange_pae_reg_spe_product_id(self):
    #     if self.pae_reg_spe:
    #         self.pae_special_price = self.pae_product_id.lst_price
    #     if self.pae_special_day:
    #         self.pae_special_price-= self.pae_product_id.special_day_price
    #         if self.pae_foc:
    #             self.pae_special_price = 0.0
    #     if self.pae_follow_foc:
    #         self.pae_special_price = self.pae_product_id.lst_price / 2
    #         if self.pae_special_day:
    #             self.pae_special_price = self.pae_product_id.lst_price - self.pae_product_id.special_day_price
    #         if self.pae_foc:
    #             self.pae_special_price = 0.0
    #     if self.pae_foc:
    #         self.pae_special_price = 0.0

    # @api.multi
    # def create_padetric_invoice(self):
    #     inv_obj = self.env['account.invoice']
    #     ir_property_obj = self.env['ir.property']
    #     inv_line_obj = self.env['account.invoice.line']
    #     product_id = self.pae_product_id
    #     #price = product_id.lst_price
    #     account_id = False
    #     price = self.pae_special_price
    #     if product_id.id:
    #         account_id = product_id.property_account_income_id.id
    #     if not account_id:
    #         prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
    #         account_id = prop and prop.id or False
    #     invoice = inv_obj.create({
    #         'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
    #         'partner_id': self.patient_id.partner_id.id,
    #         'patient_id': self.patient_id.id,
    #         'type': 'out_invoice',
    #         'name': '-',
    #         'origin': self.name,
    #         'report_type':'consult',
    #         'appointment_id': self.id,
    #         'consultant_doctor_id':self.patient_id.primary_doctor.id,
    #         'treating_doctor_id':self.patient_id.primary_doctor.id,
    #         'currency_id': self.env.user.company_id.currency_id.id,
    #         'invoice_line_ids': [(0, 0, {
    #             'name': product_id.name,
    #             'price_unit': price,
    #             'account_id': account_id,
    #             'quantity': 1.0,
    #             'discount': 0.0,
    #             'uom_id': product_id.uom_id.id,
    #             'product_id': product_id.id,
    #             'account_analytic_id': False,
    #         })],
    #     })
    #     self.invoice_id = invoice.id


    # @api.onchange('vaccination_group_id')
    # def onchange_vaccination_group_id(self):
    #     if not self._context.has_key('padetric'):
    #         product_lines = []
    #         if self.patient_id.dob:
    #             dob = fields.Date.from_string(self.patient_id.dob)
    #             for line in self.vaccination_group_id.group_line:
    #                 days = line.product_id.date_due_day
    #                 product_lines.append((0,0,{
    #                     'product_id': line.product_id.id, 
    #                     'date_check_due': (dob+ td(days=days))
    #                 }))
    #         else:
    #             for line in self.vaccination_group_id.group_line:
    #                 product_lines.append((0,0,{
    #                     'product_id': line.product_id.id,
    #                 }))
    #         self.vaccination_line = product_lines


# class Vaccination(models.Model):
#     _inherit = 'vaccination.vaccination'

#     appointment_id = fields.Many2one('banastech.hms.appointment','Appointment', help="Patient for vaccination")