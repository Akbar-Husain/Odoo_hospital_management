from lxml import etree
from lxml import etree
import math
import pytz
import threading

from odoo import fields
from datetime import datetime, timedelta
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
import odoo.addons.decimal_precision as dp
from odoo import http
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo import tools
from odoo import fields, models, api, _
from odoo.exceptions import Warning, ValidationError

employee_progress_fields = ['nda_sign', 'background_check', 'verify_check', 'group_broad', 'alternate_phone_no', 'alternate_email_id', 'verification', 'background_check_details',
        'esci', 'pf_form', 'bank_acc', 'cheque_scanned', 'nda' , 'final_degree', 'card_no', 'biometric', 'computer_allocated',
        'is_experience', 'address_proof', 'id_proof']

# class employee_skill(models.Model):
#     _name = "employee.skill"

#     name = fields.Char("Skills Name:")

class banas_hr_employee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Banastech HR Employee'
    _rec_name = 'full_name'

#     @api.model
#     def _default_checklist(self):
#         vals = []
#         checklists = self.env['employee.check.list'].search([('employee_id', '=', False)])
#         for checklist in checklists:
#             vals.append((0, 0, {
#                'name': checklist.name,
#                'remark': checklist.remark,
#             }))
#         return vals

#     @api.model
#     def _default_kaizen_document(self):
#         vals = []
#         checklists = self.env['kaizen.document'].search([('employee_id', '=', False)])
#         for checklist in checklists:
#             vals.append((0, 0, {
#                'name': checklist.name,
#                'remark': checklist.remark,
#             }))
#         return vals

#     @api.model
#     def _default_exit_check_list(self):
#         vals = []
#         checklists = self.env['employee.exist.check.list'].search([('employee_id', '=', False)])
#         for checklist in checklists:
#             vals.append((0, 0, {
#                'name': checklist.name,
#             }))
#         return vals

    aadhar_no = fields.Char('Aadhar Card No')
    pancard_no = fields.Char('PAN Card No')
    date_joining = fields.Date('Joining Date')
    # job_description = fields.Text('Job Description')
#     old_description = fields.Char(string='Old Description')
#     attachment_ids = fields.Many2many('ir.attachment',string='Attachments')

#     id_proof = fields.Boolean("ID Proof")
#     address_proof = fields.Boolean("Address Proof")
#     is_experience = fields.Boolean("If he has experience then Experience letter")
#     final_degree = fields.Boolean("Final degree copy")
#     nda = fields.Boolean("NDA")
#     pf_form = fields.Boolean("PF form 11")
#     group_broad = fields.Boolean("New Employee added in Group broad cast?")
#     verify_check = fields.Boolean("Did you Verify home and other phone no?")
#     background_check = fields.Boolean("Background Check ?")
#     nda_sign = fields.Boolean("NDA sign")
#     super_approval = fields.Boolean("Did Supervisor Approved resignation by replying to employee mail and CC to HR?")
#     is_notice = fields.Boolean("Is notice period mentioned on email?")
#     is_resource = fields.Boolean("Have we given any resource to him? Has he submitted that back to company?\
#                                     (headphone,simcard, ID card, etc)")
#     cheque_received = fields.Boolean("Cheque Receipt received?")
#     security_cheque = fields.Boolean("Security cheque given back?")
#     loan_paid = fields.Boolean("All loan paid?")
#     pf_nos = fields.Boolean("PF no. given to emp?")
#     esi_nos = fields.Boolean("ESI no. given to emp?")
#     is_tds = fields.Boolean("TDS need to cut?")
#     tds_certificate = fields.Boolean("TDS certificate given?")
#     experience_letter = fields.Boolean("Experience letter must be as per he worked for company")
#     is_notice = fields.Boolean("Has he/she completed notice period time?")
#     non_due = fields.Boolean("Non Due Certificate signed")
#     is_pwd_chng = fields.Boolean("Have we changed basecamp, skype, mail pwd, ERP, \
#                                         any access given from 3rd party, fmv, client site pwd change?")
#     resignation_date = fields.Date("Resignation date")
#     last_date = fields.Date("Last Date in organization")


#     alternate_phone_no = fields.Char("Alternate phone no")
#     alternate_email_id = fields.Char("Alternate email id")
#     verification = fields.Char("With whom spoke for background verification")
#     background_check_details = fields.Char("Background Check Details")
#     esci = fields.Char("ESIC")
#     bank_acc = fields.Char("Bank Account no")
#     cheque_scanned = fields.Char("Cheque Scanned copy")
#     card_no = fields.Char("Access card code no")
#     biometric = fields.Char("Biometric code")
#     computer_allocated = fields.Char("Computer alloted no")
#     skills_name_ids = fields.Many2many('employee.skill',string='Skills')

