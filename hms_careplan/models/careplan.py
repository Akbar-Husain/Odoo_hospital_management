from odoo import api, fields, models
from datetime import datetime ,date ,timedelta

class CareplanIpFluid(models.Model):
    _name = 'careplan.ip.fluid'

    fluid_id = fields.Many2one('careplan.detail', string="Ip Fluid")
    # ips_id = fields.Many2one('ips.fluid',string='I/V Fluids')
    rate = fields.Char(string='Rate')
    quantity = fields.Char(string='Quantity')

class CareplanVital(models.Model):
    _name="careplan.vital"

    vital_id = fields.Many2one('careplan.detail', string="Vitals")
    pulse = fields.Char(string="Pulse")
    bp = fields.Char(string="Blood Pressure")
    temperature = fields.Char(string="Temperature °C",default="0.0°C")
    time = fields.Char(string="Time",default=lambda *a: (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M"))

class CareplanLiquidMonitoring(models.Model):
    _name ='careplan.liquid.monitoring'

    @api.onchange('by_mouth','by_drip')
    def on_total_liquid(self):
        self.total = float(self.by_mouth) + float(self.by_drip)

    @api.onchange('urine')
    def on_difference_liquid(self):
        self.difference = float(self.total) - float(self.urine)

    liquid_id = fields.Many2one('careplan.detail', string="Liquid Monitoring")
    day = fields.Selection([('1','Day 1'),('2','Day 2'),('3','Day 3'),('4','Day 4'),('5','Day 5'),('6','Day 6'),('7','Day 7'),('8','Day 8'),('9','Day 9'),('10','Day 10')], string='Days')
    by_mouth = fields.Integer(string="By Mouth(ml)")
    by_drip = fields.Integer(string="By Drip(ml)")
    total = fields.Integer(string="Total(ml)",readonly="True")
    urine = fields.Integer(string="Urine(ml)")
    difference = fields.Integer(string="Difference(ml)", readonly="True")

class CareplanAntibioticAnalogesis(models.Model):
    _name = "careplan.antibiotic.analogesis"

    antibiotic_id = fields.Many2one('careplan.detail', string="Antibiotic N Analogesis")
    product_id = fields.Many2one('product.product', string='Antibiotic & Analgesics', required=True)
    sos = fields.Boolean(string="SOS")
    t1 = fields.Integer(string="T1")
    b1 = fields.Boolean(string="C1")
    time1 = fields.Char(string="Time")
    t2 = fields.Integer(string="T2")
    b2 = fields.Boolean(string="C2")
    time2 = fields.Char(string="Time")
    t3 = fields.Integer(string="T3")
    b3 = fields.Boolean(string="C3")
    time3 = fields.Char(string="Time")
    t4 = fields.Integer(string="T4")
    b4 = fields.Boolean(string="C4")
    time4 = fields.Char(string="Time")

    @api.model
    @api.constrains('t1', 't2', 't3', 't4')
    def _check_my_field(self):
        if (self.t1 < 0 or self.t1 > 24) or (self.t2 < 0 or self.t2 > 24) or (self.t3 < 0 or self.t3 > 24) or (self.t4 < 0 or self.t4 > 24):
            raise ValidationError(_("Enter Value Of Time Between  0 to 24 hrs"))

    @api.onchange('b1')
    def onchange_b1(self):
        if self.b1:
            self.time1 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b2')
    def onchange_b2(self):
        if self.b2:
            self.time2 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b3')
    def onchange_b3(self):
        if self.b3:
            self.time3 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b4')
    def onchange_b4(self):
        if self.b4:
           self.time4 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

class CareplanInstructionSet(models.Model):
    _name = "careplan.miscellaneous.drugs"

    miscellaneous_id = fields.Many2one('careplan.detail', string="Instruction")
    product_id = fields.Many2one('product.product', string='Miscellaneous Drugs', required=True)
    sos = fields.Boolean(string="SOS")
    t5 = fields.Integer(string="T1")
    b5 = fields.Boolean(string="C1")
    time5 = fields.Char(string="Time")
    t6 = fields.Integer(string="T2")
    b6 = fields.Boolean(string="C2")
    time6 = fields.Char(string="Time")
    t7 = fields.Integer(string="T3")
    b7 = fields.Boolean(string="C3")
    time7 = fields.Char(string="Time")
    t8 = fields.Integer(string="T4")
    b8 = fields.Boolean(string="C4")
    time8 = fields.Char(string="Time")
    
    @api.model
    @api.constrains('t5', 't6', 't7', 't8', 't9')
    def _check_my_field2(self):
        if (self.t5 < 0 or self.t5 > 24) or (self.t6 < 0 or self.t6 > 24) or (self.t7 < 0 or self.t7 > 24) or (self.t8 < 0 or self.t8 > 24):
            raise ValidationError(_("Enter Value Of Time Between  0 to 24 hrs"))

    @api.onchange('b5')
    def onchange_b5(self):
        if self.b5:
            self.time5 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b6')
    def onchange_b6(self):
        if self.b6:
            self.time6 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b7')
    def onchange_b7(self):
        if self.b7:
            self.time7 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b8')
    def onchange_b8(self):
        if self.b8:
            self.time8 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

class CareplanInstructionSet(models.Model):
    _name = "careplan.instruction.set"

    instruction_id = fields.Many2one('careplan.detail', string="Instruction")
    # instruction_list_id = fields.Many2one('instruction.list', string='Instruction')
    instruction_done = fields.Boolean(string="Done",default=False)
    instruction_time_ins = fields.Char(string="Time", readonly=True)
    
    @api.onchange('instruction_done')
    def onchange_done(self):
        if self.instruction_done:
            self.instruction_time_ins = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

class CareplanDetail(models.Model):
    _name = 'careplan.detail'

    @api.onchange('date_careplan')
    def onchange_date(self):
        if self.date_careplan:
            self.day_careplan = datetime.strptime(self.date_careplan,"%Y-%m-%d").strftime("%A")

    careplan_id = fields.Many2one('inpatient.registration', string="Careplan")
    nurse_id = fields.Many2one('res.users', string='Primary Nurse', help='Anesthetist data of the patient', required="True",domain=[('is_nurse','=',True)])
    date_careplan = fields.Datetime('Date', required="True")
    day_careplan = fields.Char('Day', readonly="True")
    complaint_patient = fields.Text(string="Patient Complaint")
    ci_ids = fields.One2many('careplan.instruction.set', 'instruction_id', string="Instruction")
    cm_ids = fields.One2many('careplan.miscellaneous.drugs','miscellaneous_id',string='Miscellaneous Drugs')    
    antibiotic_ids = fields.One2many('careplan.antibiotic.analogesis','antibiotic_id',string='Antibiotic & Analgesics')
    liquid_ids = fields.One2many('careplan.liquid.monitoring', 'liquid_id', string='Liquid Monitoring')
    vital_ids = fields.One2many('careplan.vital', 'vital_id', 'Vitals')
    fluid_ids = fields.One2many('careplan.ip.fluid', 'fluid_id', 'Fluid')

class IndimediCareplan(models.Model):
    _inherit = "inpatient.registration"

    careplan_ids = fields.One2many('careplan.detail', 'careplan_id', string="Careplan")