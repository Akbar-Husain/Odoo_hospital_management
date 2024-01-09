from odoo import api, fields, models, _


class HMSOperationalArea(models.Model):
    _name = 'banastech.hms.operational_area'

    info = fields.Text(string='Extra Information')
    # operational_sector = fields.One2many('banastech.hms.operational_sector', 'operational_area_id',string='Operational Sector',readonly=True)
    name = fields.Char(size=256, string='Name', required=True, help='Operational Area of the city or region')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]


class HMSOperationalSector(models.Model):
    _name = 'banastech.hms.operational_sector'

    info = fields.Text(string='Extra Information')
    operational_area_id = fields.Many2one('banastech.hms.operational_area',string='Operational Area')
    name = fields.Char(size=256, string='Op. Sector', required=True,help='Region included in an operational area')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]


class HMSFamily(models.Model):
    _name = 'banastech.hms.family'

    info = fields.Text(string='Extra Information')
    operational_sector = fields.Many2one('banastech.hms.operational_sector',string='Operational Sector')
    name = fields.Char(size=256, string='Family', required=True, help='Family code within an operational sector')
    members = fields.One2many('banastech.hms.family_member', 'family_id',string='Family Members')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Family Code must be unique!')]


class HMSFamilyMember(models.Model):
    _name = 'banastech.hms.family_member'

    member = fields.Many2one('res.partner', string='Member',help='Family Member Name')
    role = fields.Char(size=256, string='Role', required=True)
    family_id = fields.Many2one('banastech.hms.family', string='Family',help='Family code')