#     survey_one = fields.Many2one('survey.survey', 'Survey for 7 Days')
#     survey_two = fields.Many2one('survey.survey', 'Survey for 15 Days')
#     survey_three = fields.Many2one('survey.survey', 'Survey for 30 Days')
#     employee_joining_progress = fields.Char(compute = '_employee_joining_progress', multi="color", type='integer', string="Progress")

#     #kaizan's fields
    full_name = fields.Char(string="First Name")# compute="_compute_name_horizontal"
    last_name = fields.Char(string="Last Name")
    middle_name = fields.Char(string="Second Name")
    aadhar_name = fields.Char(string="Name as per Adhar")
    pan_name = fields.Char(string="Name as per PAN")
#     gurdian = fields.Char(string="Father\Husband")
#     gurdian_occupation = fields.Char(string="Occupation")
#     phone_personal = fields.Char(string="Personal Phone")
#     street = fields.Char(string="Street")
#     street2 = fields.Char(string="Street2")
#     city = fields.Char(string="City")
#     zip = fields.Char(string="Zip", limit=6)
#     state_id = fields.Many2one("res.country.state", string="State")
#     age = fields.Char(string="Age", compute="_compute_age")
#     place_of_birth = fields.Char(string="Place of Birth")
    emergency_con_no = fields.Char(string="Emergency Cont. No.")
#     personal_email = fields.Char(string="Personal Email ID")
#     salary = fields.Float(string="Salary")
    current_epxperiance = fields.Char(string="Experience in current Organisation")
    total_experience = fields.Char(string="Total Experiance")
    shift = fields.Char(string="Shift")
#     registration_no = fields.Char(string="Registration No.")
#     work_hour = fields.Char(string="W/Hr")
#     actual_con_date = fields.Date(string="Actual Confirmation Date")
#     confirm_due_date = fields.Date(string="Confirmation Due Date")
    help_check_amount = fields.Float(string="Health Check Up Amount")
    voter_id = fields.Char(string="Voter ID")
    driving_lic = fields.Char(string="DL")
#     marrital_status = fields.Selection([
#         ('single', 'Single'),
#         ('married', 'Married'),
#     ],string="Marrital Status")
    date_of_marriage = fields.Date(string="Date of marriage")
    date_of_uan = fields.Date(string="Date of UAN")
    uan_no = fields.Char(string="UAN")
    pf_no = fields.Char(string="PF")
#     blood_group = fields.Char(string="Blood Group")
    ifsc_code = fields.Char(string="IFSC Code")
#     branch = fields.Char(string="Branch")
    employee_family_line = fields.One2many("employee.family", "employee_id", string="Family")
#     employee_family_address_line = fields.One2many("employee.family.address", "employee_id", string="Family Address")
#     employee_experience_line = fields.One2many("employee.experience", "employee_id", string="Experience")
#     employee_language_line = fields.One2many("employee.language", "employee_id", string="Languages")
#     employee_qualification_line = fields.One2many("employee.qualification", "employee_id", string="Qualification")
#     employee_check_list_line = fields.One2many("employee.check.list", "employee_id", string="Employee Check List", default=lambda self: self._default_checklist())
#     kaizen_document_line = fields.One2many("kaizen.document", "employee_id", string="Kaizen Document", default=lambda self: self._default_kaizen_document())
#     employee_history_line = fields.One2many("employee.history", "employee_id", string="Employee History")
#     employee_training_line = fields.One2many("employee.training", "employee_id", string="Employee Training")
#     employee_awards_line = fields.One2many("employee.awards", "employee_id", string="Employee Awards")
#     employee_discliplinary_action_line = fields.One2many("employee.discliplinary.action", "employee_id", string="Employee Discliplinary Action")
#     employee_grievances_line = fields.One2many("employee.grievances", "employee_id", string="Employee Grievances")
#     employee_events_report_line = fields.One2many("employee.events.report", "employee_id", string="Employee Events Report")
#     employee_refuse_work_line = fields.One2many("employee.refuse.work", "employee_id", string="Employee Refuse Work")
#     employee_appraisal_line = fields.One2many("employee.appraisal", "employee_id", string="Employee Appraisal")
#     employee_advance_salary_line = fields.One2many("employee.advance.salary", "employee_id", string="Employee Advance Salary")
#     employee_documents_details_line = fields.One2many("employee.documents.details", "employee_id", string="Employee Documents Details")
#     employee_exit_line = fields.One2many("employee.exist.check.list", 'employee_id', 
#         string="Exit Check List", default=lambda self: self._default_exit_check_list())
    
