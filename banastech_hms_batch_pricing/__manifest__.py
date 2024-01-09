{
    'name': 'BanasTech HMS Batch Wise Pricing',
    'category': 'HMS',
    'author': 'Banas Tech Pvt. Ltd.',
    'version': '1.0.1',
    'sequence': -94,
    'summary': 'Module for Batch Wise Pricing for BanasTech HMS',
    'website': 'www.banastech.com',
    'description': """

    """,
    'depends': ['stock', 'sale'], # 'hms_sale_purchase'
    'data': [
        'security/ir.model.access.csv',
        'views/batch_wise_pricing_view.xml',
    ],
    'demo': [],
    'assets': {},
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3'
}