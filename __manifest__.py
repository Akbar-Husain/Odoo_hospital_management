# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hospital Management',
    'category': 'Hospital',
    'author': 'Local Host',
    'version': '1.0',
    'sequence': -100,
    'summary': 'Hospital management system',
    'description': """ We provide best hospital management system """,
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False, 
    'license': 'LGPL-3',
}