import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class BoxStatus(models.Model):
    _name='box.history'

    patient_id = fields.Many2one('res.partner', ondelete='cascade', string='Patient', domain=[('bone_bank_registered','=',True)])
    box_history_id = fields.Many2one('box.management', ondelete='restrict', string='Box Status')
    date_start = fields.Datetime('Date O/P')
    state = fields.Selection([('draft','Draft'),('receive','Received'),('donate','Donated'),('cancel','Cancel')], "State")

class BoxManagement(models.Model):
    _name = 'box.management'
    _rec_name ='box_code'

    box_code = fields.Char(size=10, string='Box ID', help='Box Identifier', default=lambda self: _(''), copy=False, readonly=True)
    history_allocation_ids = fields.One2many('box.history','box_history_id','Box Status')
    status = fields.Selection([('full','Full'),('empty','Empty')], "Box-Status")
    is_outside = fields.Boolean('Is Outside')
    location = fields.Char('Location')
    remark = fields.Text('Remark')

    @api.model
    def create(self, values):
        if values.get('box_code', '') == '':
            values['box_code'] = self.env['ir.sequence'].next_by_code('box.management') or ''
        return super(BoxManagement, self).create(values)

class BoneBankRegistration(models.Model):
    _inherit = 'res.partner'
    _description = 'Bank User'

#     #personal detail
    bone_bank_registered = fields.Boolean('Is Bone Bank User')
    is_receiver = fields.Boolean('Is Bone Receiver')
    is_donor = fields.Boolean('Is Bone Donor')
    code = fields.Char(size=256, string='Registration ID', help='Patient Identifier', copy=False)
#     biometric = fields.Char(size=256, string='Biometric ID')
    language = fields.Selection([('hindi', 'Hindi'),('english', 'English'),('gujarati', 'Gujarati')], String="Language", default='gujarati')
#     hepatitis = fields.Boolean('1.Have you suffered from Hepatitis (if so ,when and what type) \
#                                 or suffering from any liver disease?')
#     infection = fields.Boolean(string="2. Are you suffering from or have you suffered from any of a \
#                                  Serious infectious disease(e.g., Paratyphoid, Relapsing fever,\
#                                 Oseomyelitis or other)in the past?")
#     tuberculosis = fields.Boolean('3. Have you suffered from Tuberculosis?')
#     parkinson = fields.Boolean('4. Do you suffer from Parkinsons disease or other Nervous disorder?')
#     malignant = fields.Boolean('5. Are you suffering from or have you suffered from a Malignant tumor (cancer)?')
#     chronic = fields.Boolean('6. Are you suffering from or have suffered from chronic diseases such '
#                               'as Rheumatoid arthritis, Chronic renal conditions or other serious diseases?')
#     explant = fields.Boolean('7. Have you ever undergone any procedure in which Explants from other person \
#                              or animal were used (for ex-ample, eye surgery with cornea transplant, brain surgery \
#                             with transplanting the dura skin, heart valve surgery)?')
#     drugs = fields.Boolean('8. Are you taking any drugs (Corticosteroids, Immunosuppressive drugs) permanently?')
#     hormones = fields.Boolean('9. Have you ever been treated with human origin hormones?')
#     hemodialysis = fields.Boolean('10. Are you on regular hemodialysis?')
#     malaria = fields.Boolean('1. Have you been suffering from Malaria or typhoid fever in last one year')
#     febrile = fields.Boolean('2. Have you suffered from unclear febrile condition in last twelve months?')
#     rabies = fields.Boolean('3. Have you been vaccinated against rabies in past twelve months?')
#     transfusion =fields.Boolean('1. Have you taken Transfusion of blood or blood component in last six months?.')
#     tatto =fields.Boolean('2. Have you done any tattoo or acupuncture treatment or done piercing of skin in last \
#                               six months or have you been injured with any contaminated needle?')
#     vaccine =fields.Boolean('1.Have you been vaccinated against hepatits B vaccine in last three weeks?.')
#     gonorrheal =fields.Boolean('2.Have you suffered for gonorrheal/diarshocal disease in last four weeks?')
#     operation = fields.Boolean('3.Have you Undergone any small operation or tooth extraction in last week?')  
#     donation = fields.Boolean('Patient meets the criteria for donation?')
#     date_donation = fields.Datetime('Donation Date', default=fields.Datetime.now)
#     physician_id = fields.Many2one('hms.physician', string='Doctor')

#     @api.model
#     def register_patient(self):
#         for rec in self:
#             rec.bone_bank_registered = True
#             rec.code = self.env['ir.sequence'].next_by_code('bone.bank') or ''



class BoneDonor(models.Model):
    _name = 'bone.donor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(size=256, string='Sequence', copy=False, default=lambda self: _(''))
    patient_id = fields.Many2one('res.partner', ondelete='cascade', string='Patient', domain=[('bone_bank_registered','=',True),('is_donor','=',True)],)
    box_id = fields.Many2one('box.management', ondelete='restrict', string='Box', domain=[('status','=','empty')])
    state = fields.Selection([('draft','Draft'),('donate','Donated'),('cancel','Cancel')], default="draft", string="State")
    responsible_id = fields.Many2one('res.users', ondelete='restrict', string='Responsible', help="Responsible Person", default=lambda self: self.env.user)
    date_donation = fields.Datetime('Date', default=fields.Datetime.now)
    is_outside = fields.Boolean('Is Outside')
    location = fields.Char('Location')
    remark = fields.Text('Remark')

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('bone.donor') or ''
        return super(BoneDonor, self).create(values)

    def button_donate(self):
        self.state = 'donate'
        BoxHistory = self.env['box.history']
        for rec in self:
            if rec.location:
                self.box_id.location = rec.location
            BoxHistory.create({
                'patient_id':self.patient_id.id,
                'date_start':datetime.now(),
                'state':self.state,
                'box_history_id':self.box_id.id,
            })
            if rec.box_id:
                rec.box_id.status = 'full'

    def button_cancel(self):
        self.state = 'cancel'

class BoneReceiver(models.Model):
    _name = 'bone.receiver'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(size=256, string='Sequence', copy=False)
    patient_id = fields.Many2one('res.partner', ondelete='cascade', string='Patient', domain=[('bone_bank_registered','=',True),('is_receiver','=',True)])
    box_id = fields.Many2one('box.management', ondelete='restrict', string='Box', domain=[('status','=','full')])
    state = fields.Selection([('draft','Draft'),('receive','Received'),('cancel','Cancel')], default="draft", string="State")
    responsible_id = fields.Many2one('res.users', ondelete='restrict', string='Responsible', help="Responsible Person", default=lambda self: self.env.user)
    date_receiver = fields.Datetime('Date', default=fields.Datetime.now)
    is_outside = fields.Boolean('Is Outside')
    location = fields.Char('Location')
    remark = fields.Text('Remark')

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('bone.receiver') or ''
        return super(BoneReceiver, self).create(values)

    def button_receive(self):
        self.state = 'receive'
        BoxHistory = self.env['box.history']
        for rec in self:
            if rec.location:
                self.box_id.location = rec.location
            BoxHistory.create({
                'patient_id':self.patient_id.id,
                'date_start':datetime.now(),
                'state':self.state,
                'box_history_id': self.box_id.id,
            })
            if rec.box_id:
                rec.box_id.status = 'empty'

    def button_cancel(self):
        self.state = 'cancel'