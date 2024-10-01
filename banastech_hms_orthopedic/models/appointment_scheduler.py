import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import dateutil.relativedelta
import random

class AppointmentScheduler(models.Model):
    _inherit='banastech.hms.appointment'

    @api.model
    def create_appointment(self):
        appointment_ids = self.search([
            ('department_name', '=', 'Orthopedic'),
            ('date', '>=', datetime.now().strftime('%Y-%m-%d')),
            ('date', '<', (datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d')),
            ('state', '=', 'done')])
        if appointment_ids:
            for data in appointment_ids:
                print("=====================data",data)
                if data.days_1 or data.weeks or data.months:
                    t= self.create({
                        'patient_id' : data.patient_id.id,
                        'doctor_id' : data.doctor_id.id,
                        # 'date': data.follow_date,
                        # 'purpose_id': data.reason_id.id or False,
                        # 'consultation_type':'followup',
                        'hypersensitive':data.hypersensitive,
                        'follow_foc':data.follow_foc,
                        'opd_foc':data.opd_foc,
                        # 'radilogy_date':data.follow_date
                        })
                    print("=============t",t)