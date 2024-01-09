{
    'name': 'HMS Investigation',
    'category': 'HMS',
    'author': 'Banas Tech Pvt. Ltd.',
    'version': '1.0.1',
    'sequence': -87,
    'summary': 'Base Module for Hospital Management System',
    'website': 'www.banastech.com',
    'description': """

    """,
    'depends': ['base', 'web', 'banastech_hms', 'hms_hospitalization', 'hms_document'], # 'hms_image_zoom'
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'data/account_data.xml',
        'data/sequence.xml',
        'views/investigation_view.xml',
    ],
    'demo': [
        # 'data/hms_investigation_demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}