from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError

class CertificateManagement(models.Model):
    _name = 'certificate.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Certificate Management'

    name = fields.Char(size=256, string='Sequence',required=True, readonly=True, default=lambda self: _('NEW'), copy=False)
    patient_id = fields.Many2one('banastech.hms.patient',string='Patient', ondelete="restrict", help="Patient whose certificate to be attached")
    doctor_id = fields.Many2one('banas.hms.doctor',string='Doctor', ondelete="restrict", help="Doctor in consultant with the patient")
    date_attachment = fields.Date('Date', readonly="True", default=fields.Datetime.now)
    certificate_content = fields.Text('Certificate Content')
    state = fields.Selection([('draft','Draft'),('done','Done')], 'Status', default="draft", track_visibility='onchange') 
    template_id = fields.Many2one('certificate.template', string="Certificate Template", ondelete="cascade")

    def action_done(self, values):
        self.state = 'done'

    @api.model
    def create(self, values):
        if values.get('name', _('NEW')) == 'NEW':
            values['name'] = self.env['ir.sequence'].next_by_code('certificate.management')
        res = super(CertificateManagement, self).create(values)
        return res

    @api.onchange('template_id')
    def onchange_template(self):
        self.certificate_content = self.template_id.certificate_content

    @api.model
    def unlink(self, values):
        for data in self:
            if data.state in ['done']:
                raise UserError(_('You can only delete in draft'))
        return super(CertificateManagement, self).unlink()

class CertificateTemplate(models.Model):
    _name = 'certificate.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Certificate Template'

    name = fields.Char("Template")
    certificate_content = fields.Text('Certificate Content')

class HMSPatient(models.Model):
    _inherit = 'banastech.hms.patient'

    @api.model
    def action_open_certificate(self, values):
        return {
            'type': 'ir.actions.act_window',
            'name': ('Certificate'),
            'res_model': 'certificate.management',
            'view_mode': 'tree,form',
            'domain': [('patient_id','=',self.id)],
            'target' : 'current',
        }