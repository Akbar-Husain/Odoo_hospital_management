{
    "name": "Banastech HMS Birthday Wish/Notifications",
    "category": "HMS",
    "author": "Banas Tech Pvt. Ltd.",
    "version": "1.0",
    'sequence': -93,
    "summary": "Send Birthday Wishes via mail, get birthday Notifications and wish your customers",
    "website": "www.banastech.com",
    "description": """In any business customer relations are most important and for any one their bithday is alwasy special so wish your clients using this module and improve your relations. Send Birthday Wishes via mail, get birthday Notifications and wish your customers.""",
    "depends": ['base', 'banastech_hms', 'mail'], # sms_cellapps, 'base.config.settings'
    'data':[
        'views/res_config_view.xml',
        # 'data/template_data.xml',
        # 'data/wish_cronjob.xml',
    ],
    'assets': {},
    "installable": True,
    "active": True,
    "auto_install": False,
    "license": "LGPL-3",
}