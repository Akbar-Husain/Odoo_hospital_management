import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
# from odoo.addons.website.models.website import slug
import dateutil.relativedelta
import random
# from exceptions import Warning
import odoo.addons.decimal_precision as dp

class PrescriptionGroupLine(models.Model):
    _name = 'banastech.hms.prescription.group.line'

    medicament_group_id = fields.Many2one('medicament.group', 'Group Name')
    group_id = fields.Many2one('banastech.hms.prescription.group', 'Group Id')


class PrescriptionGroup(models.Model):
    _name = 'banastech.hms.prescription.group'

    @api.model
    def _merge_name_prescription(self):
        score_details = []
        for data in self.group_line:
            if data.medicament_group_id:
                score_details.append(data.medicament_group_id.name)
        score_details = ','.join(score_details)
        self.display_name = score_details

    name = fields.Char(string='Group Name', required=True)
    diagnosis_id = fields.Many2one('banas.hms.diseases', 'Diagnosis')
    group_line = fields.One2many('banastech.hms.prescription.group.line', 'group_id', string='Medicament line')
    display_name = fields.Char(compute=_merge_name_prescription, string='Display')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain =[]
        if 'diagnosis_id' in self._context and self._context.get('diagnosis_id',False):
            diagnosis = self.env['banas.hms.diseases'].search([('id','in',self._context.get('diagnosis_id',False)[0][2])])
            domain += [('diagnosis_id','in',diagnosis.ids)]
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()

class RadiologyLine(models.Model):
    _inherit = 'hms.investigation.radiology.line'

    plate = fields.Selection([('8x10', '08 x 10'), ('14x11', '14 x 11'), ('paper', 'Paper'), ('other', 'Other')], default="8x10")
    side = fields.Selection([('none', 'None'), ('right', 'Right'), ('left', 'Left'), ('both', 'Both')], default="none")
    appointment_id = fields.Many2one('hms.appointment', 'Appointment')
    foc = fields.Boolean('FOC')

#     @api.onchange('product_id','foc')
#     def onchange_product(self):
#         super(RadiologyLine, self).onchange_product()
#         if self.product_id:
#             price = self.product_id.lst_price
#             # if self.appointment_id.wednesday:
#             #     price -= self.product_id.special_day_price
#             #     self.plate = '8x10'
#             if self.appointment_id.reg_spe == 'spe':
#                 price -= self.product_id.reg_spe_price
#             if self.foc:
#                 price = 0.0
#             self.price = price


class ProvisionalInvestigation(models.Model):
    _name = 'provisional.investigation'

    appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment')
    past_inv_datetime = fields.Date(string="Date")
    product_id = fields.Many2one('product.product',string="Test")
    result = fields.Char('Outcome')

class PathologyLine(models.Model):
    _inherit = 'hms.investigation.pathology.line'

    appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment')

class ManometryLine(models.Model):
    _inherit = 'hms.investigation.manometry.line'

    appointment_id = fields.Many2one('hms.appointment', 'Appointment')


class EndoscopyLine(models.Model):
    _inherit = 'hms.investigation.endoscopy.line'

    appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment')

class OtherServicesLine(models.Model):
    _inherit = 'hms.investigation.other_services.line'

    appointment_id = fields.Many2one('hms.appointment', 'Appointment')

class HMSPatient(models.Model):
    _inherit = "banastech.hms.patient"

    # first_name = fields.Char(string='First Name', required=True, select=True)
    # middel_name = fields.Char(string='Middle Name')
    # last_name = fields.Char(string='Last Name')
    # hypersensitive = fields.Char('Hypersensitive to')
    followup_validity = fields.Date(string='Followup date validity')
    # opd_foc = fields.Boolean(string='OPD FOC')
    # bmi_ids = fields.One2many('banastech.hms.patient.bmi','patient_id',string="BMI Details")


# ##############CODE FOR AUTO CAPS LETTER##############

    # @api.depends('first_name')
    # @api.onchange('first_name')
    # def onchange_case_first(self):#  cr, uid, ids, first_name
    #     if self.first_name:
    #         result_first = {'value': {
    #             'first_name': str(first_name).upper()
    #             }
    #         }
    #         return result_first

    # @api.depends('middel_name')
    # @api.onchange('middel_name')
    # def onchange_case_middle(self):# , cr, uid, ids, middel_name
    #     if self.middel_name:
    #         result_middle = {'value': {
    #             'middel_name': str(middel_name).upper()
    #             }
    #         }
    #         return result_middle

    # @api.depends('last_name')
    # @api.onchange('last_name')
    # def onchange_case_last(self):#, cr, uid, ids, last_name
    #     if self.last_name:
    #         result_last = {'value': {
    #             'last_name': str(last_name).upper()
    #             }
    #         }
    #         return result_last

#     @api.depends('street')
#     @api.onchange('street')
#     def onchange_case_street(self, cr, uid, ids, street):
#         if street:
#             result_street = {'value': {
#                 'street': str(street).upper()
#                 }
#             }
#             return result_street

#     @api.depends('street2')
#     @api.onchange('street2')
#     def onchange_case_street2(self, cr, uid, ids, street2):
#         if street2:
#             result_street2 = {'value': {
#                 'street2': str(street2).upper()
#                 }
#             }
#             return result_street2 

#     # @api.depends('area_id')
#     # @api.onchange('area_id')
#     # def onchange_case_area_id(self, cr, uid, ids, area_id):
#     #     if area_id:
#     #         result_area_id = {'value': {
#     #             'area_id': str(area_id).upper()
#     #             }
#     #         }
#     #         return result_area_id

#     # @api.depends('city_id')
#     # @api.onchange('city_id')
#     # def onchange_case_city_id(self, cr, uid, ids, city_id):
#     #     if city_id:
#     #         result_city_id = {'value': {
#     #             'city_id': str(city_id).upper()
#     #             }
#     #         }
#     #         return result_city_id

#     # @api.depends('state_id')
#     # @api.onchange('state_id')
#     # def onchange_case_state_id(self, cr, uid, ids, state_id):
#     #     if state_id:
#     #         result_state_id = {'value': {
#     #             'state_id': str(state_id).upper()
#     #             }
#     #         }
#     #         return result_state_id 


# #########################################
#     @api.multi
#     def write(self, values):
#         if values.get('first_name', ''):
#             values['first_name'] = str(values.get('first_name').title())
#         if values.get('middel_name', ''):
#             values['middel_name'] = str(values.get('middel_name').title())
#         if values.get('last_name', ''):
#             values['last_name'] = str(values.get('last_name').title())
#         # if values.get('bmi') or values.get('cm'):
#         #     bmi = self.env['patient.bmi'].create({'bmi': self.bmi, 'patient_id':self.id})
#         res = super(Patient, self).write(values)
#         self.partner_id.write({'name': (self.first_name.title() if self.first_name else '')+' '+ (self.middel_name.title() if self.middel_name else '')+' '+(self.last_name.title() if self.last_name else '')})
#         return res

#     @api.model
#     def create(self, values):
#         name = values.get('first_name', '')
#         values['first_name'] = str(values.get('first_name').title())
#         if values.get('middel_name', ''):
#             name += ' ' + values.get('middel_name', '')
#             values['middel_name'] = str(values.get('middel_name').title())
#         if values.get('last_name', ''):
#             name += ' ' + values.get('last_name', '')
#             values['last_name'] = str(values.get('last_name').title())
#         values['name'] = name
#         return super(Patient, self).create(values)

# class DocumentManagement(models.Model):
#     _inherit = "document.management"
#     appointment = fields.Many2one('hms.appointment', string = 'Appointment Documents')

class Appointment(models.Model):
    _inherit = 'banastech.hms.appointment'

    @api.model
    def _get_appointment_total(self):
        for app in self:
            visit_count = 0
            if app.patient_id:
                appointment = self.search([('patient_id', '=', app.patient_id.id)])
                visit_count = len(appointment)
                if app.patient_id.visits:
                    visit_count += app.patient_id.visits
            app.visit_count = visit_count

#     def _get_years_sex(self):
#         for app in self:
#             if app.patient_id.dob:
#                 b_date = datetime.strptime(app.patient_id.dob, '%Y-%m-%d')
#                 delta = relativedelta(datetime.now(), b_date)
#                 age = _("%s year") % (delta.years)
#                 app.years_sex = age

    @api.depends('waiting_ids')
    def _get_wait_list(self):
        for app in self:
            app.waiting_ids = self.search([('doctor_id','=',self.doctor_id.id),('state', '=', 'waiting'), ('patient_id', '!=', app.patient_id.id), ('date', '>=', fields.Date.today()),('date', '<', (datetime.today() + relativedelta(days=1)).strftime('%Y-%m-%d'))])

# #Block Counting Function As it is not required in Generic Code Feb 13
#     # def _counting_tab(self):
#     #     for app in self:
#     #         history = "<table class='table table-condensed'>"
#     #         sql = self.env.cr.execute("select count(*) from hms_appointment where department_name ='Orthopedic' and state='in_consultation' and date >= CURRENT_DATE and date < CURRENT_DATE + interval '1 day' LIMIT 5")
#     #         active = self.env.cr.fetchone()[0]
#     #         sql = self.env.cr.execute("select count(*) from hms_appointment where department_name ='Orthopedic'  and state not in('done','draft','confirm') and date >= CURRENT_DATE and date < CURRENT_DATE + interval '1 day' LIMIT 1000")
#     #         not_done = self.env.cr.fetchone()[0]
#     #         sql = self.env.cr.execute("select count(*) from hms_appointment where department_name ='Orthopedic'  and state='waiting' and date >= CURRENT_DATE and date < CURRENT_DATE + interval '1 day' LIMIT 1000")
#     #         waiting = self.env.cr.fetchone()[0]
#     #         sql = self.env.cr.execute("select count(*) from hms_appointment where department_name ='Orthopedic' and state not in('draft','confirm') and date >= CURRENT_DATE and date < CURRENT_DATE + interval '1 day' LIMIT 1000")
#     #         total = self.env.cr.fetchone()[0]
#     #         history += _("<span><b>Active: %s</b></span>, <span><b>Not Done: %s</b></span>, <span><b>Waiting: %s</b></span>, <span><b>Total: %s</b></span>")%(active,not_done,waiting,total)
#     #         history += _("</table>")
#     #         app.counting_tab = history

#     # def _patient_list(self):
#     #     for app in self:
#     #         app.active_patient = len(self.search([('state', '=', 'in_consultation'),('department_name','=',app.department_name),  ('date', '>=', fields.Date.today()),('date', '<', (datetime.today() + relativedelta(days=1)).strftime('%Y-%m-%d'))]))
#     #         app.not_done_patient = len(self.search([('state', '!=', 'done'),('department_name','=',app.department_name), ('date', '>=', fields.Date.today()),('date', '<', (datetime.today() + relativedelta(days=1)).strftime('%Y-%m-%d'))]))
#     #         app.waiting_patient = len(self.search([('state', '=', 'waiting'),('department_name','=',app.department_name),  ('date', '>=', fields.Date.today()),('date', '<', (datetime.today() + relativedelta(days=1)).strftime('%Y-%m-%d'))]))
#     #         app.done_patient = len(self.search([('department_name','=',app.department_name), ('date', '>=', fields.Date.today()),('date', '<', (datetime.today() + relativedelta(days=1)).strftime('%Y-%m-%d'))]))

#     def _get_investigation_list(self):
#         for apointment in self:
#             domain = [('patient_id', '=', apointment.patient_id.id)]
#             if apointment.state != 'done':
#                 domain += '|',('appointment_id', '!=', apointment.id),('appointment_id', '=', False)
#             apointment.investigation_ids = self.env['hms.investigation'].search(domain)

    # def _get_history(self):
    #     for app in self:
    #         if app.patient_id:
    #             history = "<table class='table table-condensed'>"
    #             for appointment in self.env['prescription.order'].search([('patient_id', '=', app.patient_id.id)],order='creation_date desc'):
    #                 if appointment.appointment.date:
    #                     history += _("<tr><td><b>Date:</b></td><td>%s</td></tr>")%(datetime.strftime(datetime.strptime(appointment.appointment.date,'%Y-%m-%d %H:%M:%S') + timedelta(hours=5, minutes=30),"%d-%m-%Y %H:%M"))
    #                 diagnosis_name = ''
    #                 for diagnosis in appointment.appointment.diagnosis_id:
    #                     diagnosis_name+= diagnosis.name + ', '
    #                 history += _("<tr><td><b>Diagnosis:</b></td><td>%s</td></tr>")%(diagnosis_name)
    #                 history += _("<tr><td><b>Secondary Diagnosis:</b></td><td>%s</td></tr>")%(appointment.appointment.second_diagonsiss)
    #                 history += _("<tr><td><b>Medicine:</b></td>")
    #                 history += _("<td><table class='table table-condensed'><thead><th>Name</th><th>Frequency</th><th>Days</th><th>Qty</th></thead>")
    #                 for line in appointment.prescription_line:
    #                     history += _("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>")%(line.product_id.name, line.common_dosage.abbreviation, line.days, line.quantity)
    #                 history += _("</table></td></tr>")
