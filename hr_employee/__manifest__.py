{
    'name' : 'Employee Check List',
    'category': 'HMS',
    'Author': "Banas Tech Pvt. Ltd.",
    'version' : '1.0.1',
    'sequence': -95,
    'summary': "Allow to Employee's joining checklist and exit checklist.",
    'website': 'www.banastech.com',
    'description': """
Employee Check List
====================
In employee form, there will be three tabs Employee details, Joining Checklist, Kaizen Tenure, Exit Formalities

In employee details tab capture all the basic details related to employee.
    """,
    'depends' : ['base','hr'], # hr_contract, indimedi_kra
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
        # 'views/hr_contract_view.xml',
        # 'data/employee_kaizen_data.xml',
        # 'data/employee_kaizen_document_demo.xml',
        # 'data/employee_exit_check_list_data.xml',
    ],
    'demo': [
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
