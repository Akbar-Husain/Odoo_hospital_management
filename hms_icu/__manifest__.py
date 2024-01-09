{
    'name': 'HMS - ICU MGMT',
    'category': 'HMS',
    'author': 'Banas Tech Pvt. Ltd.',
    'version': '1.0.1',
    'sequence': -88,
    'summary': 'ICU Management System.',
    'website': 'www.banastech.com',
    'description': """
        ICU Management System.
    """,
    'depends': ['banastech_hms', 'hms_hospitalization'], #  , hms_treatment
    'data': [
       'security/ir.model.access.csv',
       'views/menuitem.xml',
       'views/hms_icu.xml',
       # 'views/hms_icu_css.xml',
       # 'reports/icu_chart_report.xml',
       # 'reports/investigations_report.xml',
       # 'reports/rbs_report.xml',
       'data/sequence.xml',
       # 'data/icu_schedluar.xml',
       'data/diet_value.xml',
       # 'reports/doctor_invoice.xml',
       # 'reports/patient_invoice.xml',
       'views/hms_icu_hospitalization.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}