#     is_phone_resource = fields.Boolean(string="Phone")
#     is_sim = fields.Boolean(string="Sim")
#     is_card = fields.Boolean(string="ID Card")
#     is_uniform = fields.Boolean(string="Uniform")
#     is_other = fields.Boolean(string="Other")
#     other_resource = fields.Char(string="Other Resource")
#     resigned_date = fields.Date(string="Resigned Date")
#     notice_period = fields.Char(string="Notice Period")
#     date_of_relieving = fields.Date(string="Date of Relieving")

#     def onchange_state(self, cr, uid, ids, state_id, context=None):
#         if state_id:
#             country_id=self.pool.get('res.country.state').browse(cr, uid, state_id, context).country_id.id
#             return {'value':{'country_id':country_id}}
#         return {}

#     @api.multi
#     @api.onchange('country_id')
#     def _onchange_country(self):
#         state_obj = self.env['res.country.state']
#         for rec in self:
#             if rec.country_id:
#                 state_datas = state_obj.search([('country_id', '=', rec.country_id.id)])
#                 state_list = [data.id for data in state_datas]
#                 domain = {'state_id': [('id', 'in', state_list)]}
#                 return {'domain': domain}
#             else:
#                 state_datas = state_obj.search([])
#                 state_list = [data.id for data in state_datas]
#                 domain = {'state_id': [('id', 'in', state_list)]}
#                 return {'domain': domain}

#     @api.multi
#     @api.depends('name', 'middle_name', 'last_name')
#     def _compute_name_horizontal(self):
#         for rec in self:
#             rec.full_name = (rec.name.encode('utf-8') if rec.name else '') + ' ' + (rec.middle_name.encode('utf-8') if rec.middle_name else '') + ' ' + (rec.last_name.encode('utf-8') if rec.last_name else '')

#     @api.multi
#     @api.depends('birthday')
#     def _compute_age(self):
#         for record in self:
#             if record.birthday and record.birthday <= fields.Date.today():
#                 record.age = str(relativedelta(
#                                     fields.Date.from_string(fields.Date.today()),
#                                     fields.Date.from_string(record.birthday)).years) + ' ' + 'Years'
#             else:
#                 record.age = str(0) + ' ' + 'Years'

#     # @api.one
#     @api.depends('employee_joining_progress')
#     def _employee_joining_progress(self):
#         res = {}
#         todo = len(employee_progress_fields)
#         for employee in self.browse(self._uid):
#             done = 0
#             for field in employee_progress_fields:
#                 if employee[field]:
#                     done += 1
#             res[employee.id] = {
#                 'employee_joining_progress': ( 100 * done ) / todo,
#                 'color': 3 if done<todo else 0,
#             }
#         return res

#     @api.multi
#     def toggle_active(self):
#         cols = ['super_approval', 'is_notice', 'is_resource',
#             'cheque_received', 'security_cheque', 'loan_paid',
#             'pf_nos', 'is_tds', 'tds_certificate',
#             'experience_letter', 'is_notice', 'non_due', 'is_pwd_chng',
#         ]
#         for col in cols:
#             if not eval('self.'+col):
#                 raise ValidationError(_('Please select %s.')%(col))
#         super(hr_employee, self).toggle_active()

#     @api.multi
#     def write(self,vals):
#         if vals.get('old_description'):
#            vals.update({'old_description': self.old_description + '\n' + vals['job_description']})
#         else:
#            vals.update({'old_description': self.old_description}) 
#         result = super(banastech_hr_employee, self).write(vals)
#         return result

class employee_family(models.Model):
    _name = 'employee.family'

    employee_id = fields.Many2one("hr.employee", string="Employee")
    name = fields.Char(string="Member name", required=True)
    relationship = fields.Char(string="Relationship")
    family_dependence = fields.Char(string="Family Dependence")
    dob = fields.Date(string="DOB")
    age = fields.Char(string="AGE", compute="_compute_age")
    kaizen_employees = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Kaizen Employees")

    @api.model
    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob and record.dob <= fields.Date.today():
                record.age = str(relativedelta(
                                    fields.Date.from_string(fields.Date.today()),
                                    fields.Date.from_string(record.dob)).years) + ' ' + 'Years'
            else:
                record.age = str(0) + ' ' + 'Years'

# class EmployeeFamilyAddress(models.Model):
#     _name = 'employee.family.address'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     address_type = fields.Char(string="Address Type", required=True)
#     con_person_name = fields.Char(string="Contact Person Name")
#     relationship_emp = fields.Char(string="Relation Ship with Employee")
#     address = fields.Char(string="Address")
#     mobile_no = fields.Char(string="Mobile No.")
#     city = fields.Char(string="City")
#     dist = fields.Char(string="Dist")
#     state = fields.Char(string="State")
#     country = fields.Char(string="Country")
#     zip_code = fields.Char(string="Zip Code")


