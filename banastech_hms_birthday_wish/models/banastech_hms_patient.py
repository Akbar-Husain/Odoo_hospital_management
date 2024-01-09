# from odoo import api, fields, models, _
# from datetime import datetime, timedelta, time

# class IndimediPatient(models.Model):
#     _inherit = 'banastech.hms.patient'

#     @api.model
#     def send_birthday_email(self):
#         temp_obj = self.env['mail.template']
#         #group_obj = self.env['mail.group']
#         sms_obj = self.env['partner.sms.send']
#         wish_template_id = self.env['ir.model.data'].get_object_reference('banas_hms_birthday_wish', 'email_template_birthday_wish')[1]
#         group_id = self.env['ir.model.data'].get_object_reference('hms_birthday_wish', 'group_birthday')[1]
#         today = datetime.now()
#         today_month_day = '%-' + today.strftime('%m') + '-' + today.strftime('%d')
#         patient_ids = self.search([('dob', 'like', today_month_day)])
#         for patient_id in patient_ids:
#             #send SMS
#             if patient_id.mobile:
#                 message = _('Happy Birthday Dear %s.') % (patient_id.name)
#                 sms_id = sms_obj.create({
#                     'mobile_to': patient_id.mobile,
#                     'text': message,
#                 })
#                 sms_obj.sms_send([sms_id])

#                 # send Mail
#                 if patient_id.email:
#                     temp_obj.send_mail(patient_id.company_id.birthday_mail_template and patient_id.company_id.birthday_mail_template.id or wish_template_id,
#                                    patient_id.id, force_send=True)

#                 # post message in birthday wishes Group and on partner. 
#                 # group_obj.message_post(group_id, body=_('Happy Birthday Dear %s.') % (patient_id.name), partner_ids=[patient_id.id])
#                 # self.message_post(patient_id.id, body=_('Happy Birthday.'))