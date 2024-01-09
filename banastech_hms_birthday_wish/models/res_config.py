from odoo import api, fields, models, tools


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'
        
    birthday_mail_template = fields.Many2one('mail.template', 'Birthday Wishes Template', required=True,
            help='This will set the default mail template for birthday wishes.')


    @api.model
    def get_default_birthday_mail_template(self):
        user = self.env.user
        return {'birthday_mail_template': user.company_id.birthday_mail_template.id}

    @api.model
    def set_birthday_mail_template(self):
        user = self.env.user
        user.company_id.write({'birthday_mail_template': self.birthday_mail_template.id})