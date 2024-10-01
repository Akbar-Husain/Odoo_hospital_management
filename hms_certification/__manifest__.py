{
    'name': 'Certificate Management',
    'category': 'HMS',
    'author': 'Torq-Shade',
    'version': '1.0.1',
    'sequence': -96,
    'summary': 'HMS Certificate Management',
    'website': 'www.odoo.com',
    'description': """
        This Module will Add functionality to provide certificate to patient and maintain history..
    """,
    'depends': ["base","mail","banastech_hms"],
    'data' : [
        'security/certificate_security.xml',
        'security/ir.model.access.csv',
        'data/certificate_sequence.xml',
        'views/certificate_management_view.xml',
        'report/certificate_content_report.xml',
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}