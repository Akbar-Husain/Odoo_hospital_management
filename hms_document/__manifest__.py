{
    'name': 'HMS Document',
    'category': 'HMS',
    'author': 'Banas Tech Pvt. Ltd.',
    'version': '1.0.1',
    'website': 'www.banastech.com',
    'description': """Add Multiple documents to records
    """,
    'license': 'LGPL-3',
    'depends': [
        'base','banastech_hms'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/document_view.xml'
    ],
}