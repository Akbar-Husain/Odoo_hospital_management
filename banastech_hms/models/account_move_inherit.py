from odoo import api, fields, models, _
import time

class AccountMove(models.Model):
    _inherit = 'account.move'

    appointment_id = fields.Many2one('banastech.hms.appointment', string='Appointment', readonly=True)

    def default_appointment_id(self):
        return appointment_id