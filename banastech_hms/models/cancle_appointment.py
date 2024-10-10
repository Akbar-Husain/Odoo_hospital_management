from datetime import datetime
from odoo import api, fields, models
from odoo.addons.base.models.res_users import check_identity


class HMSCancleAppointment(models.TransientModel):
    _name = "banas.hms.cancle.appointment"
    _description = "HMS Cancle Appointment"

    appointment_id = fields.Many2one('banastech.hms.appointment', string='Appointment')
    reason = fields.Text(string='Reason')

    @check_identity
    def action_cancle_btn(self):
        active_id = self._context.get('active_id')
        appointment = self.env['banastech.hms.appointment'].browse(active_id)

        self.env['cancle.appointment.history'].create({
            'appointment_id': appointment.id,
            'cancellation_reason': self.reason,
            'cancellation_date': fields.Datetime.now(),
        })
        for rec in self:
            rec.appointment_id.unlink()

    def cancle_btn(self):
        return




class HMSCancleAppointmentHistory(models.Model):
    _name = "cancle.appointment.history"
    _description = "Cancle Appointment History"

    appointment_id = fields.Many2one('banastech.hms.appointment', string='Cancelled Appointment', required=True)
    cancellation_reason = fields.Text('Cancellation Reason', required=True)
    cancellation_date = fields.Datetime('Cancellation Date', required=True)