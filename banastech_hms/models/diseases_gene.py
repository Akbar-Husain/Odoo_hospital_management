from odoo import api, fields, models
from odoo.tools.translate import _

class HMSDiseaseGene(models.Model):

    _name = 'banas.hms.disease.gene'
    _description = 'HMS Disease Genes'

    name = fields.Char(string='Official Symbol', size=256, required=True)
    gene_id = fields.Char(string='Gene ID', size=256)
    long_name = fields.Char(string='Official Long Name', size=256, required=True)
    location = fields.Char(string='Location', size=256, required=True, help="Locus of the chromosome")
    chromosome = fields.Char(string='Affected Chromosome', size=256, required=True)
    info = fields.Text(string='Information')
    dominance = fields.Selection([('d', 'dominant'),('r', 'recessive')], 'Dominance', select=True)

HMSDiseaseGene()


class HMSPatientGeneticRisk(models.Model):
    
    _name = 'banas.hms.patient.genetic.risk'
    _description = 'HMS Patient Genetic Risks'
    
    patient_id = fields.Many2one('banastech.hms.patient', ondelete='restrict', string='Patient', select=True)
    disease_gene = fields.Many2one('banas.hms.disease.gene', ondelete='restrict',string='Disease Gene', required=True)

HMSPatientGeneticRisk()

class HMSFamilyDiseases(models.Model):
    
    _name = 'banas.hms.patient.family.diseases'
    _description = 'HMS Patient Family Diseases'

    # patient_id = fields.Many2one('banastech.hms.patient', ondelete='restrict', string='Patient', select=True)
    name_id = fields.Many2many('banas.hms.diseases', 'rz_id','pz_id','cz_id' ,'Disease', required=True)
    xory = fields.Selection([('m', 'Maternal'),('f', 'Paternal')], 'Maternal or Paternal')
    relative = fields.Selection([
                                ('mother', 'Mother'),
                                ('father', 'Father'),
                                ('brother', 'Brother'),
                                ('sister', 'Sister'),
                                ('aunt', 'Aunt'),
                                ('uncle', 'Uncle'),
                                ('nephew', 'Nephew'),
                                ('niece', 'Niece'),
                                ('grandfather', 'Grandfather'),
                                ('grandmother', 'Grandmother'),
                                ('cousin', 'Cousin')], 'Relative',
    help="First degree = siblings, mother and father; second degree = "
    "Uncles, nephews and Nieces; third degree = Grandparents and cousins",required=True)

HMSFamilyDiseases()
