from datetime import date
from odoo import api, fields, models, _


class RegProduct(models.Model):
    _inherit = 'product.template'

    patient_reg = fields.Boolean('Patient Registration')
    product_id =fields.Char(string='Product Id')
    is_product_id = fields.Boolean('Check-Product')