# class EmployeeExperience(models.Model):
#     _name = 'employee.experience'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     external_comp_name = fields.Char(string="External Company name", required=True)
#     functional_domain = fields.Char(string="Functional Domain")
#     external_comp_add = fields.Char(string="External Company Address")
#     last_salary_drawn = fields.Char(string="Last Salary Drawn")
#     from_date = fields.Date(string="From Date")
#     to_date = fields.Date(string="To Date")
#     experience_duration = fields.Char(string="Experience Duration")
#     designation = fields.Char(string="Designation")
#     relevant_exp = fields.Char(string="Relevant Experience")


# class EmployeeLanguage(models.Model):
#     _name = 'employee.language'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     name = fields.Selection(
#         [('hindi', 'Hindi'), 
#         ('english', 'English'),
#         ('gujarati', 'Gujarati'),
#         ('other', 'Other')], string="Languages", required=True)
#     is_read = fields.Boolean(string="Read", default = False)
#     is_write = fields.Boolean(string="Write", default = False)
#     is_speak = fields.Boolean(string="Speak", default = False)


# class EmployeeQualification(models.Model):
#     _name = 'employee.qualification'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     institute = fields.Char(string="Institute/Board/University", required=True)
#     year = fields.Char(string="Year")
#     grade = fields.Char(string="Class/ Grade")
#     subject = fields.Char(string="Subjects")


# class EmployeeCheckList(models.Model):
#     _name = 'employee.check.list'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     name = fields.Char(string="Details", required=True)
#     is_check = fields.Boolean(string="Yes/No", default=False)
#     remark = fields.Char(string="Remark")


# class KaizenDocument(models.Model):
#     _name = 'kaizen.document'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     name = fields.Char(string="Details", required=True)
#     is_check = fields.Boolean(string="Yes/No", default=False)
#     remark = fields.Char(string="Remark")


# class EmployeeHistory(models.Model):
#     _name = 'employee.history'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     employee_designation = fields.Char(string="Employee Designation")
#     active_is = fields.Boolean(string="Active", default=False)
#     designation_from_date = fields.Date(string="Designation From Date")
#     designation_till_date = fields.Date(string="Designation Till Date")
#     reporting_to = fields.Char(string="Reporting To")


# class EmployeeTraining(models.Model):
#     _name = 'employee.training'

#     employee_id = fields.Many2one("hr.employee", string="Trainer")
#     training_date = fields.Date(string="Date")
#     topic = fields.Char(string="Topic")
#     evaluation_marks = fields.Char(string="Evaluation Marks")


# class EmployeeAwards(models.Model):
#     _name = 'employee.awards'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     date = fields.Date(string="Date")
#     theme = fields.Char(string="Theme")
#     attachment_letter = fields.Binary(string="Letter Attachment")


# class EmployeeDiscliplinaryAction(models.Model):
#     _name = 'employee.discliplinary.action'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     date = fields.Date(string="Date")
#     reason = fields.Char(string="Reason")
#     attachment_letter = fields.Binary(string="Letter Attachment")


# class EmployeeGrievances(models.Model):
#     _name = 'employee.grievances'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     date = fields.Date(string="Date")
#     issue = fields.Char(string="Issue")
#     against_to_whom  = fields.Char(string="Against to whom")


# class EmployeeEventsReport(models.Model):
#     _name = 'employee.events.report'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     date = fields.Date(string="Date")
#     type_error = fields.Char(string="Type Error")
#     description = fields.Char(string="Discription ")


# class EmployeeRefuseWork(models.Model):
#     _name = 'employee.refuse.work'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     office_date = fields.Date(string="Offer Date")
#     work = fields.Char(string="Work")
#     reason = fields.Char(string="Reason")


# class EmployeeAppraisal(models.Model):
#     _name = 'employee.appraisal'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     year = fields.Char(string="Year")
#     date = fields.Date(string="Date")
#     ctc = fields.Float(string="CTC")
#     increment_percentage = fields.Float(string="Increment Percentage")
#     current = fields.Float(string="Current")
#     retention_increment = fields.Float(string="Retention Increment")


# class EmployeeAdvanceSalary(models.Model):
#     _name = 'employee.advance.salary'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     date = fields.Date(string="Date")
#     eid = fields.Char(string="EID")
#     designation = fields.Char(string="Designation")
#     amount = fields.Float(string="Amount")
#     reason = fields.Char(string="Reason")
#     approval_person = fields.Char(string="Approval Person")


# class EmployeeDocumentsDetails(models.Model):
#     _name = 'employee.documents.details'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     document_no = fields.Char(string="Document No.")
#     description = fields.Char(string="Document Description")
#     datas = fields.Binary(string="Datas")

# class EmployeeExistCheckList(models.Model):
#     _name = 'employee.exist.check.list'

#     employee_id = fields.Many2one("hr.employee", string="Employee")
#     name = fields.Char(string="Details")
#     is_check = fields.Boolean(string="Yes/No", default=False)