{
    'name': 'HMS Bone Bank',
    'category': 'HMS',
    'author': 'Torq-Shade',
    'version': '1.0.2',
    'sequence': -92,
    'summary': 'Hospital Bone Bank Management System',
    'website': 'www.odoo.com',
    'description': """
        This Module will install Bone Bank Module, which will help to register user, and managed bone 
        in the Bone Bank.
    """,
    'depends': ['banastech_hms'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/bone_bank_view.xml',
        'data/bone_bank_sequence.xml',
        # 'report/survey_paper_format.xml',
        # 'report/survey_form.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}