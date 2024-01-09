{
    'name': 'Banastech HMS Orthopedic',
    'version': '1.0',
    'category': 'HMS',
    'summary': 'Hospital Management System',
    'sequence': -88,
    'description': """

    """,
    'author': 'Banas Tech Pvt. Ltd.',
    'website': 'www.banastech.com',
    'depends': ['base', 'banastech_hms', 'hms_investigation', 'banastech_hms_prescription'],  # 'hms_prescription','web_timer_widget','hms_invoice','hms_next_patient_screen'
    'data': [
        'security/ir.model.access.csv',
# #         'wizard/radiology_wizard.xml',
# #         'wizard/pathology_wizard.xml',
# #         'wizard/prescription_wizard.xml',
        'data/account_data.xml',
        'views/appointment_view.xml',
        'views/banastech_hms_prescription_view.xml',
        # 'views/template.xml',
        # 'report/prescription_report.xml',
#         # 'report/prescription_groupreport.xml',
        # 'data/create_appointment.xml',

    ],
    'qweb' : ["static/src/xml/shah_appointment.xml",],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}