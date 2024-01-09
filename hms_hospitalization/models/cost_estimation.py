from odoo import api, fields, models, _
import datetime

class CostEstimation(models.Model):
    _name = 'cost.estimation'

    @api.model
    def _default_room_estimation(self):
        vals = []
        estimation = self.env['room.facility.charges'].search([])
        for room in estimation:
            vals.append((0, 0, {
                'name': room.name,
            }))
        return vals

    @api.model
    def _default_surgical_estimation(self):
        vals = []
        estimation = self.env['surgical.charges'].search([])
        for surgical in estimation:
            vals.append((0, 0, {
                'name': surgical.name,
            }))
        return vals

    @api.model
    def _default_operation_estimation(self):
        vals = []
        estimation = self.env['operation.equip.charges'].search([])
        for operation in estimation:
            vals.append((0, 0, {
                'name': operation.name,
            }))
        return vals

    @api.model
    def _default_investigation_estimation(self):
        vals = []
        estimation = self.env['investigation.pharmacy.charges'].search([])
        for investigation in estimation:
            vals.append((0, 0, {
                'name': investigation.name,
            }))
        return vals

    @api.model
    def create(self, values):
        if values.get('name', 'New Estimation') == 'New Estimation':
            values['name'] = self.env['ir.sequence'].next_by_code('cost.estimation') or 'New'
        res = super(CostEstimation, self).create(values)
        return res

    name = fields.Char("Name", default=lambda self: _('New Estimation'))
    patient_id = fields.Many2one('banastech.hms.patient', string="Patient", required=True)
    consultant_id = fields.Many2one('banas.hms.doctor', string='Consultant')
    surgery_procedure = fields.Char(string='Surgery/Unplanned')
    case_type = fields.Selection([('planned', 'Planned'),('unplanned', 'Unplanned')], string='Case Type')
    surgery_grade = fields.Char('Surgery Grade')
    estimate_date = fields.Datetime('Date', default=fields.Datetime.now)
    room_category = fields.Char('Room Category')
    estimate_day = fields.Char(string='No of Days')
    package = fields.Selection([('yes', 'Yes'),('no', 'No')], string='Package')
    room_facility_charges_ids = fields.One2many('room.facility.charges','room_facility_charges_id','Room Facility Charge',default=lambda self: self._default_room_estimation())
    surgical_charges_ids = fields.One2many('surgical.charges','surgical_charges_id','Surgical Charge',default=lambda self: self._default_surgical_estimation())
    operation_equip_charges_ids = fields.One2many('operation.equip.charges','operation_equip_charges_id','Operation Equip Charge',default=lambda self: self._default_operation_estimation())
    investigation_pharmacy_charges_ids = fields.One2many('investigation.pharmacy.charges','investigation_pharmacy_charges_id','Investigation & Pharmacy Charges',default=lambda self: self._default_investigation_estimation())
    hospitalization_id = fields.Many2one('inpatient.registration', string = 'Hospitalization')
    appointment_id = fields.Many2one('banastech.hms.appointment', string="Appointment")
    admission_deposit = fields.Integer(string="Admission Deposit")
    ot_clear_amount = fields.Integer(string="OT Clearance Amount")
    executive_id = fields.Many2one('banas.hms.doctor', string="Executive")
    patient_relative = fields.Char(string="Patient/Relative Name")

class RoomFacilityCharges(models.Model):
    _name = 'room.facility.charges'

    name = fields.Char('Particulars')
    room_type = fields.Selection([('general', 'General'),
        ('semi_spaecial', 'Semi-Special'),
        ('deluxe', 'Deluxe'),
        ('super_deluxe', 'Super Deluxe'),
        ('suite', 'Suite'),
        ('sharing', 'Sharing'),
        ('icu', 'ICU'),
        ('dialysis', 'Dialysis'),
        ('recovery_room', 'Recovery Room'),
    ], string='Room Type',default='general')
    stay_day = fields.Float('Days')
    room_charges = fields.Float('Charges')
    room_total_amount = fields.Float('Total Amount')
    room_facility_charges_id = fields.Many2one('cost.estimation','Cost Estimaion')

    @api.onchange('stay_day','room_charges')
    def on_room_chanrges(self):
       self.room_total_amount = float(self.stay_day) * float(self.room_charges)


class SurgicalCharges(models.Model):
    _name = 'surgical.charges'

    name = fields.Char('Particulars')
    risk_type = fields.Selection([('high_risk', 'High Risk'),('complicated', 'Complicated'),('emergency','Emeergency')], string='Risk Factor')
    room_type = fields.Selection([('general', 'General'),('semi_spaecial', 'Semi-Special'),('deluxe', 'Deluxe'),('super_deluxe', 'Super Deluxe'),('suite', 'Suite'),
        ('sharing', 'Sharing'),('icu', 'ICU'),('dialysis', 'Dialysis'),('recovery_room', 'Recovery Room'),], string='Room Type',default='general')
    stay_day = fields.Float('Days')
    room_charges = fields.Float('Charges')
    room_total_amount = fields.Float('Total Amount')
    surgical_charges_id = fields.Many2one('cost.estimation','Cost Estimaion')


class OperationEquipCharges(models.Model):
    _name = 'operation.equip.charges'

    name = fields.Char('Particulars')
    room_type = fields.Selection([('general', 'General'),('semi_spaecial', 'Semi-Special'),('deluxe', 'Deluxe'),('super_deluxe', 'Super Deluxe'),('suite', 'Suite'),
        ('sharing', 'Sharing'),('icu', 'ICU'),('dialysis', 'Dialysis'),('recovery_room', 'Recovery Room'),], string='Room Type',default='general')
    stay_day = fields.Float('/Hr & /Mins')
    room_charges = fields.Float('Charges')
    room_total_amount = fields.Float('Total Amount')
    operation_equip_charges_id = fields.Many2one('cost.estimation','Cost Estimaion')

    @api.onchange('stay_day','room_charges')
    def on_operation_chanrges(self):
       self.room_total_amount = float(self.stay_day) * float(self.room_charges)


class InvestigationPharmacyCharges(models.Model):
    _name = 'investigation.pharmacy.charges'

    name = fields.Char('Particulars')
    room_type = fields.Selection([('general', 'General'),('semi_spaecial', 'Semi-Special'),('deluxe', 'Deluxe'),('super_deluxe', 'Super Deluxe'),('suite', 'Suite'),
        ('sharing', 'Sharing'),('icu', 'ICU'),('dialysis', 'Dialysis'),('recovery_room', 'Recovery Room'),], string='Room Type',default='general')
    stay_day = fields.Float('Days')
    room_charges = fields.Float('Charges')
    investigation_pharmacy_charges_id = fields.Many2one('cost.estimation','Cost Estimaion')