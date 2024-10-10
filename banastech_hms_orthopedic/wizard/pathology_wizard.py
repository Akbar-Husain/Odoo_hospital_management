# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _

class PathologyLineWizard(models.TransientModel):
    _name = 'investigation.pathology.line.wizard'
    
    product_id = fields.Many2one('product.product', 'Investigation Name', required=True, domain=[('hospital_product_type', '=', 'pathology')])
    price = fields.Float('Cost')
    instruction = fields.Char('Instruction')
    investigation_id = fields.Many2one('hms.investigation')
    wizard_id = fields.Many2one('investigation.pathology.wizard', 'Pathology wizard')


class PathologyWizard(models.TransientModel):
    _name = 'investigation.pathology.wizard'

    appointment_id = fields.Many2one('hms.appointment', 'Appointment')
    pathology_wizard_line = fields.One2many('investigation.pathology.line.wizard', 'wizard_id', 'Pathology Wizard')
    
    @api.model
    def default_get(self,fields):
        res = super(PathologyWizard, self).default_get(fields)        
        result1 = []
        res = {}
        context = self._context or {}
        record_id = context and context.get('active_id', False) or False
        apt_obj = self.env['hms.appointment']
        appointment = apt_obj.browse(record_id)
        for pathology in appointment.pathology_line:
            result1.append((0, 0, {'product_id': pathology.product_id.id, 'price':pathology.price,'instruction':pathology.instruction,'investigation_id':pathology.investigation_id.id}))
        if 'pathology_wizard_line' in fields:
            res.update({'pathology_wizard_line': result1})
        return res