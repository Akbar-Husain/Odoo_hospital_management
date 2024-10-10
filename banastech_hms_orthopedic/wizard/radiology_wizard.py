# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _

class RadiologyLineWizard(models.TransientModel):
    _name = 'investigation.radiology.line.wizard'
    
    plate = fields.Selection([('8x10', '08 x 10'), ('14x11', '14 x 11'), ('paper', 'Paper'), ('other', 'Other')], default="8x10")
    side = fields.Selection([('none', 'None'), ('right', 'Right'), ('left', 'Left'), ('both', 'Both')], default="none")
    product_id = fields.Many2one('product.product', 'Investigation Name', required=True, domain=[('hospital_product_type', '=', 'radiology')])
    price = fields.Float('Cost')
    instruction = fields.Char('Instruction')
    investigation_id = fields.Many2one('hms.investigation')
    wizard_id = fields.Many2one('investigation.radiology.wizard', 'Radiology wizard')

    



class RadiologyWizard(models.TransientModel):
    _name = 'investigation.radiology.wizard'

    appointment_id = fields.Many2one('hms.appointment', 'Appointment')
    radiology_wizard_line = fields.One2many('investigation.radiology.line.wizard', 'wizard_id', 'Radiology Wizard')
    
    @api.model
    def default_get(self,fields):
        res = super(RadiologyWizard, self).default_get(fields)        
        result1 = []
        res = {}
        context = self._context or {}
        record_id = context and context.get('active_id', False) or False
        apt_obj = self.env['hms.appointment']
        appointment = apt_obj.browse(record_id)
        for radiology in appointment.radiology_line:
            result1.append((0, 0, {'product_id': radiology.product_id.id, 'plate': radiology.plate,'side': radiology.side,
                            'price':radiology.price,'instruction':radiology.instruction,'investigation_id':radiology.investigation_id.id}))
        if 'radiology_wizard_line' in fields:
            res.update({'radiology_wizard_line': result1})
        return res

