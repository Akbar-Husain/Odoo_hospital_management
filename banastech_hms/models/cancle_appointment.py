from datetime import datetime
from odoo import api, fields, models


class HMSCancleAppointment(models.Model):
    _name = "banas.hms.cancle.appointment"
    _description = "HMS Cancle Appointment"

    appointment_id = fields.Many2one('banastech.hms.appointment', string='Appointment')
    reason = fields.Text(string='Reason')

    def action_cancle_btn(self):
        for rec in self:
            rec.appointment_id.unlink()

    def cancle_btn(self):
        return