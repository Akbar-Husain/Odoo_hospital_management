from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError
# from urlparse import urljoin
# from odoo.addons.website.models.website import slug
from datetime import datetime
import os, sys
import base64  # file encode


# # class product_template(models.Model):
# #     _inherit = "product.template"

# #     hospital_product_type = fields.Selection(selection_add=[('manometry', 'Manometry'), ('endoscopy', 'Endoscopy')])

class DocumentManagement(models.Model):
    _inherit = "document.management"

    investigation_id = fields.Many2one('hms.investigation', string = 'Investigation Documents')
    investigation_type = fields.Selection(related = 'investigation_id.investigation_type', string = 'Type')
#     appointment_id = fields.Many2one('hms.appointment', string = 'Appointment Documents')
#     patient_id = fields.Many2one('hms.patient', string = 'Patient Documents')


class GroupLine(models.Model):
    _name = 'hms.investigation.group.line'

    product_id = fields.Many2one('product.product', 'Investigation Name', required = True)
    price = fields.Float('Cost')
    instruction = fields.Char('Instruction')
    group_id = fields.Many2one('hms.investigation.group')

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.price = self.product_id.lst_price
            self.instruction = self.product_id.description_sale
            # self.plate = self.product_id.plate
            # self.side = self.product_id.side

class InvestigationGroup(models.Model):
    _name = 'hms.investigation.group'

    name = fields.Char('Name')
    code = fields.Char('Code')
    investigation_type = fields.Selection([('pathology', 'Pathology'), ('radiology', 'Radiology'),('manometry', 'Manometry'), ('endoscopy', 'Endoscopy'), ('os', 'Other Services'),('all','Path+Rad+Mano+Endo+Oth')], string = 'Type')
    group_line = fields.One2many('hms.investigation.group.line', 'group_id', 'Line')

    _sql_constraints = [('name_uniq', 'unique(name)', 'The Unit name must be unique')]


class RadiologyLine(models.Model):
    _name = 'hms.investigation.radiology.line'

#     old_id = fields.Integer('Old ID')
    product_id = fields.Many2one('product.product', 'Investigation Name', domain = [('hospital_product_type', '=', 'radiology')])
    price = fields.Float('Cost')
#     inv_username = fields.Many2one('res.users', string="Prescribed By", default=lambda self: self.env.user, readonly="True")
    instruction = fields.Char('Instruction')
    investigation_id = fields.Many2one('hms.investigation')
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('invoiced', 'Invoiced'),
#         ('in_progress', 'In Progress'),
#         ('done', 'Done'),
#         ('cancel', 'Cancel'),
#         ], related = 'investigation_id.state', string = "State")
    palnofcare_id = fields.Many2one('inpatient.registration')

#     @api.onchange('product_id')
#     def onchange_product(self):
#         if self.product_id:
#             self.instruction = self.product_id.description_sale
#             self.side = self.product_id.side
#             self.price = self.product_id.lst_price
#             self.plate = self.product_id.plate

    @api.model
    def action_open_preview(self):
        ''' Open the website page with the preview results view '''
        if self.investigation_id:
            self.investigation_id.fetch_images()
        if self.investigation_id.doc_ids:
            return self.investigation_id.action_open_preview()


class PathologyLine(models.Model):
    _name = 'hms.investigation.pathology.line'

    product_id = fields.Many2one('product.product', 'Investigation Name', domain = [('hospital_product_type', '=', 'pathology')])
    price = fields.Float('Cost')
#     inv_username = fields.Many2one('res.users', string="Prescribed By", default=lambda self: self.env.user, readonly="True")
    instruction = fields.Char('Instruction')
    investigation_id = fields.Many2one('hms.investigation')
    palnofcare_id = fields.Many2one('inpatient.registration')