#                     history += _("<tr><td style='border-bottom: 1px solid black'><b>Chief Complain:</b></td><td style='border-bottom: 1px solid black'>%s</td></tr>")%(appointment.appointment.chief_complain or '')
#                 presc_line = self.env['prescription.line'].search([('temp_patient_id', '=', app.patient_id.id)])
#                 dict = {}
#                 for presc_line in self.env['prescription.line'].search([('temp_patient_id', '=', app.patient_id.id)]):
#                     if dict.has_key(presc_line.start_treatment):
#                         dict[presc_line.start_treatment].append(presc_line.id)
#                     else:
#                         dict.update({presc_line.start_treatment:[presc_line.id]})
#                 for rec,value in dict.iteritems():
#                     history += _("<tr><td><b>Date:</b></td><td>%s</td></tr>")%(datetime.strftime(datetime.strptime(rec,'%Y-%m-%d  %H:%M:%S') + timedelta(hours=5, minutes=30),"%d-%m-%Y %H:%M"))
#                     history += _("<tr><td><b>Medicine:</b></td>")
#                     history += _("<td><table class='table table-condensed'><thead><th>Name</th><th>Frequency</th><th>Days</th><th>Qty</th></thead>")
#                     for presc in self.env['prescription.line'].browse(value):
#                         history += _("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>")%(presc.product_id.name, presc.common_dosage.abbreviation, presc.days, presc.quantity)
#                     history += _("</table></td></tr>")
# #                         history += _("<tr><td style='border-bottom: 1px solid black'><b>Findings:</b></td><td style='border-bottom: 1px solid black'>%s</td></tr>")%(appointment.appointment.notes or '')
#                app.past_history = history

    @api.model
    def get_payment_status(self):
        for appointment in self:
#             #code block for Physiotheraphy For generic
#             # Getting status for radiology investigation invoice
            for radiology in appointment.radiology_line:
                if radiology.investigation_id.amount_total == 0.0 or not radiology.investigation_id.invoice_id:
                    appointment.x_ray = '•'
                elif radiology.investigation_id.invoice_id.state == 'paid':
                    domain = [('account_id', '=', radiology.investigation_id.invoice_id.account_id.id), ('partner_id', '=', self.env['res.partner']._find_accounting_partner(radiology.investigation_id.invoice_id.partner_id).id), ('reconciled', '=', False), ('amount_residual', '!=', 0.0)]
                    domain.extend([('credit', '>', 0), ('debit', '=', 0), ('id', 'in', radiology.investigation_id.invoice_id.payment_move_line_ids.ids)])
                    lines = self.env['account.move.line'].search(domain)
                    amount_to_show = 0
                    for line in lines:
                        amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(abs(line.amount_residual), radiology.investigation_id.invoice_id.currency_id)
                    if amount_to_show == 0:
                        appointment.x_ray = '✓'
                    elif amount_to_show > 0:
                        appointment.x_ray = '+'
                # elif radiology.investigation_id.invoice_id.state != 'paid':
                #     if radiology.investigation_id.invoice_id.residual < radiology.investigation_id.invoice_id.amount_total and radiology.investigation_id.invoice_id.residual != 0:
                #         appointment.x_ray = '−'
                #     else:
                #         appointment.x_ray = '✕'
                else:
                    appointment.x_ray = '•'
            if not appointment.radiology_line:
                appointment.x_ray = 'No'

            # appointment.x_ray = "No"

#             #Pathology_Fee
            for pathology in appointment.pathology_line:
                if pathology.investigation_id.amount_total == 0.0 or not pathology.investigation_id.invoice_id:
                    appointment.payment_pathology = '•'
                elif pathology.investigation_id.invoice_id.state == 'paid':
                    domain = [('account_id', '=', pathology.investigation_id.invoice_id.account_id.id), ('partner_id', '=', \
                        self.env['res.partner']._find_accounting_partner(pathology.investigation_id.invoice_id.partner_id).id), \
                        ('reconciled', '=', False), ('amount_residual', '!=', 0.0)]
                    domain.extend([('credit', '>', 0), ('debit', '=', 0), ('id', 'in', pathology.investigation_id.invoice_id.payment_move_line_ids.ids)])
                    lines = self.env['account.move.line'].search(domain)
                    amount_to_show = 0
                    for line in lines:
                        amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(abs(line.amount_residual), pathology.investigation_id.invoice_id.currency_id)
                    if amount_to_show == 0:
                        appointment.payment_pathology = '✓'
                    elif amount_to_show > 0:
                        appointment.payment_pathology = '+'
                # elif pathology.investigation_id.invoice_id.state != 'paid':
                #     if pathology.investigation_id.invoice_id.residual < pathology.investigation_id.invoice_id.amount_total and pathology.investigation_id.invoice_id.residual != 0:
                #         appointment.payment_pathology = '−'
                #     else:
                #         appointment.payment_pathology = '✕'
                else:
                    appointment.payment_pathology = '•'
            if not appointment.pathology_line:
                appointment.payment_pathology = 'No'

#             #Manometry_Fee
            for manometry in appointment.manometry_line:
                if manometry.investigation_id.amount_total == 0.0 or not manometry.investigation_id.invoice_id:
                    appointment.payment_manometry = '•'
                elif manometry.investigation_id.invoice_id.state == 'paid':
                    domain = [('account_id', '=', manometry.investigation_id.invoice_id.account_id.id), ('partner_id', '=', \
                        self.env['res.partner']._find_accounting_partner(manometry.investigation_id.invoice_id.partner_id).id), \
                        ('reconciled', '=', False), ('amount_residual', '!=', 0.0)]
                    domain.extend([('credit', '>', 0), ('debit', '=', 0), ('id', 'in', manometry.investigation_id.invoice_id.payment_move_line_ids.ids)])
                    lines = self.env['account.move.line'].search(domain)
                    amount_to_show = 0
                    for line in lines:
                        amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(abs(line.amount_residual), manometry.investigation_id.invoice_id.currency_id)
                    if amount_to_show == 0:
                        appointment.payment_manometry = '✓'
                    elif amount_to_show > 0:
                        appointment.payment_manometry = '+'
                # elif manometry.investigation_id.invoice_id.state != 'paid':
                #     if manometry.investigation_id.invoice_id.residual < manometry.investigation_id.invoice_id.amount_total and manometry.investigation_id.invoice_id.residual != 0:
                #         appointment.payment_manometry = '−'
                #     else:
                #         appointment.payment_manometry = '✕'
                else:
                    appointment.payment_manometry = '•'
            if not appointment.manometry_line:
                appointment.payment_manometry = 'No'

#             #Endoscopy_Fee
            for endoscopy in appointment.endoscopy_line:
                if endoscopy.investigation_id.amount_total == 0.0 or not endoscopy.investigation_id.invoice_id:
                    appointment.payment_endoscopy = '•'
                elif endoscopy.investigation_id.invoice_id.state == 'paid':
                    domain = [('account_id', '=', endoscopy.investigation_id.invoice_id.account_id.id), ('partner_id', '=', \
                        self.env['res.partner']._find_accounting_partner(endoscopy.investigation_id.invoice_id.partner_id).id), \
                        ('reconciled', '=', False), ('amount_residual', '!=', 0.0)]
                    domain.extend([('credit', '>', 0), ('debit', '=', 0), ('id', 'in', endoscopy.investigation_id.invoice_id.payment_move_line_ids.ids)])
                    lines = self.env['account.move.line'].search(domain)
                    amount_to_show = 0
                    for line in lines:
                        amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(abs(line.amount_residual), endoscopy.investigation_id.invoice_id.currency_id)
                    if amount_to_show == 0:
                        appointment.payment_endoscopy = '✓'
                    elif amount_to_show > 0:
                        appointment.payment_endoscopy = '+'
                # elif endoscopy.investigation_id.invoice_id.state != 'paid':
                #     if endoscopy.investigation_id.invoice_id.residual < endoscopy.investigation_id.invoice_id.amount_total and endoscopy.investigation_id.invoice_id.residual != 0:
                #         appointment.payment_endoscopy = '−'
                #     else:
                #         appointment.payment_endoscopy = '✕'
                else:
                    appointment.payment_endoscopy = '•'
            if not appointment.endoscopy_line:
                appointment.payment_endoscopy = 'No'

#             # Getting status for appointment invoice
            if not appointment.invoice_id:
                appointment.opd_fee = 'No'
            elif appointment.invoice_id.state == 'paid':
                domain = [('account_id', '=', appointment.invoice_id.account_id.id), ('partner_id', '=', self.env['res.partner']._find_accounting_partner(appointment.invoice_id.partner_id).id), ('reconciled', '=', False), ('amount_residual', '!=', 0.0)]
                domain.extend([('credit', '>', 0), ('debit', '=', 0), ('id', 'in', appointment.invoice_id.payment_move_line_ids.ids)])
                lines = self.env['account.move.line'].search(domain)
                amount_to_show = 0
                for line in lines:
                    amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(abs(line.amount_residual), appointment.invoice_id.currency_id)
                if amount_to_show == 0:
                    appointment.opd_fee = '✓'
                elif amount_to_show > 0:
                    appointment.opd_fee = '+'
            # elif appointment.invoice_id.state != 'paid':
            #     if appointment.invoice_id.residual < appointment.invoice_id.amount_total and appointment.invoice_id.residual != 0:
            #         appointment.opd_fee = '−'
            #     else:
            #         appointment.opd_fee = '✕'

        appointment.opd_fee = "No"

#     @api.model
#     def get_investigation(self):
#         res = ''
#         for line in self.radiology_line:
#             # print "====================",line.product_id
#             res+=line.product_id.name + ','
#         for line in self.pathology_line:
#             # print "====================",line.product_id
#             res+=line.product_id.name + ','
#         for line in self.endoscopy_line:
#             # print "====================",line.product_id
#             res+=line.product_id.name + ','
#         for line in self.manometry_line:
#             # print "====================",line.product_id
#             res+=line.product_id.name
#             # print "=============res==============",res
#             return res

#     @api.model
#     def get_due_payments(self):
#         for appointment in self:
#             domain = [
#                 ('patient_id', '=', appointment.patient_id.id)
#             ]
#             total_payment_due = 0
#             for appoint in appointment.search(domain):
#                 if appoint.invoice_id:
#                     total_payment_due += appoint.invoice_id.residual
#             appointment.amount_due = total_payment_due

#     @api.model
#     def __compute_time(self):
#         for rec in self:
#             rec.to_count = fields.Date.from_string(rec.date) - fields.Date.from_string(rec.date_start)

# #     @api.multi
# #     def _compute_ranking(self):
# #         AppNormal = self.search([('state','=','waiting'),('date_start','>=', (datetime.now().strftime('%Y-%m-%d 00:00:00')))],order='date_start,booked_online desc')
# #         rank = 1
# #         for rec in AppNormal:
# #             app_date = (datetime.strptime(rec.date, DEFAULT_SERVER_DATETIME_FORMAT)  + timedelta(minutes=10)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
# #             if rec.booked_online == True and rec.date_start <= app_date:
# #                 rec.ranking = rank
# #                 rec.ranking_order = rank
# #                 rank += 1
# #             else:
# #                 rec.ranking = rank 
# #                 rec.ranking_order = rank
# #                 rank += 1 

#     # @api.multi
#     # def _note_history(self):
#     #     words = []
#     #     notes_search = self.search([('patient_id', '=', app.patient_id.id)])
#     #     for notes in notes_search:
#     #         words.append(notes)
#     #     return ' '.join(words)

