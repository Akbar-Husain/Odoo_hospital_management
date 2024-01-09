import time
from datetime import datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class HMSAppointmentPurpose(models.Model):
    _name = 'banas.hms.appointment.purpose'
    _description = "HMS Appointment Purpose"

    name = fields.Char(string='Appointment Purpose', required=True)
    product_id = fields.Many2one('product.product', string="Product")


class HMSmedicalReason(models.Model):
    _name= "banas.hms.reason"
    _description = "HMS Medical History"

    name = fields.Char(string="Reason")


class HMSAppFinding(models.Model):
    _name = 'banastech.hms.appointment.finding'

    name = fields.Char('Name')


class HMSFinding(models.Model):
    _name = "banastech.hms.opd.finding"

    name = fields.Many2one('banastech.hms.appointment.finding', 'Name')
    description = fields.Char('Description')
    datetime = fields.Datetime('Date', default=fields.Datetime.now)
    appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment', ondelete='cascade')


class HMSAppointment(models.Model):
    _name = "banastech.hms.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HMS Appointment"
    _rec_name = 'name'

    @api.model
    def _get_service_id(self):
        return self.product_id.search([('hospital_product_type', '=', 'consultation')], limit=1).id

    @api.model
    def _get_reason_id(self):
        return self.env.ref("banastech_hms.reason_routine_follow")

    @api.model
    def _get_purpose_id(self):
        return self.env.ref("banastech_hms.purpose_consultation")

    @api.model
    def create(self, values):
        if values.get('name', 'New Appointment') == 'New Appointment':
            values['name'] = self.env['ir.sequence'].next_by_code('banastech.hms.appointment') or ''
        res = super(HMSAppointment, self).create(values)
        return res

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if self.doctor_id:
            return {
                'value': {
                    'department_id': self.doctor_id.department_ids.id
                    }
                }

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            return {
                'value': {
                    'doctor_id': self.department_id.doctor_ids.id
                    }
                }


    name = fields.Char(string='Appointment Id', default=lambda self: _('New Appointment'), readonly=True)
    patient_id = fields.Many2one('banastech.hms.patient', ondelete='restrict', string='Patient',required=True, help='Patient Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    image = fields.Binary(related='patient_id.image',string='Image', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    doctor_id = fields.Many2one('banas.hms.doctor', string='Doctor', help='Doctor\'s Name', required=True, states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    department_id = fields.Many2one('banas.hms.department', string='Department', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    no_invoice = fields.Boolean(string='Invoice Exempt', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True, states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    urine_reports = fields.Text(string='Urine Reports', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    s_creatinine = fields.Char(string='S.Creatinine', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    bi_sugar = fields.Char(string='BI.Sugar', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    cbc = fields.Char(string='CBC', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    blood_group = fields.Char(string='Blood Group', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    spsa = fields.Char(string='SPSA', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    electrolytes = fields.Char(string='Electrolytes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    others = fields.Char(string='Others', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    usg_abdomen_kub = fields.Char(string='USG Abdomen/KUB', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    x_ray_kub = fields.Char(string='X-Ray/KUB', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    # rgu = fields.Char(string='RGU')
    mcu = fields.Char(string='MCU', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    ct_scan = fields.Char(string='C.T. Scan', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    renal_scan = fields.Char(string='Renal Scan', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    bone_scan = fields.Char(string='Bone Scan', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    otherss = fields.Text(string='Others', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    reason_id = fields.Many2one("banas.hms.reason",ondelete='set null', string='Reason', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]}, default=_get_reason_id)
    follow_date = fields.Datetime(string="Follow Up Date", states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    weight = fields.Float(string='Weight', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    temp = fields.Char(string='Temp', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    hr = fields.Char(string='HR', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})

    rr = fields.Char(string='RR', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    bp = fields.Char(string='BP', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    spo2 = fields.Char(string='SpO2', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})

    differencial_diagnosis = fields.Text(string='Differencial Diagnosis', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    medical_advice = fields.Text(string='Medical Advice', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
#    #Below Fields Copy from Shah opd
    complain_ids = fields.Many2many('banas.hms.chief.complain','appointment_rel_complain','appointment_id','complain_ids' , string='Chief Complain')
    complain_ids_dummy = fields.Many2many('banas.hms.chief.complain','appointment_rel_complain_dummy','appointment_id','complain_ids' , string='Chief Complain')
    chief_complain = fields.Text(string='Chief Complaints', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    present_illness = fields.Text(string='History of Present Illness', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    notes = fields.Text(string='Notes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    rs = fields.Text(string='Respiratory Syncytial', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    cvs = fields.Text(string='C.V.S.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    cns = fields.Text(string='C.N.S', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    per_abdominal = fields.Text(string=' Per Abdominal', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    per_rectal = fields.Text(string='Per Rectal Examination', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    per_vaginal = fields.Text(string='Per Vaginal Examination', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    external_genitals = fields.Text(string='External Genitals', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    back_spine = fields.Text(string='Back Spine', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    peripheral_pulsation = fields.Text(string='Peripheral Pulsation', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    notess = fields.Text(string='Notes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    advice_notes = fields.Text(string='Notes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    # past_ho = fields.Text('Past H/O')
    associated_disease = fields.Many2one('banas.hms.diseases','Disease and Description"')
    associated_diseases = fields.One2many('banas.hms.associated.diseases','associated_diseases_id',string='Disease and Description')
    # post_medication = fields.Text('Past Medication')
    # previous_inv = fields.Text('Present Medication')
    # family_ho = fields.Text('Family H/O')
    past_history = fields.Text(string='Past History', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    # comments = fields.Text(string='Comments', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='cascade', copy=False)
    urgency = fields.Selection([
        ('a', 'Normal'),
        ('b', 'Urgent'),
        ('c', 'Medical Emergency'),
    ], string='Urgency Level', default='a', required=True, states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('waiting', 'Waiting'),
        ('in_consultation', 'In Consultation'),
        ('invoiced', 'Invoiced'),
        ('invoice_exempt', 'Invoice Exempt'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='State', default='draft', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    product_id = fields.Many2one('product.product', string='Consultation Service', help='Consultation Services', default=_get_service_id, states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    age =  fields.Char(related='patient_id.age', string='Age', readonly=True)
    gender =  fields.Selection(related='patient_id.gender', string='Gender', readonly=True)
    company_id = fields.Many2one('res.company', ondelete='restrict', string='Company',default=lambda self: self.env.user.company_id.id)
    duration = fields.Float(string='Duration', default=15.00, states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    # no_invoice = fields.Boolean('Invoice Exempt', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    consultation_type = fields.Selection([('consultation','Consultation'),('followup','Follow Up')],'Consultation Type', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    #Diseases
    medical_history = fields.Text(string="Past Medical History", states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    patient_diseases = fields.One2many('banas.hms.patient.disease', 'patient_id',  string='Diseases', help='Mark if the patient has died', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    # related='patient_id.patient_diseases'
    date_start = fields.Datetime(string='Waiting Start Date', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    date_end = fields.Datetime(string='Waiting end Date', states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    waiting_duration = fields.Char('Wait Time', compute="_time_count" ,readonly=True)
    purpose_id = fields.Many2one('banas.hms.appointment.purpose', string='Purpose', help="Appointment Purpose", default=_get_purpose_id, states={'cancel': [('readonly', True)], 'done': [('readonly', True)], 'confirm': [('readonly', True)], 'waiting': [('readonly', True)]})
    # days_1 = fields.Integer(string='Days', default=15,states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # weeks = fields.Integer(string='Weeks', default=0,states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # months = fields.Integer(string='Months', default=0,states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # area_id = fields.Many2one(related='patient_id.area_id',string='Area')
    sequence = fields.Integer(help='Used to order Appointment in tree view' ,default=10)
    state_id = fields.Many2one(related="patient_id.state_id", string="State")
    invoice_count = fields.Integer(string='Invoide Count', compute='_compute_invoice_count', track_visibility="onchange")
    presc_count = fields.Integer(string="Prescription Count", compute='_compute_prescription_count')


    def _compute_invoice_count(self):
        for rec in self:
            invoice_count = self.env['account.move'].sudo().search_count([('appointment_id', '=', rec.id)])
            rec.invoice_count = invoice_count

    def _compute_prescription_count(self):
        for rec in self:
            presc_count = self.env['prescription.order'].sudo().search_count([('appointment', '=', rec.id)])
            rec.presc_count = presc_count

    def view_prescription(self):
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'Prescriptions',
            'res_model' : 'prescription.order',
            'domain' : [('appointment','=',self.id)],
            'view_mode' : 'tree,form',
            'target' : 'current',
        }

    @api.onchange('complain_ids')
    def onchange_complain_ids(self):
        complain = (self.complain_ids - self.complain_ids_dummy)
        if complain and self.chief_complain:
            self.chief_complain += str("\n" + complain.name)
        elif complain and not self.chief_complain:
            self.chief_complain = complain.name
        self.complain_ids_dummy = self.complain_ids

    @api.model
    def _time_count(self):
        # pass
        for rec in self:
            # date_end = datetime.strptime(rec.date_end, '%Y-%m-%d %H:%M:%S') if rec.date_end else  datetime.now()
            date_end = rec.date_end if rec.date_end else datetime.now()
            if rec.date_start:
                datetime_diff = date_end - rec.date_start
                # datetime_diff = date_end - datetime.strptime(rec.date_start, '%Y-%m-%d %H:%M:%S')
                hrs = datetime_diff.seconds / 3600
                mins = datetime_diff.seconds % 3600 / 60
                if mins in range(1,10):
                    rec.waiting_duration = "%s:0%s" % (hrs, mins)
                else:
                    rec.waiting_duration = "%s:%s" % (hrs, mins)
                sec  = datetime_diff.seconds % 60
            else:
                rec.waiting_duration = "0:0"


    # @api.onchange('patient_id')
    # def onchange_patient_id(self):
    #     print('onchange.........................',self)
    #     self.ref = self.patient_id.ref

    @api.model
    def create_invoice(self):
        inv_obj = self.env['account.move']
        invoice = inv_obj.create({
            'partner_id': self.patient_id.partner_id.id,
            # 'partner_id': self.id,
            'l10n_in_gst_treatment': 'consumer',
            'ref': self.name,
            'appointment_id': self.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'name': self.product_id.name,
                'quantity': 1.0,
                'price_unit': self.product_id.lst_price,
                'tax_ids': self.product_id.taxes_id
                })],
        })
        self.invoice_id = invoice.id
        invoice.action_post()

    def view_invoice(self):
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'Invoices',
            'res_model' : 'account.move',
            'domain' : [('ref','=',self.name)],
            'view_mode' : 'tree,form',
            'target' : 'current',
        }


    def action_move_out_invoice_type(self):
        result = self.env.ref("account.action_move_out_invoice_type").read()[0]
        # if not invoices:
            # self.sudo()._read(['invoice_ids'])
            # invoices = self.invoice_ids

        # choose the view_mode accordingly
        # if len(invoices) = 1:
        ctx = eval(result.get("context",{}))
        self.create_invoice(self)
        ctx.update({
            "default_partner_id" : self.patient_id.partner_id.id,
            "default_l10n_in_gst_treatment": "consumer",
        })
        result.update({'context' : ctx})

        res = self.env.ref('account.view_move_form', False)
        form_view = [(res and res.id or False, 'form')]
        if 'views' in result:
            result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
        else:
            result['views'] = form_view
        if self.invoice_id:
            result['domain'] = [('id', '=', self.invoice_id.id)]
            result['res_id'] = self.invoice_id.id
        else:
            result = {'type': 'ir.actions.act_window_close'}

        return result


    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     print("args............",args)
    #     print("offset...........",offset)
    #     print("limit............",limit)
    #     print("order............",order)
    #     print("count............",count)
    #     args += [('patient_id.gender', '=', 'male')]
    #     return super().search(args)


    def appointment_cancle(self):
        self.state = 'cancel'

    def appointment_done(self):
        self.state = 'done'
        self.date_end = datetime.now()
        # return self.action_list_appointment()

    def appointment_confirm(self):
        self.state = 'confirm'
        inv_obj = self.env['banastech.hms.appointment']
        for rec in self:
            rec.create_invoice()

    def appointment_waiting(self):
        self.state = 'waiting'
        self.date_start = datetime.now()
        self.sequence = 1

    def appointment_consultation(self):
        self.state = 'in_consultation'
        self.date_end = datetime.now()
        self.sequence = 2

    def appointment_invoiced(self):
        self.state = 'invoiced'

    def appointment_draft(self):
        self.state = 'draft'



class HMSAssociatedDiseasess(models.Model):
    _name = 'banas.hms.associated.diseases'
    _description = 'HMS Associated Diseases'

    associated_diseases_name = fields.Many2one('banas.hms.diseases','Disease')
    associated_diseases_desc = fields.Char(string='Description')
    associated_diseases_id = fields.Many2one('banastech.hms.appointment','Disease')



class ChiefComplains(models.Model):
    _name = 'banas.hms.chief.complain'
    _description = 'Banastech HMS Chief Complains'

    name = fields.Char('Chief Complain')