# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _

class PrescriptionLineWizard(models.TransientModel):
    _name = 'prescription.line.wizard'
    
    product_id = fields.Many2one('product.product', 'Product', required=True, domain=[('hospital_product_type', '=', 'medicament')])
    price = fields.Float(string="Charges")
    days = fields.Char("Days")
    quantity = fields.Integer('Quantity')
    cost_per_unit = fields.Float(string="Cost unit")
    common_dosage = fields.Many2one('banas.hms.medication.dosage', string='Frequency', help='Drug form, such as tablet or gel')
    wizard_id = fields.Many2one('prescription.wizard', 'Prescription wizard')


class PrescriptionWizard(models.TransientModel):
    _name = 'prescription.wizard'

    appointment_id = fields.Many2one('banastech.hms.appointment', 'Appointment')
    prescription_wizard_line = fields.One2many('prescription.line.wizard', 'wizard_id', 'Prescription Wizard')

    # @api.model
    # def default_get(self,fields):
    #     res = super(PrescriptionWizard, self).default_get(fields)
    #     result1 = []
    #     res = {}
    #     context = self._context or {}
    #     record_id = context and context.get('active_id', False) or False
    #     apt_obj = self.env['hms.appointment']
    #     appointment = apt_obj.browse(record_id)
    #     for prescription in appointment.prescription_line:
    #         if prescription.product_id.product_exception=='yes':
    #             qty = prescription.product_id.no_per_pack
    #             price = prescription.product_id.list_price
    #         else:
    #             qty = prescription.quantity
    #             price = prescription.product_id.list_price * qty
    #         result1.append((0, 0, {'product_id': prescription.product_id.id,
    #                                'price':prescription.product_id.list_price,
    #                                'common_dosage':prescription.common_dosage.id,
    #                                'days':prescription.days,
    #                                'quantity':qty,
    #                                'cost_per_unit': price
    #                                }))
    #     if 'prescription_wizard_line' in fields:
    #         res.update({'prescription_wizard_line': result1})
    #     return res