#     @api.depends('radiology_line.price','pathology_line.price','endoscopy_line.price','manometry_line.price')
#     def _amount_all(self):
#         """
#         Compute the total amounts of the price.
#         """
#         for order in self:
#             amount = 0.0
#             amount_pathology = 0.0
#             amount_manometry = 0.0
#             amount_endoscopy = 0.0

#             for line in order.radiology_line:
#                 amount += line.price
#             for line in order.pathology_line:
#                 amount_pathology += line.price
#             for line in order.manometry_line:
#                 amount_manometry += line.price
#             for line in order.endoscopy_line:
#                 amount_endoscopy += line.price

#             order.update({
#                 'xray_price_receptionist': amount,
#                 'amount_pathology': amount_pathology,
#                 'amount_manometry': amount_manometry,
#                 'amount_endoscopy' : amount_endoscopy
#             })

#     #date_radiology = fields.Datetime('Date', default=fields.Datetime.now, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    radilogy_date = fields.Date('Date', default=fields.Datetime.now, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     echo_prescription = fields.Boolean('Eco. Presc.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    pregnancy_warning = fields.Boolean('Pregnancy Warning', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    group_id = fields.Many2one('banastech.hms.prescription.group',string='Group', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    prescription_line = fields.One2many('prescription.line', 'appointment_id','Prescription', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     prescription_line_price = fields.One2many('prescription.line.price', 'appointment_id','Prescription Line', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    lab_group_id = fields.Many2one('hms.investigation.group', 'Laboratory Test Group', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     advice_group_ids = fields.Many2many('appointment.advice.group','appointment_advice_rel','groups_id','appointment_id',string="Advice Group",ondelete='cascade')
#     advices_group_lines_ids = fields.One2many('advices.group.lines','appointment_id', string='Advice Line', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, ondelete='cascade')
    radiology_line = fields.One2many('hms.investigation.radiology.line', 'appointment_id', string='Radiology Line', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    pathology_line = fields.One2many('hms.investigation.pathology.line', 'appointment_id', string='Lab Test Line', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    manometry_line = fields.One2many('hms.investigation.manometry.line', 'appointment_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    endoscopy_line = fields.One2many('hms.investigation.endoscopy.line', 'appointment_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    other_services_line = fields.One2many('hms.investigation.other_services.line', 'appointment_id', string="Other Services")
    suggestive_investigations = fields.Text('Special Investigation')
    suggestive_investigation_ipd = fields.Text('Suggestive Investigation')
#     # inv_username = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)
    provisional_inv = fields.One2many('provisional.investigation', 'appointment_id', string='Radiology Line', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
# #     inv_images = fields.Binary('Images')
#     inv_images = fields.One2many('document.management','appointment', string = 'Records', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    session1_image_ids = fields.One2many('session1.image', 'appointment_id', string='Images')
#     foc = fields.Boolean('FOC', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     #wednesday = fields.Boolean('Wednesday', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    opd_foc = fields.Boolean('FOC', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    follow_foc = fields.Boolean('Followup FOC', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    special_day = fields.Boolean('Special Day', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     reg_spe = fields.Selection([('reg', 'Regular'), ('spe', 'Special')], 'Regular or Special', default='reg', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    opd_reg_spe = fields.Selection([('reg', 'Regular'), ('spe', 'Special')], 'Regular or Special', default='reg', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    visit_count = fields.Integer(compute="_get_appointment_total", string="Visit",readonly="True")
#     street = fields.Char(related='patient_id.street', string="Area")
#     street2 = fields.Char(related='patient_id.street2', string="Landmark")
#     city = fields.Char(related="patient_id.city", string="City")
#     zip = fields.Char(related="patient_id.zip", string="Pincode")
    gender = fields.Selection(related="patient_id.gender", string="Gender")
    age = fields.Char(related="patient_id.age", string='Age')
#     first_name = fields.Char(related="patient_id.first_name", string='First Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     middel_name = fields.Char(related="patient_id.middel_name", string='Middle Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     last_name = fields.Char(related="patient_id.last_name", string='Last Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    speciality = fields.Many2one(related="doctor_id.speciality", ondelete='set null', string='Speciality', help='Specialty Code')
#     suggestive_investigation = fields.Text(string="Suggestive Investigation")
# #     street = fields.Char(string="Area")
# #     street2 = fields.Char(string="Landmark")
# #     city = fields.Char(string="City")
# #     zip = fields.Char(string="Pincode")
# #     sex = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Sex')
# #     age = fields.Char(string='Age')
# #     first_name = fields.Char(string='First Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
# #     middel_name = fields.Char(string='Middle Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
# #     last_name = fields.Char(string='Last Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})

    waiting_ids = fields.One2many('banastech.hms.appointment', compute="_get_wait_list", string="Waiting")
#     finding_ids = fields.One2many('opd.finding', 'appointment_id', string="Findings", states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    hypersensitive = fields.Char('Hypersensitive to', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
# #     diagnosis_id = fields.Many2one('hms.diseases', 'Diagnosis', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    diagnosis_id = fields.Many2many('banas.hms.diseases', 'rel_diagnosis_app', 'diagnosis_id','appointment_id' , string='Diagnosis', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # past_history = fields.Html(compute='_get_history', string='History')
#     report_2d = fields.Boolean('2D Echo', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     report_ecg = fields.Boolean('E.C.G', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     report_ppt = fields.Boolean('P.F.T', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     # lng_hindi = fields.Boolean(related="patient_id.lng_hindi", string='Hindi', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     # lng_guj = fields.Boolean(related="patient_id.lng_guj", string='Guj.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     # lng_english = fields.Boolean(related="patient_id.lng_english", string='English', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    language = fields.Selection(related="patient_id.language", String="Language")
# #     language = fields.Selection([('hindi', 'Hindi'),('english', 'English'),('gujarati', 'Gujarati')], String="Language")
    lactation = fields.Boolean('Lactation', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    ref_doctor = fields.Many2many(related="patient_id.ref_doctor", string='Referred By')
#     #ref_doctor = fields.Many2many('referring.doctors','rel_doc_pat','doc_id','patient_id', 'Referred By', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    cabin_no = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')], string='Cabin', states={'cancel': [('readonly', True)], 'done': [('readonly', True)],}, required=True, default="1")
# #     physician_id = fields.Many2one('res.users',string='Doctor')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('waiting', 'Waiting'),
        ('in_consultation', 'Active'),
        ('dressing', 'Dressing'),
        ('to_x', 'To Investigation'),
        ('f_x', 'From Investigation'),
        ('sr_dr', 'Sr. Dr.'),
        #('invoiced', 'Invoiced'),
        ('invoice_exempt', 'Invoice Exempt'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='State', default='draft', required=True)
#     prev_state = fields.Selection([
#         ('waiting', 'Waiting'),
#         ('to_x', 'To Investigation'),
#         ('f_x', 'From Investigation'),
#         ('sr_dr', 'Sr. Dr.'),
#         ('dressing', 'Dressing'),
#         ('done', 'Done'),], default='done',string='State')
    opd_fee = fields.Char(compute='get_payment_status', string='OPD', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    x_ray = fields.Char(compute='get_payment_status', string='Radiology', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     opd_phy = fields.Char(compute='get_payment_status', string='Phy.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    payment_pathology = fields.Char(compute='get_payment_status', string='Path.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     amount_pathology  = fields.Float(string = 'Path Charges', store = True, readonly = True, compute = '_amount_all', track_visibility = 'always')
    payment_manometry = fields.Char(compute='get_payment_status', string='Mano.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     amount_manometry  = fields.Float(string = 'Manometry Charges', store = True, readonly = True, compute = '_amount_all', track_visibility = 'always')
    payment_endoscopy = fields.Char(compute='get_payment_status', string='Endo.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     amount_endoscopy  = fields.Float(string = 'Endoscopy Charges', store = True, readonly = True, compute = '_amount_all', track_visibility = 'always')
#     cabin = fields.Selection([('zero', ''), ('one', '1'),
#         ('two', '2'),
#         ('three', '3'),
#         ('four', '4'),('five', '5'),('six', '6'),
#     ], string='', copy=False)
# #Below fields transter to the HMS
# #    complain_ids = fields.Many2many('chief.complain','appointment_rel_complain','appointment_id','complain_ids' , string='Chief Complain')
#     chief_complain_ids = fields.One2many('hms.appointment.chief.complain', 'appointment_id', 'Chief Complain', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    special_price = fields.Float('Special Charges', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     investigation_ids = fields.One2many('hms.investigation', compute="_get_investigation_list", string="Investigations", states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
# #     radiology_wizard_line = fields.One2many('investigation.radiology.wizard', 'appointment_id' , string='Lab Test', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
# #     pathology_wizard_line = fields.One2many('investigation.pathology.wizard', 'appointment_id' , string='Lab Test', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     amount_due = fields.Float(compute='get_due_payments', string='Amount Due', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
# #     prescription_wizard_line = fields.One2many('prescription.wizard', 'appointment_id' , string='Prescription Wizard', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}) 
# #     department_name = fields.Char(related='department_id.name', string='Department Name',store=True)
    department_name = fields.Char(string='Department Name')
    prescription_total = fields.Float(string='Prescription Amount',readonly=False)
#     to_count = fields.Integer(string="Counting", compute="_compute_time")
# #     ranking = fields.Integer(string="Ranking", compute="_compute_ranking")
# #     ranking_order = fields.Integer(string="Ranking", default=80)
    bill_to_hospital = fields.Boolean('Bill to Hospital',default=True)
#     #notes = fields.Text(string='Notes', compute="_note_history")
    p_occupation = fields.Many2one(string="Occupation",related='patient_id.occupation')
#     # p_clinical_research = fields.Boolean(string="CRL",related='patient_id.clinical_research')
    case_type = fields.Selection([
        ('normal', 'Regular'),
        ('day', 'Day Emergency'),
        ('night', 'Night Emergency'),
        ('file', 'File opinion')],
        #('camp','Camp')],
         default='normal', string='Case Type')
    dressing = fields.Boolean('For Dressing')
    certificate = fields.Boolean('For Certificate')
    # merge_invoice_id = fields.Many2one('account.invoice', string='Merge Invoice', ondelete='cascade', copy=False)
#     inv_invoice_id = fields.Many2one('account.invoice',string='INV Invoice', ondelete='cascade', copy=False)
#     payment_history_ids = fields.One2many('account.payment.history','appointment_id',string="Payment History")
#     prescription = fields.Boolean('Enable Prescription', default=True)
    special_price_receptionist = fields.Float('Special Charges', readonly=False)
#     xray_price_receptionist  = fields.Float(string = 'X-ray Charges', store = True, readonly = True, compute = '_amount_all', track_visibility = 'always')
#     # counting_tab = fields.Html(string='Counting', compute="_counting_tab")
#     chief_complain = fields.Text("Chief Complain")
#     # active_patient  = fields.Integer(string = 'A', compute="_patient_list")
#     # not_done_patient  = fields.Integer(string = 'ND', compute="_patient_list")
#     # waiting_patient  = fields.Integer(string = 'W', compute="_patient_list")
#     # done_patient  = fields.Integer(string = 'T', compute="_patient_list")
#     vitals = fields.Text('Vitals')
    general_examination = fields.Char('General Examination')
#     # abdominal_examination_id = fields.Many2one('abdominal.examination','Abdominal Examination')
    abdominal_examination_note = fields.Text('Abdominal Examination')
#     # rectal_examination_id = fields.Many2one('rectal.examination','Rectal Examination')
    rectal_examination_ids = fields.Many2many('rectal.examination','rel_rectal_exa_id','rectal_id','appointment_id','Rectal Examination')
    rectal_examination_note = fields.Text('Rectal Examination Note')
    rs = fields.Char('Respiratory Syncytial')
    cvs = fields.Char('C.V.S.')
    cns = fields.Char('C.N.S')
    external_genitals = fields.Char(' Hernial sites')
#     per_vaginal = fields.Text('Per Vaginal Examination')
    remark = fields.Text('Notes')
    pulse = fields.Float(string="Pulse", digits=dp.get_precision('Pulse'))
    bp = fields.Float(string="BP", digits=dp.get_precision('BP'))
    lbp = fields.Float(string="BP", digits=dp.get_precision('LBP'))
    temperature = fields.Float(string="Temp", digits=dp.get_precision('Temp'))
    rr = fields.Float(string="RR", digits=dp.get_precision('RR'))
    spo2 = fields.Float(string='SPO2', digits=dp.get_precision('Spo2'))
    pain_score = fields.Selection([('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'), ('nine', '9'), ('ten', '10')], default="one",string="Pain Score")
    adv_followup_date = fields.Date(string="Followup Date")
#     second_diagonsis = fields.Char('Secondary Diagnosis',default=None)
    appt_prov_diagnosis = fields.Text(string="Provisional Diagnosis")
    second_diagonsiss = fields.Text('Secondary Diagnosis')
#     p_total = fields.Float('Pathology Total',compute='_kaizen_total')
#     r_total = fields.Float('Radiology Total',compute='_kaizen_total')
#     e_total = fields.Float('Endoscopy Total',compute='_kaizen_total')
#     m_total = fields.Float('Manometry Total',compute='_kaizen_total')
#     os_total = fields.Float('Other Services Total',compute='_kaizen_total')
#     final_amount = fields.Float('Total Investigation Charges',compute='_kaizen_totall')
    bmi_lines_ids = fields.One2many(related='patient_id.bmi_line_ids')

#     @api.depends('radiology_line.price','pathology_line.price','endoscopy_line.price','manometry_line.price','other_services_line.price')
#     def _kaizen_total(self):
#         for itnr in self:
#             for line in itnr.pathology_line:
#                 itnr.p_total += line.price
#             for line in itnr.radiology_line:
#                 itnr.r_total += line.price
#             for line in itnr.endoscopy_line:
#                 itnr.e_total += line.price
#             for line in itnr.manometry_line:
#                 itnr.m_total += line.price
#             for line in itnr.other_services_line:
#                 itnr.os_total += line.price

#     @api.depends('p_total','r_total','e_total','m_total','os_total')
#     def _kaizen_totall(self):
#         for app in self:
#             app.final_amount = float(app.p_total) + float(app.r_total) + float(app.e_total)+ float(app.m_total)+ float(app.os_total)

    def get_name(self,obj):
        if obj.patient_id:
            return obj.patient_id.name.title()
    
    @api.onchange('doctor_id')
    def onchange_doctor(self):
        self.cabin_no = self.doctor_id.cabin_no

#     @api.onchange('associated_disease')
#     def onchange_associated_disease(self):
#         if not self.second_diagonsis:
#             self.second_diagonsis = self.associated_disease.name and self.associated_disease.name or False
# #changed method from function --> onchange method
#     @api.model
#     def create(self, vals):
#         res = super(Appointment, self).create(vals)
#         for appointment in res:
#             appointments_ids = self.search([('patient_id','=',res.patient_id.id),('state','=','done')])
#             if appointments_ids:
#                 latest_appointment_id = max(appointments_ids.ids)
#                 latest_appointment = self.browse(latest_appointment_id)
#                 appointment.diagnosis_id = latest_appointment.diagnosis_id
#                 appointment.group_id = latest_appointment.group_id
#                 appointment.associated_disease = latest_appointment.associated_disease
#                 appointment.past_ho = latest_appointment.past_ho
#                 appointment.post_medication = latest_appointment.post_medication
#                 appointment.previous_inv = latest_appointment.previous_inv
#                 appointment.family_ho = latest_appointment.family_ho

#                 past_surgery_lines = []
#                 for line in latest_appointment.past_surgeries_ids:
#                     past_surgery_lines.append((0,0,{
#                         'date': line.date,
#                         'description': line.description,
#                         'result': line.result,
#                         'hosp_or_doctor': line.hosp_or_doctor,
#                     }))
#                 appointment.past_surgeries_ids = past_surgery_lines

#                 # personal_his_lines = []
#                 # for line in latest_appointment.personal_his_ids:
#                 #     personal_his_lines.append((0,0,{
#                 #         'personal_his_id': line.personal_his_id,
#                 #         'personal_his': line.personal_his,
#                 #     }))
#                 # appointment.personal_his_ids = personal_his_lines

#                 session1_image_lines = []
#                 for line in latest_appointment.session1_image_ids:
#                     session1_image_lines.append((0,0,{
#                         's_image1':line.s_image1,
#                         's_date1':line.s_date1,
#                     }))
#                 appointment.session1_image_ids = session1_image_lines

#                 prescription_lines = []
#                 for line in latest_appointment.prescription_line:
#                     prescription_lines.append((0,0,{
#                         'product_id':line.product_id.id,
#                         'common_dosage':line.common_dosage.id,
#                         'sub_frequency_id':line.sub_frequency_id.id,
#                         'days':line.days,
#                         'quantity':line.quantity,
#                     }))
#                 appointment.prescription_line = prescription_lines
#                 result1 = []
#                 for prescription in appointment.prescription_line:
#                     if prescription.product_id.product_exception=='yes':
#                         qty = prescription.product_id.no_per_pack
#                         price = prescription.product_id.list_price
#                     else:
#                         qty = prescription.quantity
#                         price = prescription.product_id.list_price * qty
#                     result1.append((0, 0, {'product_id': prescription.product_id.id,
#                                            'price':prescription.product_id.list_price,
#                                            'common_dosage':prescription.common_dosage.id,
#                                            'days':prescription.days,
#                                            'quantity':qty,
#                                            'cost_per_unit': price,
#                                            'sequence':prescription.sequence
#                                            }))
#                 appointment.prescription_line_price = result1
#             appointment.special_price_receptionist = appointment.special_price
#             total = 0
#             for line in appointment.prescription_line:
#                 if line.product_id.product_exception=='yes':
#                     total += line.product_id.list_price
#                 else:
#                     total += line.product_id.list_price * line.quantity
#             appointment.prescription_total = total
#             for path_line in res.pathology_line:
#                 if not path_line.inv_username:
#                     path_line.inv_username = path_line.write_uid.id
#         return res

#     @api.multi
#     def write(self, vals):
#         if vals.has_key('special_price'):
#              vals.update({'special_price_receptionist': vals.get('special_price')})
#         if vals.has_key('patient_id'):
#             appointments_ids = self.search([('patient_id','=',vals['patient_id']),('state','=','done')])
#             if appointments_ids:
#                 latest_appointment_id = max(appointments_ids.ids)
#                 latest_appointment = self.browse(latest_appointment_id)
#                 self.diagnosis_id = latest_appointment.diagnosis_id
#                 self.group_id = latest_appointment.group_id
#                 prescription_lines = []
#                 for line in latest_appointment.prescription_line:
#                     prescription_lines.append((0,0,{
#                         'product_id':line.product_id,
#                         'common_dosage':line.common_dosage,
#                         'sub_frequency_id':line.sub_frequency_id.id,
#                         'days':line.days,
#                         'quantity':line.quantity,
#                     }))
#                 self.prescription_line = prescription_lines

#         res = super(Appointment, self).write(vals)

#         for path_line in self.pathology_line:
#                 if not path_line.inv_username:
#                     path_line.inv_username = path_line.write_uid.id

#         return res


#     @api.onchange('prescription_line')
#     def onchange_prescription_line(self):
#         for appointment in self:
#             total = 0
#             for line in appointment.prescription_line:
#                 if line.product_id.product_exception=='yes':
#                     total += line.product_id.list_price
#                 else:
#                     total += line.product_id.list_price * line.quantity
#             appointment.prescription_total = total
#             result1 = []
#             for prescription in appointment.prescription_line:
#                 if prescription.product_id.product_exception=='yes':
#                     qty = prescription.product_id.no_per_pack
#                     price = prescription.product_id.list_price
#                 else:
#                     qty = prescription.quantity
#                     price = prescription.product_id.list_price * qty
#                 result1.append((0, 0, {'product_id': prescription.product_id.id,
#                                        'price':prescription.product_id.list_price,
#                                        'common_dosage':prescription.common_dosage.id,
#                                        'sub_frequency_id':prescription.product_id.suffix_frequency_id.id,
#                                        'days':prescription.days,
#                                        'quantity':qty,
#                                        'cost_per_unit': price,
#                                        'sequence':prescription.sequence
#                                        }))
#             appointment.prescription_line_price = result1

# #method obsolete because there is no provision of selecting department in appointment
#     # @api.onchange('department_id')
#     # @api.multi
#     # def onchnage_department(self):
#     #     physician = self.env['hms.physician'].search([('is_primary_surgeon', '=', True), ('department_ids', '=', self.department_id.id)], limit=1)
#     #     self.write({'physician_id': physician.id})
#     #     self.physician_id = physician.id
    
# #Code Block For Wednesday Functionality ,13 Feb
#     # @api.model
#     # def default_get(self, fields):
#     #     res = super(Appointment, self).default_get(fields)
#     #     if res.get('date'):
#     #         week_name = time.strftime("%A", time.strptime(res.get('date'), "%Y-%m-%d %H:%M:%S"))
#     #         get_time = time.strftime("%H:%M:%S", time.strptime(res.get('date'), "%Y-%m-%d %H:%M:%S"))
#     #         if week_name == 'Wednesday' and get_time >= '00:00:00' and get_time <= '02:00:00':
#     #             res.update({'wednesday': True,'special_day':True,'follow_foc':False,'case_type':'special'})
#     #     return res

#     @api.onchange('purpose_id')
#     def on_change_purpose(self):
#         if self.purpose_id in self.env.ref("hms.purpose_follow_up"):
#             self.follow_foc = True
#         else :
#             self.follow_foc = False
#         if self.purpose_id.product_id:
#             self.product_id = self.purpose_id.product_id.id
    
#     @api.multi
#     def action_view_bmi(self):
#         print "================action_view_bmi"
#         return {
#             'name': _('BMI'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'patient.bmi',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id', '=', self.patient_id.id)],
#             'context': {'default_patient_id': self.patient_id.id,'default_appointment': self.id},
#     }

#     @api.multi
#     def action_cost_estimation_form(self):
#         return {
#             'name': _('Cost Estimation'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'cost.estimation',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id', '=', self.patient_id.id)],
#             'context': {'default_patient_id': self.patient_id.id,'default_appointment': self.id},
#     }

#     @api.multi
#     def action_admission_note(self):
#         return {
#             'name': _('Admission Note'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'admission.note',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id', '=', self.patient_id.id)],
#             'context': {'default_patient_id': self.patient_id.id},
#         }

#     @api.onchange('hypersensitive')
#     def on_change_hypersensitive(self):
#         self.patient_id.write({'hypersensitive':self.hypersensitive})

#     @api.onchange('product_id','opd_reg_spe','special_day','opd_foc','follow_foc')
#     def onchange_opd_reg_spe_product_id(self):
#         if self.opd_reg_spe:
#             self.special_price = self.product_id.lst_price
#         if self.special_day:
#             self.special_price-= self.product_id.special_day_price
# #             self.echo_prescription = True
#             if self.opd_foc:
#                 self.special_price = 0.0
#         if self.follow_foc:
#             self.special_price = self.product_id.lst_price
#             #self.special_price = self.product_id.lst_price / 2
#             if self.special_day:
#                 self.special_price = self.product_id.lst_price - self.product_id.special_day_price
#             if self.opd_foc:
#                 self.special_price = 0.0
#         if self.opd_foc:
#             self.special_price = 0.0
#         self.special_price_receptionist = self.special_price

#     @api.onchange('case_type','follow_foc','opd_foc')
#     def onchange_case_type(self):
#         self.special_day = False  
#         self.echo_prescription = False
#         # self.wednesday = False
#         if self.case_type == 'normal':
#             self.special_price_receptionist = self.product_id.lst_price
#             if self.follow_foc:
#                 self.special_price = self.product_id.lst_price
#                 #self.special_price_receptionist = self.product_id.lst_price / 2
#             if self.opd_foc:
#                 self.special_price_receptionist = 0.0
#         if self.case_type == 'special':
#             self.special_price_receptionist =self.product_id.lst_price - self.product_id.special_day_price
# #             self.special_day = True
#             # self.wednesday = True
#             self.special_day = True
#             if not self.env['prescription.order'].search([('patient_id', '=', self.patient_id.id)]):
#                 self.echo_prescription = True
#         if self.case_type == 'day':
#            self.special_price_receptionist = self.product_id.day_price
#         if self.case_type == 'file':
#             self.special_price_receptionist = self.product_id.file_price
#         if self.case_type == 'night':
#             self.special_price_receptionist = self.product_id.night_price
#         self.special_price_receptionist = self.special_price
#         # if self.case_type == 'camp':
#         #     self.special_price = ''

#     @api.onchange('special_price_receptionist')
#     def onchange_special(self):
#         if self.special_price_receptionist:
#             self.special_price = self.special_price_receptionist

#     @api.depends('patient_id')
#     @api.onchange('patient_id')
#     def onchange_patient_id(self):
#         res = super(Appointment, self).onchange_patient_id()
#         self.diagnosis_id = False
#         self.group_id = False
#         self.prescription_line = False
#         self.purpose_id = False

#         self.hypersensitive = self.patient_id.hypersensitive
#         visit_count = self.search_count([('patient_id', '=', self.patient_id.id)])
#         if self.patient_id and self.patient_id.visits:
#             visit_count+=self.patient_id.visits
#         self.visit_count = visit_count
#         if self.patient_id.followup_validity:
#             validity = datetime.strptime(self.patient_id.followup_validity, '%Y-%m-%d')
#             if datetime.now()<=validity:
#                 self.follow_foc = True
#                 # self.purpose_id = self.env.ref("hms.purpose_follow_up")
#                 # self.product_id = self.purpose_id.product_id.id
#         if self.patient_id.opd_foc:
#             validity = datetime.strptime(self.patient_id.followup_validity, '%Y-%m-%d')
#             if datetime.now()<=validity:
#                 self.opd_foc = True
#         if self.patient_id and self.patient_id.findings:
#             self.notes = self.patient_id.findings
#         appointments_ids = self.search([('patient_id','=',self.patient_id.id),('state','=','done')])
#         if appointments_ids:
#             latest_appointment_id = max(appointments_ids.ids)
#             latest_appointment = self.browse(latest_appointment_id)
#             self.notes = latest_appointment.notes
# #             if self.notes:
# #                 self.notes += "\n" + (latest_appointment.notes or '')
# #             else:
# #                 self.notes = latest_appointment.notes
# #             self.diagnosis_id = latest_appointment.diagnosis_id
# #             self.group_id = latest_appointment.group_id
#         history_ids = []
#         for appointment in appointments_ids:
#             invoices = self.env['account.invoice'].search([('appointment_id','=',appointment.id), ('state','=','paid')])
#             xray_total = 0
#             physio_total = 0
#             consultation = 0
#             for invoice in invoices:
#                 for line in invoice.invoice_line_ids:
#                     if line.product_id.hospital_product_type=='radiology':
#                         xray_total+= line.price_unit
#                     # if line.product_id.hospital_product_type=='physiotherapy':
#                     #     physio_total+= line.price_unit
#                     if line.product_id.hospital_product_type=='consultation':
#                         consultation+= line.price_unit
#             history_ids.append((0, 0, {
#                 'patient_id':self.patient_id.id,
#                 'appointment_id':self.id,
#                 'total_consult':consultation,
#                 'total_xray':xray_total,
#                 'date':appointment.date,
#             }))
#         self.payment_history_ids = history_ids
#         self.department_name = self.department_id.department_name
# #         if self.patient_id.department_id.department_name == 'Orthopedic':
#         self.product_id = self.product_id.search([('hospital_product_type', '=', "consultation")], limit=1).id
# #         if self.patient_id.department_id.name == 'Paediatric':
# #             self.pae_product_id = self.pae_product_id.search([('hospital_product_type', '=', "consultation_paediatric")], limit=1).id
# #         self.street = self.patient_id.street
# #         self.street2 = self.patient_id.street2
# #         self.city = self.patient_id.city
# #         self.zip = self.patient_id.zip
# #         self.sex = self.patient_id.sex
# #         self.age = self.patient_id.age
# #         self.first_name = self.patient_id.first_name
# #         self.middel_name = self.patient_id.middel_name
# #         self.last_name = self.patient_id.last_name
# #         self.language = self.patient_id.language
#         return res

#     @api.onchange('advice_group_ids')
#     def onchange_advice_group_ids(self):
#         if self.advice_group_ids.filtered(lambda att: att.investigation_type == 'advices_group'):
#             product_lines = []
#             for rec in self:
#                 for line in rec.advice_group_ids.mapped('group_line'):
#                     product_lines.append((0,0,{
#                         'name': line.name.name,
#                     }))
#                 rec.advices_group_lines_ids = product_lines

#     @api.onchange('lab_group_id')
#     def on_change_lab_group_id(self):
#         if self.lab_group_id.investigation_type == 'pathology':
#             product_lines = []
#             for line in self.lab_group_id.group_line:
#                 product_lines.append((0,0,{
#                     'product_id': line.product_id.id,
#                     'price': line.price,
#                     'inv_username': line.env.user.name,
#                     'instruction': line.instruction,
#                 }))
#             self.pathology_line = product_lines

#         if self.lab_group_id.investigation_type == 'radiology':
#             product_lines = []
#             for line in self.lab_group_id.group_line:
#                 product_lines.append((0,0,{
#                     'product_id': line.product_id.id,
#                     'price': line.price,
#                     'instruction': line.instruction,
#                 }))
#             self.radiology_line = product_lines

#         if self.lab_group_id.investigation_type == 'manometry':
#             product_lines = []
#             for line in self.lab_group_id.group_line:
#                 product_lines.append((0,0,{
#                     'product_id': line.product_id.id,
#                     'price': line.price,
#                     'instruction': line.instruction,
#                 }))
#             self.manometry_line = product_lines

#         if self.lab_group_id.investigation_type == 'endoscopy':
#             product_lines = []
#             for line in self.lab_group_id.group_line:
#                 product_lines.append((0,0,{
#                     'product_id': line.product_id.id,
#                     'price': line.price,
#                     'instruction': line.instruction,
#                 }))
#             self.endoscopy_line = product_lines

#         if self.lab_group_id.investigation_type == 'os':
#             product_lines = []
#             for line in self.lab_group_id.group_line:
#                 product_lines.append((0,0,{
#                     'product_id': line.product_id.id,
#                     'price': line.price,
#                     'instruction': line.instruction,
#                 }))
#             self.other_services_line = product_lines

#         if self.lab_group_id.investigation_type == 'all':
#             rad_product_lines = []
#             path_product_lines = []
#             endo_product_lines = []
#             mano_product_lines = []
#             os_product_lines = []
#             for line in self.lab_group_id.group_line:
#                 if line.product_id.hospital_product_type == 'radiology':
#                     rad_product_lines.append((0,0,{
#                         'product_id': line.product_id.id,
#                         'price': line.price,
#                         'instruction': line.instruction,
#                     }))
#                     self.radiology_line = rad_product_lines
#                 if line.product_id.hospital_product_type == 'pathology':
#                     path_product_lines.append((0,0,{
#                         'product_id': line.product_id.id,
#                         'price': line.price,
#                         'instruction': line.instruction,
#                     }))
#                     self.pathology_line = path_product_lines
#                 if line.product_id.hospital_product_type == 'endoscopy':
#                     endo_product_lines.append((0,0,{
#                         'product_id': line.product_id.id,
#                         'price': line.price,
#                         'instruction': line.instruction,
#                     }))
#                 self.endoscopy_line = endo_product_lines
#                 if line.product_id.hospital_product_type == 'manometry':
#                     mano_product_lines.append((0,0,{
#                         'product_id': line.product_id.id,
#                         'price': line.price,
#                         'instruction': line.instruction,
#                     }))
#                 self.manometry_line = mano_product_lines
#                 if line.product_id.hospital_product_type == 'os':
#                     os_product_lines.append((0,0,{
#                         'product_id': line.product_id.id,
#                         'price': line.price,
#                         'instruction': line.instruction,
#                     }))
#                 self.other_services_line = os_product_lines


#     @api.onchange('group_id', 'echo_prescription', 'pregnancy_warning', 'lactation')
#     def on_change_group_id(self):
#         self.prescription_line = []
#         product_lines = []
#         group_obj = self.env['medicament.group.line']
#         for group in self.group_id.group_line:
#             lines = []
#             echo_lines = {}
#             e_lines=[]
#             echo_price = 0
#             echo_p = 0
#             for medicament in group.medicament_group_id.medicine_list:
#                 if self.pregnancy_warning and medicament.product_id.pregnancy_warning or self.lactation and medicament.product_id.lactation:
#                     pass
#                 elif self.echo_prescription:
#                     echo_price = medicament.product_id.lst_price
#                     if echo_lines.has_key(echo_price):
#                         echo_lines[echo_price].append(medicament.id)
#                     else:
#                         echo_lines.update({echo_price:[medicament.id]})
#                     min_key = min(echo_lines.keys())
#                     e_lines = echo_lines[min_key]
#                 else:
#                     lines.append(medicament.id)
#             if self.echo_prescription:
#                 lines = e_lines
#             else:
#                 lines = lines
#             limit = 0
#             if group.medicament_group_id.limit > len(lines):
#                 limit = len(lines)
#             else:
#                 limit = group.medicament_group_id.limit
#             list_l = random.sample(lines, limit)
#             for line in group_obj.browse(list_l):
#                 qty = float(line.common_dosage.code) * int(self.days_1) or 0.0
#                 if line.product_id.product_exception=='yes':
#                     qty = line.product_id.no_per_pack
#                 product_lines.append((0, 0, {
#                     'product_id': line.product_id.id,
#                     'common_dosage': line.product_id and line.product_id.common_dosage and line.product_id.common_dosage.id,
#                     'sub_frequency_id':line.product_id and line.product_id.suffix_frequency_id and line.product_id.suffix_frequency_id.id,
#                     'days': self.days_1,
#                     'quantity' : qty,
#                     'sequence':99
#                 }))
#         self.prescription_line = product_lines

#     @api.onchange('diagnosis_id')
#     def on_change_diagnosis_id(self):
#         self.group_id = False

#     @api.multi
#     def action_button_appointment(self):
#         return {
#             'name': _(self.name),
#             'view_type': 'form',
#             'view_mode': 'form,tree',
#             'res_model': 'hms.appointment',
#             'type': 'ir.actions.act_window',
#             'target': 'inline',
#             'res_id': self.id,
#         }

#     @api.multi
#     def action_zero(self):
#         self.cabin = 'zero'
#         return self.action_button_appointment()

#     @api.multi
#     def action_cabin(self):
#         temp = fields.Boolean("temp",default=False)
#         if self.physician_id.cabin_no == '1':
#             if self.state in ['in_consultation'] and self.cabin not in ['one']:
#                 raise UserError(("Patient is already in cabin"))
#             found = self.search([('cabin','=','one'),('patient_id','!=',self.patient_id.id)])
#             print "###@@found",found,"&&&&Cabin###",self.cabin
#             if not found:
#                 temp=True
#             if found:
#                 temp=False
#         elif self.physician_id.cabin_no == '2':
#             if self.state in ['in_consultation'] and self.cabin not in ['two']:
#                 raise UserError(("Patient is already in cabin"))
#             found = self.search([('cabin','=','two'),('patient_id','!=',self.patient_id.id)])
#             if not found:
#                 temp=True
#             if found:
#                 temp=False
#         elif self.physician_id.cabin_no == '3':
#             if self.state in ['in_consultation'] and self.cabin not in ['three']:
#                 raise UserError(("Patient is already in cabin"))
#             found = self.search([('cabin','=','three'),('patient_id','!=',self.patient_id.id)])
#             if not found:
#                 temp=True
#             if found:
#                 temp=False
#         elif self.physician_id.cabin_no == '4':
#             if self.state in ['in_consultation'] and self.cabin not in ['four']:
#                 raise UserError(("Patient is already in cabin"))
#             found = self.search([('cabin','=','four'),('patient_id','!=',self.patient_id.id)])
#             if not found:
#                 temp=True
#             if found:
#                 temp=False
#         elif self.physician_id.cabin_no == '5':
#             if self.state in ['in_consultation'] and self.cabin not in ['five']:
#                 raise UserError(("Patient is already in cabin"))
#             found = self.search([('cabin','=','five'),('patient_id','!=',self.patient_id.id)])
#             if not found:
#                 temp=True
#             if found:
#                 temp=False
#         elif self.physician_id.cabin_no == '6':
#             if self.state in ['in_consultation'] and self.cabin not in ['six']:
#                 raise UserError(("Patient is already in cabin"))
#             found = self.search([('cabin','=','six'),('patient_id','!=',self.patient_id.id)])
#             if not found:
#                 temp=True
#             if found:
#                 temp=False
#         else:
#             self.cabin = 'zero'
#         #found = self.search([('cabin','=',self.physician_id.cabin_no),('patient_id','!=',self.patient_id.id)])
#         #found = self.search([('cabin','=',self.cabin),('patient_id','!=',self.patient_id.id)])
#         #print "###@@found",found,"&&&&Cabin###",self.cabin,"&&&&Cabin_NO###",self.physician_id.cabin_no
#         if temp:
#             if self.state in ['waiting','sr_dr','f_x','dressing']:
#                 if self.physician_id.cabin_no == '1':
#                     self.cabin = 'one'
#                 elif self.physician_id.cabin_no == '2':
#                     self.cabin = 'two'
#                 elif self.physician_id.cabin_no == '3':
#                     self.cabin = 'three'
#                 elif self.physician_id.cabin_no == '4':
#                     self.cabin = 'four'
#                 elif self.physician_id.cabin_no == '5':
#                     self.cabin = 'five'
#                 elif self.physician_id.cabin_no == '6':
#                     self.cabin = 'six'
#                 else:
#                     self.cabin = 'zero'
#                 self.prev_state = self.state
#                 self.appointment_consultation()
#             return self.action_button_appointment()
#         if not temp:
#             print "###@@found",found,"&&&&Cabin###",self.cabin,"&&&&Cabin_NO###",self.physician_id.cabin_no    
#             raise UserError(("Cabin is already allocated"))
        

#     @api.multi
#     def action_one(self):
#         if self.state in ['in_consultation'] and self.cabin not in ['one']:
#             raise UserError(("Patient is already in cabin"))
#         found = self.search([('cabin','=','one'),('patient_id','!=',self.patient_id.id)])
#         print "###@@found",found,"&&&&Cabin###",self.cabin
#         if not found:
#             if self.state in ['waiting','sr_dr','f_x','dressing']:
#                 self.cabin = 'one'
#                 self.prev_state = self.state
#                 self.appointment_consultation()
#             return self.action_button_appointment()
#         if found:
#             raise UserError(("Cabin is already allocated"))

#     @api.multi
#     def action_two(self):
#         if self.state in ['in_consultation'] and self.cabin not in ['two']:
#             raise UserError(("Patient is already in cabin"))
#         found = self.search([('cabin','=','two'),('patient_id','!=',self.patient_id.id)])
#         if not found:
#             if self.state in ['waiting','sr_dr','f_x','dressing']:
#                 self.cabin = 'two'
#                 self.prev_state = self.state
#                 self.appointment_consultation()
#             return self.action_button_appointment()
#         if found:
#             raise UserError(("Cabin  is already allocated"))

#     @api.multi
#     def action_three(self):
#         if self.state in ['in_consultation'] and self.cabin not in ['three']:
#             raise UserError(("Patient is already in cabin"))
#         found = self.search([('cabin','=','three'),('patient_id','!=',self.patient_id.id)])
#         if not found:
#             if self.state in ['waiting','sr_dr','f_x','dressing']:
#                 self.cabin = 'three'
#                 self.prev_state = self.state
#                 self.appointment_consultation()
#             return self.action_button_appointment()
#         if found:
#             raise UserError(("Cabin  is already allocated"))

#     @api.multi
#     def action_four(self):
#         if self.state in ['in_consultation'] and self.cabin not in ['four']:
#             raise UserError(("Patient is already in cabin"))
#         found = self.search([('cabin','=','four'),('patient_id','!=',self.patient_id.id)])
#         if not found:
#             if self.state in ['waiting','sr_dr','f_x','dressing']:
#                 self.cabin = 'four'
#                 self.prev_state = self.state
#                 self.appointment_consultation()
#             return self.action_button_appointment()
#         if found:
#             raise UserError(("Cabin is already allocated"))


#     @api.multi
#     def refresh_waiting_list(self):
#         pass

    def appointment_done(self):
        self.state = 'done'
        # self.sequence = 6

        if not self.patient_id.followup_validity:
            self.patient_id.write({'followup_validity': datetime.now() + dateutil.relativedelta.relativedelta(months=6)})

#         hypersensitive = self.hypersensitive
#         follow_foc = self.follow_foc
#         opd_foc = self.opd_foc
#         for data in self:
#             if data.days_1 or data.weeks or data.months:
#                 hypersensitive = hypersensitive
#                 if data.patient_id.followup_validity:
#                     validity = datetime.strptime(data.patient_id.followup_validity, '%Y-%m-%d')
#                     if datetime.now()<=validity:
#                         follow_foc = True
#                     if data.patient_id.opd_foc:
#                         validity = datetime.strptime(data.patient_id.followup_validity, '%Y-%m-%d')
#                         if datetime.now()<=validity:
#                             opd_foc = True
#                 date = fields.Date.from_string(self.date)
#                 days = data.days_1
#                 weeks = data.weeks
#                 months = data.months
#                 follow_date = date + relativedelta(days=days,weeks=weeks,months=months)
#                 data.follow_date = fields.Date.to_string(follow_date)
# #                 self.create({
# #                     'patient_id' : data.patient_id.id,
# #                     'physician_id' : data.physician_id.id,
# #                     'date': data.follow_date,
# #                     'purpose_id': data.reason_id.id or False,
# #                     'consultation_type':'followup',
# #                     'hypersensitive':hypersensitive,
# #                     'follow_foc':follow_foc,
# #                     'opd_foc':opd_foc,
# #                     'radilogy_date':data.follow_date
# #                     })
#         if self.prescription_line:
#             order_ids = self.env['prescription.order'].search([('appointment','=',self.id)])
#             order_id = False
#             if not order_ids:
#                 order = self.env['prescription.order'].create({
#                         'patient_id': self.patient_id.id,
#                         'appointment': self.id,
#                         'language': self.language,
#                         'physician_id': self.physician_id.id,
#                         'notes': self.others,
#                         'prescription':self.prescription,
#                         'prescription_date': datetime.now(),
#                     })
#                 order_id = order.id
#             if order_ids:
#                 order_id = order_ids[0].id
#             for prescription in self.prescription_line:
#                 prescription.write({'prescription_id': order_id})

#         # if self.pathology_line:
#         #     investigation_obj = self.env['hms.investigation']
#         #     inv_ids = investigation_obj.search([('appointment_id','=',self.id)])
#         #     inv_id = False
#         #     if not inv_ids:
#         #         pathology = investigation_obj.create({
#         #                 'patient_id': self.patient_id.id,
#         #                 'investigation_type': 'pathology',
#         #                 'appointment_id': self.id,
#         #                 'group_id':self.lab_group_id.id,
#         #             })
#         #         inv_id = pathology.id
#         #     if inv_ids:
#         #         inv_id = inv_ids[0].id
#         #     for patho in self.pathology_line:
#         #         patho.write({'investigation_id': inv_id})

#         # if self.manometry_line:
#         #     investigation_obj = self.env['hms.investigation']
#         #     inv_ids = investigation_obj.search([('appointment_id','=',self.id)])
#         #     inv_id = False
#         #     if not inv_ids:
#         #         manometry = investigation_obj.create({
#         #                 'patient_id': self.patient_id.id,
#         #                 'investigation_type': 'manometry',
#         #                 'appointment_id': self.id,
#         #                 # 'group_id':self.lab_group_id.id,
#         #             })
#         #         inv_id = manometry.id
#         #     if inv_ids:
#         #         inv_id = inv_ids[0].id
#         #     for manom in self.manometry_line:
#         #         manom.write({'investigation_id': inv_id})

#         # if self.endoscopy_line:
#         #     investigation_obj = self.env['hms.investigation']
#         #     inv_ids = investigation_obj.search([('appointment_id','=',self.id)])
#         #     inv_id = False
#         #     if not inv_ids:
#         #         endoscopy = investigation_obj.create({
#         #                 'patient_id': self.patient_id.id,
#         #                 'investigation_type': 'endoscopy',
#         #                 'appointment_id': self.id,
#         #                 # 'group_id':self.lab_group_id.id,
#         #             })
#         #         inv_id = endoscopy.id
#         #     if inv_ids:
#         #         inv_id = inv_ids[0].id
#         #     for endos in self.endoscopy_line:
#         #         endos.write({'investigation_id': inv_id})

#         self.cabin = 'zero'
#         super(Appointment, self).appointment_done()
#         return self.action_list_appointment()

#     @api.onchange('days_1','weeks','months')
#     def on_change_days_week_month(self):
#         if self.days_1 or self.weeks or self.months:
#             days_1 = self.days_1
#             weeks = self.weeks * 7
#             months = self.months * 30
#             total_days = days_1 + weeks + months
#             for line in self.prescription_line:
#                 line.days = total_days
#                 line.quantity = line.days * float(line.common_dosage.code)
#                 if line.product_id.product_exception=='yes':
#                     line.quantity = line.product_id.no_per_pack

#     @api.multi
#     def merge_invoice(self):
#         invoice_obj = self.env['account.invoice']
#         account_id = False
#         if self.merge_invoice_id:
#             raise UserError(_('Invoice is already created.Please refresh view'))
#         price = self.special_price
#         # if not self.invoice_id:
#         #     product_id = self.product_id
#         #     #price = product_id.lst_price
#         #     if product_id.id:
#         #         account_id = product_id.property_account_income_id.id
#         #     if not account_id:
#         #         prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#         #         account_id = prop and prop.id or False
#         #     invoice = invoice_obj.create({
#         #     'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
#         #     'partner_id': self.patient_id.partner_id.id,
#         #     'patient_id': self.patient_id.id,
#         #     'type': 'out_invoice',
#         #     'name': '-',
#         #     'origin': self.name,
#         #     'report_type':'consult',
#         #     'appointment_id': self.id,
#         #     'consultant_doctor_id':self.patient_id.primary_doctor.id,
#         #     'treating_doctor_id':self.patient_id.primary_doctor.id,
#         #     'currency_id': self.env.user.company_id.currency_id.id,
#         #     'invoice_line_ids': [(0, 0, {
#         #         'name': product_id.name,
#         #         'price_unit': price,
#         #         'account_id': account_id,
#         #         'quantity': 1.0,
#         #         'discount': 0.0,
#         #         'uom_id': product_id.uom_id.id,
#         #         'product_id': product_id.id,
#         #         'account_analytic_id': False,
#         #                             })],
#         #     })
#         #     self.invoice_id = invoice.id
#         #     self.opd_fee = 'right'
#         if not self.merge_invoice_id:
#             invoices = invoice_obj.search([('appointment_id','=',self.id),('state','not in',['paid','cancel']),('report_type','in',['radiology'])])
#             invoice = invoice_obj.create({
#                 'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
#                 'partner_id': self.patient_id.partner_id.id,
#                 'patient_id': self.patient_id.id,
#                 'type': 'out_invoice',
#                 'name': '-',
#                 'origin': self.name,
#                 'report_type':'consult',
#                 'appointment_id': self.id,
#                 'consultant_doctor_id':self.patient_id.primary_doctor.id,
#                 'treating_doctor_id':self.patient_id.primary_doctor.id,
#                 'currency_id': self.env.user.company_id.currency_id.id,
#             })
#             for record in invoices:
#                 account_id = False
#                 for line in record.invoice_line_ids:
#                     if line.product_id.hospital_product_type in ['radiology','pathology','endoscopy','manometry','os']:
#                         account_id = self.env.ref('hms_invoice.bill_to_hosp_radiology')
#                     if line.product_id.hospital_product_type=='physiotherapy':
#                         account_id = self.env.ref('hms_invoice.bill_to_hosp_physiotherapy')
#                     if line.product_id.hospital_product_type=='consultation':
#                         account_id = line.account_id
#                     if line.product_id.hospital_product_type=='package':
#                         account_id = self.env.ref('hms_invoice.bill_to_hosp_ipd')

#                     values = {
#                             'name': line.product_id.name,
#                             'price_unit': line.price_unit,
#                             'account_id': account_id and account_id.id or False,
#                             'quantity': 1.0,
#                             'discount': 0.0,
#                             'uom_id': line.product_id.uom_id.id,
#                             'product_id': line.product_id.id,
#                             'account_analytic_id': False,
#                             'invoice_id':invoice.id
#                     }
#                     self.env['account.invoice.line'].create(values)
#             self.merge_invoice_id = invoice.id
#             # self.invoice_id = invoice.id
#             radiology_ids = self.env['hms.investigation'].search([('appointment_id','=',self.id)])
#             for radiology in radiology_ids:
#                 if radiology.invoice_id and radiology.invoice_id.state not in['paid','cancel']:
#                     radiology.invoice_id = invoice.id


#     @api.multi
#     def view_merge_invoice(self):
#         invoice_ids = self.mapped('merge_invoice_id')
#         invoice_obj = self.env['account.invoice']
#         radiology_ids = self.env['hms.investigation'].search([('appointment_id','=',self.id)])
#         for radiology in radiology_ids:
#             if radiology.invoice_id and radiology.invoice_id.state not in['paid','cancel']:
#                 radiology.invoice_id = invoice_ids.ids[0]
#         invoices = invoice_obj.search([('id','!=',self.merge_invoice_id.id),('appointment_id','=',self.id),('state','not in',['paid','cancel']),('report_type','in',['radiology'])])
#         for record in invoices:
#             product_ids = []
#             account_id = False
#             for line in self.merge_invoice_id.invoice_line_ids:
#                 product_ids.append(line.product_id.id)
#             for line in record.invoice_line_ids:
#                 if line.product_id.id not in product_ids:
#                     if line.product_id.hospital_product_type in ['radiology','pathology','endoscopy','manometry']:
#                         account_id = self.env.ref('hms_invoice.bill_to_hosp_radiology')
#                     if line.product_id.hospital_product_type=='physiotherapy':
#                         account_id = self.env.ref('hms_invoice.bill_to_hosp_physiotherapy')
#                     if line.product_id.hospital_product_type=='consultancy':
#                         account_id = line.account_id
#                     values = {
#                             'name': line.product_id.name,
#                             'price_unit': line.price_unit,
#                             'account_id': account_id and account_id.id or False,
#                             'quantity': 1.0,
#                             'discount': 0.0,
#                             'uom_id': line.product_id.uom_id.id,
#                             'product_id': line.product_id.id,
#                             'account_analytic_id': False,
#                             'invoice_id':self.merge_invoice_id.id
#                     }
#                     self.env['account.invoice.line'].create(values)
#         imd = self.env['ir.model.data']
#         action = imd.xmlid_to_object('account.action_invoice_tree1')
#         list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
#         form_view_id = imd.xmlid_to_res_id('account.invoice_form')

#         result = {
#             'name': action.name,
#             'help': action.help,
#             'type': action.type,
#             'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
#             'target': action.target,
#             'context': action.context,
#             'res_model': action.res_model,
#             'id': action.id,
#             'domain': [('partner_id','=',self.patient_id.user_id.partner_id.id),('id','=',self.merge_invoice_id.id)],
#         }
#         if len(invoice_ids) > 1:
#             result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
#         elif len(invoice_ids) == 1:
#             result['views'] = [(form_view_id, 'form'), (list_view_id, 'tree')]
#             result['res_id'] = invoice_ids.ids[0]
#         else:
#             result = {'type': 'ir.actions.act_window_close'}
#         return result

    # @api.model
    # def create_invoice(self, values):
    #     # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #     if self.invoice_id:
    #         raise UserError(_('Invoice is already created.Please refresh view'))
    #     inv_obj = self.env['account.move']
    #     # ir_property_obj = self.env['ir.property']
    #     # inv_line_obj = self.env['account.move.line']
    #     product_id = self.product_id
    #     account_id = False
    #     price = self.special_price

    #     if product_id.id:
    #         account_id = product_id.property_account_income_id.id
    #     # if not account_id:
    #         # prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
    #         # account_id = prop and prop.id or False
    #     invoice = inv_obj.create({
    #         # 'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
    #         'partner_id': self.patient_id.partner_id.id,
    #         # 'patient_id': self.patient_id.id,
    #         # 'type': 'out_invoice',
    #         # 'name': '-',
    #         # 'origin': self.name,
    #         # 'report_type':'consult',
    #         'appointment_id': self.id,
    #         # 'consultant_doctor_id':self.patient_id.primary_doctor_id.id,
    #         # 'treating_doctor_id':self.patient_id.primary_doctor_id.id,
    #         # 'currency_id': self.env.user.company_id.currency_id.id,
    #         'invoice_line_ids': [(0, 0, {
    #             'name': product_id.name,
    #             'price_unit': price,
    #             # 'account_id': account_id,
    #             'quantity': 1.0,
    #             # 'discount': 0.0,
    #             # 'uom_id': product_id.uom_id.id,
    #             'product_id': product_id.id,
    #             # 'account_analytic_id': False,
    #         })],
    #     })
    #     self.invoice_id = invoice.id
    #     self.opd_fee = 'right'

#     @api.multi
#     def create_inv_invoice(self):
#         inv_obj = self.env['account.invoice']
#         ir_property_obj = self.env['ir.property']
#         inv_line_obj = self.env['account.invoice.line']
#         account_id = False
# #             acc_id = self.env.ref('hms_investigation.ac200111')
#         invoice_id = False
# #             if self.appointment_id and not self.appointment_id.bill_to_hospital:
#         res = {
#             'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
#             'partner_id': self.patient_id.partner_id.id,
#             'patient_id': self.patient_id.id,
#             'type': 'out_invoice',
#             'name': '-',
#             'origin': self.name,
#             'currency_id': self.env.user.company_id.currency_id.id,
#             'report_type': 'radiology',
#             'appointment_id': self.id,
#             'consultant_doctor_id':self.patient_id.primary_doctor.id,
#             'treating_doctor_id':self.patient_id.primary_doctor.id,
#         }
#         inv_line = []
#         #Radiology
#         for line in self.radiology_line:
#             if line.product_id.id:
#                 account_id = line.product_id.property_account_income_id.id
#                 if not account_id:
#                     prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#                     account_id = prop and prop.id or False
#                 inv_line.append((0, 0, {
#                     'name': line.product_id.name,
#                     'price_unit': line.price,
#                     'account_id': account_id,
#                     'quantity': 1.0,
#                     'discount': 0.0,
#                     'uom_id': line.product_id.uom_id.id,
#                     'product_id': line.product_id.id,
#                     'account_analytic_id': False,
#                 }))
#         #Pathology
#         for line in self.pathology_line:
#             if line.product_id.id:
#                 account_id = line.product_id.property_account_income_id.id
#             if not account_id:
#                 prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#                 account_id = prop and prop.id or False
#             inv_line.append((0, 0, {
#                 'name': line.product_id.name,
#                 'price_unit': line.price or line.product_id.lst_price,
#                 'account_id': account_id,
#                 'quantity': 1.0,
#                 'discount': 0.0,
#                 'uom_id': line.product_id.uom_id.id,
#                 'product_id': line.product_id.id,
#                 'account_analytic_id': False,
#             }))
#         #Manometry
#         for line in self.manometry_line:
#             if line.product_id.id:
#                 account_id = line.product_id.property_account_income_id.id
#             if not account_id:
#                 prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#                 account_id = prop and prop.id or False
#             inv_line.append((0, 0, {
#                 'name': line.product_id.name,
#                 'price_unit': line.price or line.product_id.lst_price,
#                 'account_id': account_id,
#                 'quantity': 1.0,
#                 'discount': 0.0,
#                 'uom_id': line.product_id.uom_id.id,
#                 'product_id': line.product_id.id,
#                 'account_analytic_id': False,
#             }))
#         #Endoscopy
#         for line in self.endoscopy_line:
#             if line.product_id.id:
#                 account_id = line.product_id.property_account_income_id.id
#             if not account_id:
#                 prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#                 account_id = prop and prop.id or False
#             inv_line.append((0, 0, {
#                 'name': line.product_id.name,
#                 'price_unit': line.price or line.product_id.lst_price,
#                 'account_id': account_id,
#                 'quantity': 1.0,
#                 'discount': 0.0,
#                 'uom_id': line.product_id.uom_id.id,
#                 'product_id': line.product_id.id,
#                 'account_analytic_id': False,
#             }))
#         #Other Service
#         for line in self.other_services_line:
#             if line.product_id.id:
#                 account_id = line.product_id.property_account_income_id.id
#             if not account_id:
#                 prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#                 account_id = prop and prop.id or False
#             inv_line.append((0, 0, {
#                 'name': line.product_id.name,
#                 'price_unit': line.price or line.product_id.lst_price,
#                 'account_id': account_id,
#                 'quantity': 1.0,
#                 'discount': 0.0,
#                 'uom_id': line.product_id.uom_id.id,
#                 'product_id': line.product_id.id,
#                 'account_analytic_id': False,
#             }))
#         res['invoice_line_ids'] = inv_line
#         invoice = inv_obj.create(res)
#         self.inv_invoice_id = invoice.id
#         self.state = 'to_x'
#         if not(self.pathology_line or self.radiology_line or self.manometry_line or self.endoscopy_line or self.other_services_line):
#             raise UserError(('No lines found iN Investigation'))



#     @api.multi
#     def view_inv_invoice(self):
#         invoice_ids = self.mapped('inv_invoice_id')
#         imd = self.env['ir.model.data']
#         action = imd.xmlid_to_object('account.action_invoice_tree1')
#         list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
#         form_view_id = imd.xmlid_to_res_id('account.invoice_form')

#         result = {
#             'name': action.name,
#             'help': action.help,
#             'type': action.type,
#             'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
#             'target': action.target,
#             'context': action.context,
#             'res_model': action.res_model,
#             'domain': [('partner_id', '=', self.patient_id.user_id.partner_id.id),('report_type','=','radiology'),('id','=',self.inv_invoice_id.id)],
#         }
#         if len(invoice_ids) > 1:
#             result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
#         elif len(invoice_ids) == 1:
#             result['views'] = [(form_view_id, 'form'), (list_view_id, 'tree')]
#             result['res_id'] = invoice_ids.ids[0]
#         else:
#             result = {'type': 'ir.actions.act_window_close'}
#         return result

#     @api.multi
#     def send_radiology(self):
#         investigation_obj = self.env['hms.investigation']
#         inv_ids = self.env['hms.investigation.radiology.line'].search([('appointment_id','=',self.id),('investigation_id','=',False)])
#         path_ids = self.env['hms.investigation.pathology.line'].search([('appointment_id','=',self.id),('investigation_id','=',False)])
#         mano_ids = self.env['hms.investigation.manometry.line'].search([('appointment_id','=',self.id),('investigation_id','=',False)])
#         endo_ids = self.env['hms.investigation.endoscopy.line'].search([('appointment_id','=',self.id),('investigation_id','=',False)])
#         oth_ids = self.env['hms.investigation.other_services.line'].search([('appointment_id','=',self.id),('investigation_id','=',False)])
#         radiology_line = []
#         if not ((self.radiology_line and inv_ids) or (self.pathology_line and path_ids) or (self.manometry_line and mano_ids) or (self.endoscopy_line and endo_ids)):
#             raise UserError(('No radiology or pathology or manometry or endoscopy or other services found for appointment.'))
#         radiology = None
#         if self.radiology_line:
#             self.cabin = 'zero'
#             for radio in self.radiology_line:
#                 price = radio.price
#                 foc =  radio.foc
#                 if not radio.investigation_id:
#                     if not radiology:
#                         radiology = investigation_obj.create({
#                             'patient_id': self.patient_id.id,
#                             'investigation_type': 'radiology',
#                             'appointment_id': self.id,
#                             'date_investigation': datetime.now(),
#                         })
#                     radio.write({'investigation_id': radiology.id,'price':price,'foc':foc})
#             self.state = 'to_x'
#             self.sequence = 5
#             #radiology and radiology.button_accepted_xray()
#         path_line = []
#         pathology = None
#         if self.pathology_line:
#             self.cabin = 'zero'
#             for path in self.pathology_line:
#                 price = path.price
#                 # foc =  path.foc
#                 if not path.investigation_id:
#                     if not pathology:
#                         pathology = investigation_obj.create({
#                             'patient_id': self.patient_id.id,
#                             'investigation_type': 'pathology',
#                             'appointment_id': self.id,
#                             'date_investigation': datetime.now(),
#                         })
#                     path.write({'investigation_id': pathology.id,'price':price})
#             self.state = 'to_x'
#             self.sequence = 5
#             #pathology and pathology.button_accepted_xray()
#         mano_line = []
#         manometry = None
#         if self.manometry_line:
#             self.cabin = 'zero'
#             for mano in self.manometry_line:
#                 price = mano.price
#                 # foc =  mano.foc
#                 if not mano.investigation_id:
#                     if not manometry:
#                         manometry = investigation_obj.create({
#                             'patient_id': self.patient_id.id,
#                             'investigation_type': 'manometry',
#                             'appointment_id': self.id,
#                             'date_investigation': datetime.now(),
#                         })
#                     mano.write({'investigation_id': manometry.id,'price':price})
#             self.state = 'to_x'
#             self.sequence = 5
#             #manometry and manometry.button_accepted_xray()
#         endo_line = []
#         endoscopy = None
#         if self.endoscopy_line:
#             self.cabin = 'zero'
#             for endo in self.endoscopy_line:
#                 price = endo.price
#                 # foc =  endo.foc
#                 if not endo.investigation_id:
#                     if not endoscopy:
#                         endoscopy = investigation_obj.create({
#                             'patient_id': self.patient_id.id,
#                             'investigation_type': 'endoscopy',
#                             'appointment_id': self.id,
#                             'date_investigation': datetime.now(),
#                         })
#                     endo.write({'investigation_id': endoscopy.id,'price':price})
#             self.state = 'to_x'
#             self.sequence = 5
#             #endoscopy and endoscopy.button_accepted_xray()
#         # oth_line = []
#         # os = None
#         # if self.other_services_line:
#         #     self.cabin = 'zero'
#         #     for oth in self.other_services_line:
#         #         price = oth.price
#         #         # foc =  oth.foc
#         #         if not oth.investigation_id:
#         #             if not os:
#         #                 os = investigation_obj.create({
#         #                     'patient_id': self.patient_id.id,
#         #                     'investigation_type': 'os',
#         #                     'appointment_id': self.id,
#         #                     'date_investigation': datetime.now(),
#         #                 })
#         #             oth.write({'investigation_id': os.id,'price':price})
#         #     self.state = 'to_x'
#         #     self.sequence = 5
#         #     os and os.button_accepted_xray()
#         return self.action_list_appointment()        


#     @api.multi
#     def send_sr_dr(self):
#         self.cabin = 'zero'
#         self.state = 'sr_dr'
#         self.sequence = 3
#         return self.action_list_appointment()

#     @api.multi
#     def send_f_x_ray(self):
#         self.sequence = 4
#         self.state = 'f_x'

#     @api.multi
#     def action_cancel(self):
#         self.state = 'cancel'
#         self.sequence = 12

#     @api.multi
#     def button_close_wo_saving(self):
#         self.cabin = 'zero'
#         return self.action_list_appointment()

#     @api.multi
#     def button_close_wo(self):
#         self.cabin = 'zero'
#         if self.prev_state == 'waiting' and self.state == 'in_consultation':
#             self.sequence = 1
#         if self.prev_state == 'to_x':
#             self.sequence = 5
#         if self.prev_state == 'f_x':
#             self.sequence = 4
#         if self.prev_state == 'sr_dr':
#             self.sequence = 3
#         self.date_end = False
#         self.state = self.prev_state
#         return self.action_list_appointment()

#     @api.one
#     def appointment_waiting(self):
#         res = super(Appointment, self).appointment_waiting()
#         if self.dressing:
#             self.state = 'dressing'
# #             self.date_end = datetime.now()
#             self.sequence = 10
#         return res

#     @api.multi
#     def action_amount_due_invoice(self):
#         domain = [
#             ('patient_id', '=', self.patient_id.id)
#         ]
#         invoice_ids = []
#         for appoint in self.search(domain):
#             if appoint.invoice_id and appoint.invoice_id.residual:
#                 invoice_ids.append(appoint.invoice_id.id)
#         return {
#             'name': _('Amount Due Invoices'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'account.invoice',
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', invoice_ids)],
#             'context': {'form_view_ref': 'account.invoice_form'},
#         }
# #Block Bill To Hospital Default Functionality Needed  13 Feb
#     # @api.multi
#     # def action_bill_to_hospital(self):
#     #     self.bill_to_hospital = not self.bill_to_hospital

#     @api.multi
#     def action_register_payments(self):
#         if self.invoice_id.state == "draft":
#             self.invoice_id.signal_workflow('invoice_open')
#         if self.invoice_id.state == 'open':
#             return {
#                 'name': _('OPD Register Payment'),
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'res_model': 'account.payment',
#                 'view_id': self.env.ref('account.view_account_payment_invoice_form').id,
#                 'type': 'ir.actions.act_window',
#                 'context': {'active_id': self.invoice_id.id, 'default_invoice_ids': [(4, self.invoice_id.id, None)]},
#                 'target': 'new'
#             }

#     @api.multi
#     def action_view_payments(self):
#         inv_ids = self.env['hms.investigation'].search([('appointment_id', '=', self.id)])
#         payments = []
#         for inv in inv_ids:
#             payments += inv.invoice_id.payment_ids.ids
#         if self.invoice_id.payment_ids:
#             payments += self.invoice_id.payment_ids.ids
#         return {
#             'name': _('Payment Receipts'),
#             'view_type': 'form',
#             'view_mode': 'tree',
#             'res_model': 'account.payment',
#             'view_id': self.env.ref('shah_opd.view_account_payment_tree').id,
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', payments)],
#             'context': {},
#             'target': 'new'
#         }

    

#     # @api.multi
#     # def action_investigation_register_payments(self):
#     #     inv_id = self.env['hms.investigation'].search([('appointment_id','=',self.id)], limit=1, order="id desc")
#     #     if inv_id.state == 'draft':
#     #         inv_id.button_accepted_xray()
#     #     if inv_id.invoice_id.state == 'draft':
#     #         inv_id.invoice_id.signal_workflow('invoice_open')
#     #     if inv_id.invoice_id.state == 'open':
#     #         return {
#     #             'name': _('Investigation Payment Receipts'),
#     #             'view_type': 'form',
#     #             'view_mode': 'form',
#     #             'res_model': 'account.payment',
#     #             'view_id': self.env.ref('account.view_account_payment_invoice_form').id,
#     #             'type': 'ir.actions.act_window',
#     #             'context': {'active_id': inv_id.invoice_id.id, 'default_invoice_ids': [(4, inv_id.invoice_id.id, None)]},
#     #             'target': 'new'
#     #         }

#     @api.multi
#     def print_prescription(self):
#         return self.env['report'].get_action(self, 'shah_opd.report_prescription_order_app')

    @api.model
    def action_open_s1_preview(self, values):
        ''' Open the website page with the preview results view '''
        if not self:
            raise ValidationError(('No Preview found!!.'))
        return {
            'type': 'ir.actions.act_url',
            'name': "Preview",
            'target': 'new',
            'url':  "appointment/past_investigation/%s" % slug(self)
        }

#     # @api.multi
#     # def show_inv_report(self):
#     #     record_url = "web/content/%s/%s/open_pdf/" % (self._model, str(self.id))
#     #     return {
#     #         'type': 'ir.actions.act_url',
#     #         'url': record_url,
#     #         'target': 'new',
#     #     }

# class PrescriptionLineWizard(models.Model):
#     _name = 'prescription.line.price'
#     _order = 'sequence'

    # product_id = fields.Many2one('product.product', 'Product', required=True, domain=[('hospital_product_type', '=', 'medicament')])
#     price = fields.Float(string="Charges")
    # days = fields.Char("Days")
    # quantity = fields.Integer('Quantity')
#     cost_per_unit = fields.Float(string="Cost unit")    
    # common_dosage = fields.Many2one('banas.hms.medication.dosage', string='Frequency', help='Drug form, such as tablet or gel')
#     appointment_id = fields.Many2one('hms.appointment','Appointment')
    # sequence = fields.Integer(default=10)

# class AccountPaymentHistory(models.Model):
#     _name = 'account.payment.history'

#     appointment_id = fields.Many2one('hms.appointment','Appointment')
#     patient_id = fields.Many2one('hms.patient','Patient')
#     date = fields.Datetime('Date')
#     total_consult = fields.Float('Total Consultation')
#     received_consult = fields.Float('Received Consultation')
#     total_xray = fields.Float('Total X-Ray')
#     received_xray = fields.Float('Received X-Ray')
#     total_physio = fields.Float('Total Physiotherapy')
#     received_physio = fields.Float('Received Physiotherapy')

# # class ProductProduct(models.Model):
# #     _inherit = 'product.product'
# #     
# # #     @api.model
# # #     def name_search(self, name, args=None, operator='ilike', limit=100):
# # #         args = args or []
# # #         recs = self.browse()
# # #         if not recs:
# # #             recs = self.search(['|',('name',operator,name),('patient_id.name', operator, name)] + args, limit=limit)
# # #         return recs.name_get()
# # 
# #     @api.model
# #     def name_search(self, name, args=None, operator='ilike', limit=100):
# #         args = args or []
# #         domain = []
# #         print "================name=======",name,self._context
# #         if self._context.has_key('prescription'):
# #             products = self.search([('department_ids.department_name','=','gastroenterology')])
# #             print "=========products============",products
# #             
# # #             domain = ['|', ('code', '=ilike', name + '%'), ('name', operator, name)]
# #         accounts = self.search(domain + args, limit=limit)
# #         return accounts.name_get()

class Investigation(models.Model):
    _inherit = 'hms.investigation'

    waiting_ids = fields.One2many('hms.investigation', compute="_get_waiting_list", string="Waiting")

    def _get_waiting_list(self):
        for invi in self:
            if invi.investigation_type == 'radiology':
                domain = [
                    ('investigation_type', '=', 'radiology'),
                    ('state', '!=', 'done'),
                    ('date_investigation', '>=', fields.Date.today()),
                    ('patient_id', '!=', invi.patient_id.id)]
                invi.waiting_ids = self.search(domain)

            else:
                domain = [
                    ('investigation_type', '=', 'pathology'),
                    ('state', '!=', 'done'),
                    ('date_investigation', '>=', fields.Date.today()),
                    ('patient_id', '!=', invi.patient_id.id)]
                invi.waiting_ids = self.search(domain)

#     @api.multi
#     def button_done(self):
#         res = super(Investigation, self).button_done()
#         if self.appointment_id:
#             self.sudo().appointment_id.state = 'f_x'

#     @api.multi
#     def button_done_foc(self):
#         res = super(Investigation, self).button_done_foc()
#         if self.appointment_id:
#             self.sudo().appointment_id.state = 'f_x'

#     # @api.multi
#     # def write(self, values):
#     #     res = super(Investigation, self).write(values)
#     #     for rec in self:
#     #         if rec.appointment_id and rec.multi_seq:
#     #             if rec.appointment_id.state == 'to_x':
#     #                 rec.sudo().appointment_id.state = 'f_x'
#     #     return res


class PatientBmi(models.Model):
    _name = 'banastech.hms.patient.bmi'

    patient_id = fields.Many2one('banastech.hms.patient', string="Patient")
    appointment_id = fields.Many2one('banastech.hms.appointment', string="Appointment")
    date = fields.Date('Date', default=fields.Date.today())
    weight = fields.Float('Weight(kg)')
    cm = fields.Float('Height(cm)', digits=(16,2))
    bmi = fields.Float('BMI', compute="_get_bmi", digits=(16,2), store=False)

    @api.depends('cm','weight')
    def _get_bmi(self):
        for rec in self:
            if rec.cm:
                rec.bmi = round((float(rec.weight) / ((float(rec.cm) / 100) ** 2)),2)


# class AbdominalExamination(models.Model):
#     _name = 'abdominal.examination'

#     name= fields.Char('Name')

class RectalExamination(models.Model):
    _name = 'rectal.examination'

    name = fields.Char('Name')

# # class ChiefComplain(models.Model):
# #     _name = 'chief.complain'

# #     name = fields.Char('Chief Complain')

# class AdvicesGroupLines(models.Model):
#     _name = 'advices.group.lines'
#     _rec_name = 'name'

#     name = fields.Char('Advices')
#     appointment_id = fields.Many2one('hms.appointment', 'Appointment')

# # Past Investigation Preview
class Session1Image(models.Model):
    _name = 'session1.image'

    name = fields.Char('Name')
    s_image1 = fields.Binary('Image', attachment=True)
    s_date1 = fields.Datetime(string="Date", default=fields.Datetime.now)
    appointment_id = fields.Many2one('banastech.hms.appointment')