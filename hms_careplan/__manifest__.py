{
    'name': 'HMS Care Plan',
    'category': 'HMS',
    'author': 'Banas Tech Pvt. Ltd.',
    'version': '1.0',
    'sequence': -91,
    'summary': 'HMS Care Plan',
    'website': 'www.banastech.com',
    'description': """

    """,
    'depends': ['base', 'banastech_hms', 'product', 'hms_hospitalization'],
    'data': [
             'security/ir.model.access.csv',
             'views/careplan_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}