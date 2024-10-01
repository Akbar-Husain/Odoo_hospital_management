{
    'name': 'HMS Paediatric',
    'category': 'HMS',
    'author': 'Torq-Shade',
    'version': '1.1.1',
    'sequence': -98,
    'summary': 'Paediatric appointment and patient management',
    'website': 'www.odoo.com',
    'description': """
        Paediatric appointment and patient management
    """,
    'depends': ['base','mail','product','banastech_hms'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/paediatric_view.xml',
        'views/paediatric_menu.xml',
        # 'data/paediatric_data.xml',
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}