from odoo import api, fields, models
from datetime import date, datetime, timedelta as td
from odoo.exceptions import UserError
import calendar

class HMSFacilityActivity(models.Model):
    _name = 'hms.facility.activity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Faciltiy Activity'


    name = fields.Char(size=256, string='Sequence', copy=False)
    activity_name = fields.Char('Activity Name', required="True")
    date_activity = fields.Date('Date')
    assigned_id = fields.Many2one('res.users',string='Assigned To', help="Name of the person who is Assigned the Activity")
    reviewer_id = fields.Many2one('res.users',string='Reviewer', help="Name of the person who is reviewing the Activity")
    date_review = fields.Date('Reviewer Date', readonly="True")
    state = fields.Selection([('draft','Draft'),('done','Done')], 'Status', default="draft", track_visibility='onchange') 
    remark = fields.Text('Remark')

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('hms.facility.activity') or ''
        return super(HMSFacilityActivity, self).create(values)

    @api.model
    def action_done(self, values):
        self.date_review = fields.Date.today()
        self.reviewer_id =  self.env.user.id
        self.state = 'done'

    @api.model
    def unlink(self, values):
        for data in self:
            if data.state in ['done']:
                raise UserError(('You can only delete in draft'))
        return super(HMSFacilityActivity, self).unlink()
        
class HMSFacilityMaster(models.Model):
    _name = 'hms.facility.master'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(size=256, string='Sequence', copy=False)
    facility_name = fields.Char('Name', required="True")
    reviewer_id = fields.Many2one('res.users',string='Reviewer', help="Name of the person who is reviewing the task")
    time_type = fields.Selection([('daily','Daily'),('days','2 Days'),('weekly','Weekly'),('monthly','Monthly')], 'Type', default="daily")
    responsible_id = fields.Many2one('res.partner',string='Responsible', help="Name of the person who is responsible for the task")
    start_date = fields.Date('Start Date',default=fields.Date.context_today)
    end_date = fields.Date('End Date',default=fields.Date.context_today)
    next_execution_date = fields.Date('Next Execution Date')
    state = fields.Selection([('draft','Draft'),('running','Running'),('cancel','Cancel')], 'Status', default="draft", track_visibility='onchange')

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('hms.facility.master') or ''
        return super(HMSFacilityMaster, self).create(values)

    @api.model
    def action_running(self, values):
        self.state = 'running'

    @api.model
    def action_cancel(self, values):
        self.state = 'cancel'

    @api.model
    def create_task(self):
        activity_obj = self.env['hms.facility.activity']
        today = date.today()
        master_data_ids = self.search([
            ('start_date', '<=', fields.date.today()),
            ('end_date', '>', fields.date.today()),
            ('state', '=', 'running')])
        for master in master_data_ids: 
            time_type = master.time_type
            if time_type == 'daily':
                master.start_date = today
                master.next_execution_date = datetime.strptime(master.start_date,'%Y-%m-%d') + td(days=1)
                activity_obj.create({'activity_name':master.facility_name,'date_activity':master.start_date,'assigned_id':master.responsible_id.id,'reviewer_id':master.reviewer_id.id})
            elif time_type == 'days':
                delta = td(days=today.weekday())
                master.start_date = today - delta
                master.next_execution_date = datetime.strptime(master.start_date,'%Y-%m-%d') + td(days=2)
                activity_obj.create({'activity_name':master.facility_name,'date_activity':master.start_date,'assigned_id':master.responsible_id.id,'reviewer_id':master.reviewer_id.id})
            elif time_type == 'weekly':
                delta = td(days=today.weekday())
                master.start_date = today - delta
                master.next_execution_date = datetime.strptime(master.start_date,'%Y-%m-%d') + td(days=7)
                activity_obj.create({'activity_name':master.facility_name,'date_activity':master.start_date,'assigned_id':master.responsible_id.id,'reviewer_id':master.reviewer_id.id})
            elif time_type == 'monthly':
                month_range = calendar.monthrange(today.year, today.month)
                master.start_date = today.replace(day=1)
                master.next_execution_date = today.replace(day=month_range[1])
                activity_obj.create({'activity_name':master.facility_name,'date_activity':master.start_date,'assigned_id':master.responsible_id.id,'reviewer_id':master.reviewer_id.id})