#     @api.onchange('product_id')
#     def onchange_product(self):
#         if self.product_id:
#             self.price = self.product_id.lst_price

    @api.model
    def action_open_preview(self, values):
        ''' Open the website page with the preview results view '''
        if self.investigation_id:
            self.investigation_id.fetch_images()
        if self.investigation_id.doc_ids:
            return self.investigation_id.action_open_preview()

# class RadiologyGroupLine(models.Model):
#     _name = 'hms.investigation.radiology.group.line'

#     product_id = fields.Many2one('product.product', 'Investigation Name', domain = [('hospital_product_type', '=', 'radiology')])
#     price = fields.Float('Cost')
#     instruction = fields.Char('Instruction')
#     investigation_id = fields.Many2one('hms.investigation')

#     @api.onchange('product_id')
#     def onchange_product(self):
#         if self.product_id:
#             self.price = self.product_id.lst_price            

class ManometryLine(models.Model):
    _name = 'hms.investigation.manometry.line'

    product_id = fields.Many2one('product.product', 'Investigation Name', domain = [('hospital_product_type', '=', 'manometry')])
    price = fields.Float('Cost')
#     inv_username = fields.Many2one('res.users', string="Prescribed By", default=lambda self: self.env.user, readonly="True")
    instruction = fields.Char('Instruction')
    investigation_id = fields.Many2one('hms.investigation')
    palnofcare_id = fields.Many2one('inpatient.registration')

#     @api.onchange('product_id')
#     def onchange_product(self):
#         if self.product_id:
#             self.price = self.product_id.lst_price

    @api.model
    def action_open_preview(self):
        ''' Open the website page with the preview results view '''
        if self.investigation_id:
            self.investigation_id.fetch_images()
        if self.investigation_id.doc_ids:
            return self.investigation_id.action_open_preview()

class EndoscopyLine(models.Model):
    _name = 'hms.investigation.endoscopy.line'

    product_id = fields.Many2one('product.product', 'Investigation Name', domain = [('hospital_product_type', '=', 'endoscopy')])
    price = fields.Float('Cost')
#     inv_username = fields.Many2one('res.users', string="Prescribed By", default=lambda self: self.env.user, readonly="True")
    instruction = fields.Char('Instruction')
    investigation_id = fields.Many2one('hms.investigation')
    palnofcare_id = fields.Many2one('inpatient.registration')

#     @api.onchange('product_id')
#     def onchange_product(self):
#         if self.product_id:
#             self.price = self.product_id.lst_price

    @api.model
    def action_open_preview(self):
        ''' Open the website page with the preview results view '''
        if self.investigation_id:
            self.investigation_id.fetch_images()
        if self.investigation_id.doc_ids:
            return self.investigation_id.action_open_preview()

class OtherServicesLine(models.Model):
    _name = 'hms.investigation.other_services.line'

    product_id = fields.Many2one('product.product', 'Investigation Name', domain = [('hospital_product_type', '=', 'os')])
    price = fields.Float('Cost')
#     inv_username = fields.Many2one('res.users', string="Prescribed By", default=lambda self: self.env.user, readonly="True")
    instruction = fields.Char('Instruction')
    investigation_id = fields.Many2one('hms.investigation')

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.price = self.product_id.lst_price

#     # @api.multi
#     # def action_open_preview(self):
#     #     ''' Open the website page with the preview results view '''
#     #     if self.investigation_id:
#     #         self.investigation_id.fetch_images()
#     #     if self.investigation_id.doc_ids:
#     #         return self.investigation_id.action_open_preview()         


