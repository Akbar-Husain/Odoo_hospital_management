from datetime import date
from odoo import api, fields, models


class PatientTag(models.Model):
    _name = "banastech.hms.patient.tag"
    _description = "HMS Patient Tag"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="active", default=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")