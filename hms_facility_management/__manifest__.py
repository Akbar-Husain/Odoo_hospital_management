{
    'name': 'Facility Management',
    'category': 'HMS',
    'author': 'Torq-Shade',
    'version': '1.0.1',
    'sequence': -99,
    'summary': 'Facility management system',
    'website': 'www.odoo.com',
    'description': """
        This module allows you to manage your facility related stuff.
    """,
    'depends': ["base", "mail"],
    'data' : [
        'security/facility_security.xml',
        'security/ir.model.access.csv',
        'data/facility_sequence.xml',
        'views/facility_management_view.xml',
        'views/menuitem.xml',
        # 'data/cron_create_task.xml',
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}