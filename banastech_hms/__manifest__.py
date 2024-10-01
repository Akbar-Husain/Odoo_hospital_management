{
	'name': 'Hospital Management System',
	'category': 'HMS',
	'author': 'Torq-Shade',
	'version': '1.0.1',
	'sequence': -100,
	'summary': 'Hospital Management System',
	'website': 'www.odoo.com',
	'description': """ Hospital Management """,
	'depends': ['mail','product','account'],
	'data': [
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/patient_view.xml',
		'views/appointment_view.xml',
		'views/cancle_appointment_view.xml',
		'views/doctor_view.xml',
		'views/doctor_ref_view.xml',
		'views/medicament_view.xml',
		'views/drug_view.xml',
		'views/account_move_inherit_view.xml',
		'views/menuitem.xml',
		'views/diseases_view.xml',
		'views/medication_dosage_view.xml',
		'views/patient_tag_view.xml',
		'views/product_template_view.xml',
		'report/paper_format.xml',
		'data/sequence.xml',
		'data/banas_hms_data.xml',
		'data/disease_categories_demo.xml',
		'data/diseases_demo.xml',
		'data/patient_occupation_demo.xml',
		'data/doctor_demo.xml',
		'report/patient_cardreport.xml',
	],
	'demo': [
		# 'data/patient_demo.xml',
		# 'data/appointment_demo.xml',
	],
	'assets': {},
	'installable': True,
	'application': True,
	'auto_install': False,
	'license': 'LGPL-3',
}