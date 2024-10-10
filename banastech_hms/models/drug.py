from odoo import api, fields, models
from odoo.tools.translate import _

class HMSDrugForm(models.Model):
    _name = 'banas.hms.drug.form'
    _description = 'HMS Drug Form'

    code = fields.Char(string='Code')
    name = fields.Char(string='Form', required=True, translate=True)

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]


class HMSActiveComp(models.Model):
    _name = 'banas.hms.active.comp'

    name = fields.Char(size=256, string='Active Component', required=True, translate=True)
#   amount = fields.Float(string='Amount of component', help='Amount of component used in the drug (eg, 250 mg) per dose')


class HMSDrugCompany(models.Model):
    _name = 'banas.hms.drug.company'

    name = fields.Char(size=256, string='Company Name', required=True, translate=True)
    code = fields.Char(size=256, string='Code')


class HMSProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _get_default_form(self):
        tab_id = self.env['banas.hms.drug.form'].search([('name', 'ilike', 'Tablet')])
        return tab_id and tab_id[0].id or False

    form_id = fields.Many2one('banas.hms.drug.form', string='Drug Form', track_visibility='onchange')#TODO ,default=_get_default_form)
    active_component_ids = fields.Many2many('banas.hms.active.comp', 'product_active_comp_rel', 'product_id', 'comp_id', 'Active Component')
    drug_company_id = fields.Many2one('banas.hms.drug.company', string='Drug Company', help='Company producing this drug')    
    lactation = fields.Boolean('Lactation')


class HMSDrugRoute(models.Model):
    _name = 'banas.hms.drug.route'

    code = fields.Char(string='Code')
    name = fields.Char(string='Unit', required=True, translate=True)

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]


class HMSMedicationDosage(models.Model):
    _name = 'banas.hms.medication.dosage'
    _rec_name = 'abbreviation'

    abbreviation = fields.Char(string='Frequency', help='Dosage abbreviation, such as tid in the US or tds in the UK')
    code = fields.Char(string='Nos', help='Dosage Code,for example: SNOMED 229798009 = 3 times per day')
    name = fields.Char(string='English', required=True, translate=True)
    lng_guj = fields.Char('Gujarati')
    lng_hindi = fields.Char('Hindi')
    t1 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T1")
    t2 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T2")
    t3 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T3")
    t4 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')],string="T4")

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]