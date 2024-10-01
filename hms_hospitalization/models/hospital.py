from odoo import api, fields, models
from odoo.tools.translate import _


class HMSBed(models.Model):
    _name = 'banastech.hms.bed'

    name = fields.Char(string='Name', required=True, copy=False)
    product_id = fields.Many2one('product.product', ondelete='cascade', string='Bed Product', domain=[('hospital_product_type', '=', 'bed')], context={'default_hospital_product_type': 'bed'})
    bed_type = fields.Selection([
        ('gatch', 'Gatch Bed'),
        ('electric', 'Electric'),
        ('stretcher', 'Stretcher'),
        ('low', 'Low Bed'),
        ('low_air_loss', 'Low Air Loss'),
        ('circo_electric', 'Circo Electric'),
        ('clinitron', 'Clinitron')], string='Type', required=True)
    telephone = fields.Char(size=14, string='Telephone')
    state = fields.Selection([
        ('free', 'Free'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied')], string='Status')
    ward_id = fields.Many2one('banastech.hms.ward', ondelete='restrict', string='Ward/Room')
    notes = fields.Text(string='Notes')

    # # accomodation_history_ids = fields.One2many("patient.accomodation.history","bed_id",string="Accomodation History")

    @api.onchange('product_id')
    def onchnage_product_id(self):
        if not self.name:
            self.name = self.product_id.name


class HMSWard(models.Model):
    _name = 'banastech.hms.ward'

    name = fields.Char(size=64, string='Name', required=True, help='Ward / Room code', copy=False)
    building_id = fields.Many2one('banastech.hms.building', ondelete='restrict', string='Department')
    air_conditioning = fields.Boolean(string='Air Conditioning')
    floor = fields.Char(string='Ward/Room Number')
    television = fields.Boolean(string='Television')
    gender = fields.Selection([
        ('men', 'Men Ward'),
        ('women', 'Women Ward'),
        ('unisex', 'Unisex')], string='Gender', required=True)
    private_bathroom = fields.Boolean(string='Private Bathroom')
    telephone = fields.Boolean(string='Telephone')
    microwave = fields.Boolean(string='Microwave')
    guest_sofa = fields.Boolean(string='Guest sofa-bed')
    state = fields.Selection([
        ('available', 'Available'),
        ('full', 'Full')], string='Status')
    private = fields.Boolean(string='Private',help='Check this option for private room')
    number_of_beds = fields.Integer(string='Number of beds', help='Number of patients per ward')
    internet = fields.Boolean(string='Internet Access')
    bio_hazard = fields.Boolean(string='Bio Hazard', help='Check this option if there is biological hazard')
    institution = fields.Many2one('res.partner', ondelete="restrict", string='Institution', help='Medical Center')
    refrigerator = fields.Boolean(string='Refrigerator')
    notes = fields.Text('Notes')
    bed_typ = fields.Selection([
        ('gatch', 'Gatch Bed'),
        ('electric', 'Electric'),
        ('stretcher', 'Stretcher'),
        ('low', 'Low Bed'),
        ('low_air_loss', 'Low Air Loss'),
        ('circo_electric', 'Circo Electric'),
        ('clinitron', 'Clinitron'),], string='Bed Type')
    ward_room_type = fields.Selection([
        ('general', 'General'),
        ('semi_spaecial', 'Semi-Special'),
        ('deluxe', 'Deluxe'),
        ('super_deluxe', 'Super Deluxe'),
        ('suite', 'Suite'),
        ('sharing', 'Sharing'),
        ('icu', 'ICU'),
        ('dialysis', 'Dialysis'),
        ('recovery_room', 'Recovery Room'), ], string='Wards/Room Type',required=True,default='general')
    bed_ids = fields.One2many('banastech.hms.bed', 'ward_id', 'Bed Line', readonly=1)

    @api.onchange('bed_typ')
    def on_change_bed(self):
        bed_ids = self.env['banastech.hms.bed'].search([('bed_type', '=', self.bed_typ)])
        bed_lines = []
        val = {}
        for o in bed_ids:
            bed_lines.append((0,0,{
                'name': o.name,
                'bed_type': o.bed_type,
                'telephone_number': o.telephone_number,
                'state': o.state
            }))
        self.order_line = bed_lines

class HMSBuilding(models.Model):
    _name = 'banastech.hms.building'

    code = fields.Char(size=8, string='Code')
    institution = fields.Many2one('res.partner', ondelete="restrict", string='Institution',help='Medical Center')
    name = fields.Char(size=256, string='Name', required=True,help='Name of the building within the institution')
    extra_info = fields.Text(string='Extra Info')


class HMSOr(models.Model):
    _name = 'banastech.hms.or'

    patient_id = fields.Many2one('banastech.hms.patient', ondelete="restrict", string='Patient')
    hospitalize_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Hosp Id') 
    doctor_id = fields.Many2one('banas.hms.doctor', string='Doctor', ondelete="restrict")
    start_date = fields.Datetime(string='Start Date',default = fields.Datetime.now)
    end_date = fields.Datetime(string='End Date',default = fields.Datetime.now)
    building = fields.Many2one('banastech.hms.building', string='Department', select=True, ondelete="restrict")
    name = fields.Char(size=256, string='Name', required=True, help='Name of the Operating Room')
    institution = fields.Many2one('res.partner', string='Institution', help='Medical Center', ondelete="restrict")
    extra_info = fields.Text(string='Extra Info')
    telephone_number = fields.Integer(string='Telephone Number',help='Telephone number / Extension')
    state = fields.Selection([
        ('free', 'Free'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('na', 'Not available')], string=' Current Status')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]