class Investigation(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'hms.investigation'
    _order = "date_investigation desc"

    @api.model
    def _get_multi_upload_seq(self):
        return self.env['ir.sequence'].next_by_code('multi.upload')

    @api.depends('radiology_line.price','pathology_line.price','endoscopy_line.price','manometry_line.price','other_services_line.price')
    def _amount_all(self):
        """
        Compute the total amounts of the price.
        """
        for order in self:
            amount = 0.0
            if order.investigation_type=='radiology':
                for line in order.radiology_line:
                    amount += line.price
            if order.investigation_type=='pathology':
                for line in order.pathology_line:
                    amount += line.price
            if order.investigation_type=='endoscopy':
                for line in order.endoscopy_line:
                    amount += line.price
            if order.investigation_type=='manometry':
                for line in order.manometry_line:
                    amount += line.price
            if order.investigation_type=='os':
                for line in order.other_services_line:
                    amount += line.price
            order.update({
                'amount_total': amount,
            })

    binary = fields.Binary('Image')
    open_pdf = fields.Binary('Report File')
    binary_text = fields.Char('File Name')
    multi_seq = fields.Integer('Multi Seq', default = lambda self: self._get_multi_upload_seq())
#     old_id = fields.Integer('Old ID')
    name = fields.Char('Name', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    patient_id = fields.Many2one('banastech.hms.patient', string = 'Patient', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    gender = fields.Selection(related = 'patient_id.gender', string = 'Gender', readonly = True)
    age = fields.Char(related = 'patient_id.age', string = 'Age', readonly = True)
#     area_id = fields.Many2one(related = 'patient_id.area_id', string = 'Area', readonly = True)
#     state_id = fields.Many2one(related = 'patient_id.state_id', string = 'Area', readonly = True)
#     street = fields.Char(related = 'patient_id.street', string = 'Street', readonly = True)
#     street2 = fields.Char(related = 'patient_id.street2', string = 'Street2', readonly = True)
#     city_id = fields.Many2one(related = 'patient_id.city_id', string = 'City', readonly = True)
    doctor_id = fields.Many2one('banas.hms.doctor', string = 'Prescribing Doctor', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    date_investigation = fields.Datetime('Investigation Date', default = fields.Datetime.now, states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    ref_no = fields.Char('Ref. No')
#     appointment_id = fields.Many2one('hms.appointment', string = 'Appointment', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     opd_number = fields.Char(related="appointment_id.name",string="OPD No")
    notes = fields.Text(string = 'Notes', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        # ('invoiced', 'Invoiced'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ], string = 'State', readonly = True, default = 'draft')
    group_id = fields.Many2one('hms.investigation.group', 'Group', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    investigation_type = fields.Selection([('pathology', 'Pathology'), ('radiology', 'Radiology'),('manometry', 'Manometry'), ('endoscopy', 'Endoscopy'),('os', 'Other Services')], string = 'Type', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     investigation_type = fields.Selection([('pathology', 'Pathology'), ('radiology', 'Radiology'),('manometry', 'Manometry'), ('endoscopy', 'Endoscopy'),('advices_group', 'Advices')], string = 'Type', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    pathology_line = fields.One2many('hms.investigation.pathology.line', 'investigation_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     radiology_group_line = fields.One2many('hms.investigation.radiology.group.line', 'investigation_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    radiology_line = fields.One2many('hms.investigation.radiology.line', 'investigation_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    manometry_line = fields.One2many('hms.investigation.manometry.line', 'investigation_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    endoscopy_line = fields.One2many('hms.investigation.endoscopy.line', 'investigation_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    other_services_line = fields.One2many('hms.investigation.other_services.line', 'investigation_id', 'Investigation Line', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    invoice_id = fields.Many2one('account.move', string = 'Invoice', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    doc_ids = fields.One2many(comodel_name = 'document.management', inverse_name = 'investigation_id', string = 'Document', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     patho_doc_ids = fields.One2many(related = 'doc_ids', string = 'Pathology Files')
#     foc = fields.Boolean('FOC')
    hospitalization_id = fields.Many2one('inpatient.registration', string = 'Hospitalization')
#     ipd_number = fields.Char(related="hospitalization_id.name",string="IPD No")
    xray_path = fields.Char(string = 'Patient Records')
#     investigation_fee = fields.Char(compute = 'get_payment_status', string = 'Fees', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
#     invoice_state = fields.Selection(related = 'invoice_id.state', string = 'Invoice', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    image = fields.Binary(related = 'patient_id.image', string = 'Image', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    amount_total = fields.Float(string = 'Charges', store = True, compute = '_amount_all', readonly = True, track_visibility = 'always')


    _sql_constraints = [('name', 'UNIQUE(name)', 'Name must be unique!')]

    @api.model
    def create(self, values):
        values['binary'] = None
        values['name'] = self.env['ir.sequence'].next_by_code('investigation.code')
        res = super(Investigation, self).create(values)
        if res.multi_seq:
            document_ids = self.doc_ids.search([('multi_seq', '=', res.multi_seq)])
            document_ids.write({'investigation_id': res.id})
        return res

    # @api.model
    def write(self, values):
        values['binary'] = None
        res = super(Investigation, self).write(values)
        if self.multi_seq:
            document_ids = self.doc_ids.search([('multi_seq', '=', self.multi_seq)])
            document_ids.write({'investigation_id': self.id})
        return res

    @api.onchange('investigation_type')
    def onchange_investigation_type(self):
        return  {'domain': {'group_id': [('investigation_type', '=', self.investigation_type)]}}


    @api.onchange('group_id')
    def onchange_group_id(self):
        if self.investigation_type == 'pathology':
            line = []
            for grp in self.group_id.group_line:
                line.append((0, 0, {
                    'product_id' : grp.product_id.id,
                    'price' : grp.price,
                    'instruction' : grp.instruction,
            }))
            self.pathology_line = line
        if self.investigation_type == 'radiology':
            line = []
            for grp in self.group_id.group_line:
                line.append((0, 0, {
                    'product_id' : grp.product_id.id,
                    'price' : grp.price,
                    'instruction' : grp.instruction,
           }))
            self.radiology_line = line
        if self.investigation_type == 'endoscopy':
            line = []
            for grp in self.group_id.group_line:
                line.append((0, 0, {
                    'product_id' : grp.product_id.id,
                    'price' : grp.price,
                    'instruction' : grp.instruction,
            }))
            self.endoscopy_line = line
        if self.investigation_type == 'manometry':
            line = []
            for grp in self.group_id.group_line:
                line.append((0, 0, {
                    'product_id' : grp.product_id.id,
                    'price' : grp.price,
                    'instruction' : grp.instruction,
           }))
            self.manometry_line = line
        if self.investigation_type == 'os':
            line = []
            for grp in self.group_id.group_line:
                line.append((0, 0, {
                    'product_id' : grp.product_id.id,
                    'price' : grp.price,
                    'instruction' : grp.instruction,
           }))
            self.other_services_line = line

    # @api.model
    def button_cancel(self):
        self.state = 'cancel'

    # @api.model
    def button_done_foc(self):
        self.state = 'done'

    # @api.model
    def button_accepted_xray(self):
        self.sudo().state = 'in_progress'

    # @api.model
    def button_done(self):
        self.state = 'done'

#     @api.multi
#     def get_payment_status(self):
#         for investigation in self:
#             if not investigation.invoice_id:
#                 investigation.investigation_fee = '•'
#             elif investigation.invoice_id.state == 'paid':
#                 domain = [('account_id', '=', investigation.invoice_id.account_id.id), ('partner_id', '=', self.env['res.partner']._find_accounting_partner(investigation.invoice_id.partner_id).id), ('reconciled', '=', False), ('amount_residual', '!=', 0.0)]
#                 domain.extend([('credit', '>', 0), ('debit', '=', 0), ('id', 'in', investigation.invoice_id.payment_move_line_ids.ids)])
#                 lines = self.env['account.move.line'].search(domain)
#                 amount_to_show = 0
#                 for line in lines:
#                     amount_to_show = line.company_id.currency_id.with_context(date = line.date).compute(abs(line.amount_residual), investigation.invoice_id.currency_id)
#                 if amount_to_show == 0:
#                     investigation.investigation_fee = '✓'
#                 elif amount_to_show > 0:
#                     investigation.investigation_fee = '+'
#             elif investigation.invoice_id.state != 'paid':
#                 if investigation.invoice_id.residual < investigation.invoice_id.amount_total and investigation.invoice_id.residual != 0:
#                     investigation.investigation_fee = '−'
#                 else:
#                     investigation.investigation_fee = '✕'

#     @api.multi
#     def view_invoice(self):
#         invoice_ids = self.mapped('invoice_id')
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
#             'domain': [('partner_id', '=', self.patient_id.user_id.partner_id.id),('report_type','=','radiology'),('id','=',self.invoice_id.id)],
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
#     def action_open_preview(self):
#         ''' Open the website page with the preview results view '''
#         if not self:
#             raise ValidationError(('No Preview found.Please send to radiology!!.'))
#         for inv in self:
#             if inv.investigation_type != 'radiology':
#                 record_url = "web/content/%s/%s/open_pdf/" % (self._model, str(self.id))
#                 return {
#                     'type': 'ir.actions.act_url',
#                     'url': record_url,
#                     'target': 'new',
#                 }
#             self.env.context = dict(inv.env.context or {}, relative_url = True)
#             inv.fetch_images()
#             inv.doc_ids = self.env['document.management'].search([('investigation_id', '=', inv.id)])
#             return {
#                 'type': 'ir.actions.act_url',
#                 'name': "Preview",
#                 'target': 'new',
#                 'investigation_id':inv.id,
#                 'url':  "investigation/%s" % slug(inv)
#             }

    def unlink(self):
        for data in self:
            if data.state in ['done']:
                raise UserError(('You can not delete record in done state'))
        return super(Investigation, self).unlink()

    # @api.model
    def fetch_images(self):
        doc_obj = self.env['document.management']
        for invest in self:
            if invest.xray_path:
                for xray_path in str(invest.xray_path.decode('utf-8')).split(','):
                    if not os.path.isdir(xray_path):
                        raise UserError(('The given path is wrong or improper.'))
                    if self.investigation_type == 'radiology':
                        file_ext = ('.png', '.jpg', '.jpeg', 'gif')
                    else:
                        file_ext = ('.pdf')
                    for link in os.listdir(xray_path):
                        if link.lower().endswith(file_ext):
                            photo = base64.encodestring(open(os.path.join(xray_path, link)).read())
                            search = doc_obj.search([('name', '=', link), ('patient_id', '=', invest.patient_id.id)])
                            if not search:
                                values = {'is_document':photo, 'patient_id': invest.patient_id.id, 'name':link}
                                values.update({'investigation_id': invest.id})
                                doc_obj.create(values)


# class IndimediAppointment(models.Model):
#     _inherit = 'hms.appointment'

#     doc_ids = fields.One2many(comodel_name = 'document.management', inverse_name = 'appointment_id', string = 'Document')
#     old_inv = fields.Boolean(compute = 'get_old_investigation', string = 'Old Radiology?')

#     @api.multi
#     def button_investigation_view(self):
#         return {
#             'name': _('Investigation'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'hms.investigation',
#             'type': 'ir.actions.act_window',
#             'domain': [('appointment_id', '=', self.id)],
#             'context': {'default_patient_id': self.patient_id.id, 'default_doctor_id':self.physician_id.id, 'default_appointment_id': self.id, 'default_laboratory_id':False},
#         }

#     @api.multi
#     def get_old_investigation(self):
#         for appointment in self:
#             domain = [('patient_id', '=', appointment.patient_id.id), ('investigation_type', '=', 'radiology')]
#             if appointment.state != 'done':
#                 domain += '|', ('appointment_id', '!=', appointment.id), ('appointment_id', '=', False)
#             investigation_ids = self.env['hms.investigation'].search(domain)
#             if len(investigation_ids) > 0:
#                 appointment.old_inv = True
#             else:
#                 appointment.old_inv = False

#     @api.multi
#     def action_open_preview(self):
#         ''' Open the website page with the preview results view '''
#         self.env.context = dict(self.env.context or {}, relative_url = True)
#         base_url = self.env['ir.config_parameter'].get_param('web.base.url')
#         investigation_ids = self.env['hms.investigation'].search([('appointment_id', '=', self.id)])
#         return {
#             'type': 'ir.actions.act_url',
#             'name': "Preview",
#             'target': 'new',
#             'url': urljoin(base_url, "appointment/%s" % slug(self))
#         }

#     @api.multi
#     def action_open_preview_old(self):
#         ''' Open the website page with the preview results view '''
#         self.env.context = dict(self.env.context or {}, relative_url = True)
#         base_url = self.env['ir.config_parameter'].get_param('web.base.url')
#         investigation_ids = self.env['hms.investigation'].search([('appointment_id', '=', self.id)])
#         return {
#             'type': 'ir.actions.act_url',
#             'name': "Preview",
#             'target': 'new',
#             'url': urljoin(base_url, "/patient/appointment/%s" % slug(self))
#         }


# class IndimediPatient(models.Model):
#     _inherit = "hms.patient"

#     @api.multi
#     def _get_xray_path(self):
#         for patient in self:
#             investigation_ids = self.env['hms.investigation'].search([('patient_id', '=', patient.id)])
#             path = []
#             for inv in investigation_ids:
#                 # split path by , if multiple path exist.
#                 if inv.xray_path:
#                     inv_path = (inv.xray_path).split(',')
#                     for i_path in inv_path:
#                         # checking for path exist
#                         if i_path not in path:
#                             path.append(i_path)
#             # join path and assign to xray_path field
#             patient.xray_path = ",".join(path)

#     doc_ids = fields.One2many(comodel_name = 'document.management', inverse_name = 'patient_id', string = 'Document')
#     xray_path = fields.Char(compute = '_get_xray_path', string = 'X-Ray')

#     @api.multi
#     def action_open_preview(self):
#         ''' Open the website page with the preview results view '''
#         self.env.context = dict(self.env.context or {}, relative_url = True)
#         investigation_ids = self.env['hms.investigation'].search([('patient_id', '=', self.id)])
#         for invest in investigation_ids:
#             invest.fetch_images()
#         return {
#             'type': 'ir.actions.act_url',
#             'name': "Preview",
#             'target': 'new',
#             'url': "patient/%s" % slug(self)
#         }

#     @api.multi
#     def action_investigation_view(self):
#         return {
#             'name': _('Investigation'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'hms.investigation',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id', '=', self.id)],
#             'context': {'default_patient_id': self.id},
#         }

# class AppointmentAdviceGroup(models.Model):
#     _name = 'appointment.advice.group'

#     name = fields.Char('Name')
#     investigation_type = fields.Selection([('advices_group', 'Advices')],default="advices_group", string = 'Advices')
#     group_line = fields.One2many('appointment.advice.group.line', 'groups_id', 'Line')
#     _sql_constraints = [('name_uniq', 'unique(name)', 'The Unit name must be unique')]

# class AdviceGroupLine(models.Model):
#     _name = 'appointment.advice.group.line'

#     name = fields.Many2one('appointment.advice.group.line.name','Advice Name')
#     groups_id = fields.Many2one('appointment.advice.group')

# class AdviceGroupLineName(models.Model):
#     _name = 'appointment.advice.group.line.name'

#     name = fields.Char('Name')

class POCPathoRadio(models.Model):
    _inherit = 'inpatient.registration'

    poc_patho_line = fields.One2many('hms.investigation.pathology.line', 'palnofcare_id', string='Pathology')
    poc_radio_line = fields.One2many('hms.investigation.radiology.line', 'palnofcare_id', string='Radiology')
    poc_mano_line = fields.One2many('hms.investigation.manometry.line', 'palnofcare_id', string='Manometry')
    poc_endo_line = fields.One2many('hms.investigation.endoscopy.line', 'palnofcare_id', string='Endoscopy')