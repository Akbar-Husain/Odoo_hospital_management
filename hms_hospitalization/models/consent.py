from odoo import api, fields, models
import datetime
from odoo.exceptions import ValidationError

class Consent(models.Model):
    _name = 'inpatient.consent'
    _rec_name = 'consent_form_type'

    @api.model
    def default_get(self, fields):
        res = super(Consent, self).default_get(fields)
        res['model_id'] = self.env['ir.model'].search([('model', '=', 'inpatient.consent')]).id
        return res

    consent_patient_name = fields.Many2one('banastech.hms.patient', ondelete="restrict", string='Patient')
    consent_date = fields.Datetime('Date')
    # consent_type = fields.Many2one('mail.template', domain="[('model', '=', model)]", required=True)
    # consent_selected = fields.Html('Body', related='consent_type.body_html', translate=True, sanitize=False, help="Rich-text/HTML version of the message (placeholders may be used here)")
    # model_id = fields.Many2one('ir.model', 'Applies to', help="The kind of document with with this template can be used")
    # model = fields.Char('Related Document Model', related='model_id.model', index=True, store=True, readonly=True)

    consent_form_template = fields.Html(string='Template')
    consent_form_type = fields.Selection([('blood_consent', 'Blood Consent'),
                                            ('c_colonoscopy', 'C-COLONOSCOPY'),
                                            ('Consent_form_for_transfusion_of_Blood_&_blood_products', 'Consent form for transfusion of Blood & blood products'),
                                            ('high_risk_consent', 'High Risk consent'),
                                            ('icu_admission_consent', 'ICU Admission consent'),
                                            ('informed_consent_costly', 'Informed consent costly'),
                                            ('stoma', 'Stoma'),
                                            ('intubation', 'Intubation'),
                                            ('team_admission', 'Team admission'),
                                            ('C_UPPER_GASTROINTESTINAL_ENDOSCOPY_DILATATION', 'C - UPPER GASTROINTESTINAL ENDOSCOPY DILATATION'),
                                            ('C_UPPER_GASTROINTESTINAL_ENDOSCOPY_FOR_BLEEDING','C - UPPER GASTROINTESTINAL ENDOSCOPY FOR BLEEDING'),
                                            ('C_UPPER_GASTROINTESTINAL_ENDOSCOPY_VARICEAL_BANDING_(OR_GLUEING)', 'C - UPPER GASTROINTESTINAL ENDOSCOPY  VARICEAL BANDING (OR GLUEING)'),
                                            ('C_SIGMOIDOSCOPY','C - SIGMOIDOSCOPY'),
                                            ('Discharge_on_Request_(DOR)', 'Discharge on Request (DOR)')
                                        ], string='C-Type')

    @api.onchange('consent_form_type')
    def _onchange_name(self):
        if self.consent_form_type == 'blood_consent':
            data = self.env['ir.model.data'].search([('name','=','report_blood_consent_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',data)]).arch_base
        if self.consent_form_type == 'c_colonoscopy':
            col = self.env['ir.model.data'].search([('name','=','report_saleorder_oa_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',col)]).arch_base
        if self.consent_form_type == 'Consent_form_for_transfusion_of_Blood_&_blood_products':
            trans = self.env['ir.model.data'].search([('name','=','report_blood_consent_for_transfusion_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',trans)]).arch_base
        if self.consent_form_type == 'high_risk_consent':
            high = self.env['ir.model.data'].search([('name','=','report_high_consent_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',high)]).arch_base
        if self.consent_form_type == 'icu_admission_consent':
            icus = self.env['ir.model.data'].search([('name','=','report_admission_icu_consent_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',icus)]).arch_base
        if self.consent_form_type == 'informed_consent_costly':
            cost = self.env['ir.model.data'].search([('name','=','report_informed_consent_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',cost)]).arch_base
        if self.consent_form_type == 'stoma':
            stomata = self.env['ir.model.data'].search([('name','=','report_stoma_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',stomata)]).arch_base
        if self.consent_form_type == 'intubation':
            inb = self.env['ir.model.data'].search([('name','=','report_intubation_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',inb)]).arch_base
        if self.consent_form_type == 'team_admission':
            teams = self.env['ir.model.data'].search([('name','=','report_team_admission_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',teams)]).arch_base
        if self.consent_form_type == 'C_UPPER_GASTROINTESTINAL_ENDOSCOPY_DILATATION':
            dilations = self.env['ir.model.data'].search([('name','=','report_dilatation_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',dilations)]).arch_base
        if self.consent_form_type == 'C_UPPER_GASTROINTESTINAL_ENDOSCOPY_FOR_BLEEDING':
            gas = self.env['ir.model.data'].search([('name','=','report_bleeding_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',gas)]).arch_base
        if self.consent_form_type == 'C_UPPER_GASTROINTESTINAL_ENDOSCOPY_VARICEAL_BANDING_(OR_GLUEING)':
            glue = self.env['ir.model.data'].search([('name','=','report_variceal_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',glue)]).arch_base
        if self.consent_form_type == 'C_SIGMOIDOSCOPY':
            sigma = self.env['ir.model.data'].search([('name','=','report_sigma_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',sigma)]).arch_base  
        if self.consent_form_type == 'Discharge_on_Request_(DOR)':
            dis = self.env['ir.model.data'].search([('name','=','report_discharge_document')]).id
            self.consent_form_template = self.env['ir.ui.view'].search([('model_data_id','=',dis)]).arch_base  


    @api.onchange('consent_form_type')
    def onchange_template(self):
        self.consent_form_template = self.consent_form_type.types


    @api.model
    def print_consent_report(self, data):
        ir_model_data = self.env['ir.model.data']
        if self.consent_form_type == 'blood_consent':
            template_blood_consent_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_blood_consent_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_blood_consent_document')]).id == template_blood_consent_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_blood_consent')
        if self.consent_form_type == 'c_colonoscopy':
            template_c_colonoscopy_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_saleorder_oa_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_saleorder_oa_document')]).id == template_c_colonoscopy_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_saleorder_oa')
        if self.consent_form_type == 'Consent_form_for_transfusion_of_Blood_&_blood_products':
            template_transfusion_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_blood_consent_for_transfusion_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_blood_consent_for_transfusion_document')]).id == template_transfusion_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_blood_consent_trans')
        if self.consent_form_type == 'high_risk_consent':
            template_high_risk_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_high_consent_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_high_consent_document')]).id == template_high_risk_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_high_consent')
        if self.consent_form_type == 'icu_admission_consent':
            template_icu_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_admission_icu_consent_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_admission_icu_consent_document')]).id == template_icu_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_icu_admission_consent')
        if self.consent_form_type == 'informed_consent_costly':
            template_inform_consent_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_informed_consent_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_informed_consent_document')]).id == template_inform_consent_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_inform_consent_costly_admission_consent')
        if self.consent_form_type == 'stoma':
            template_stoma_consent_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_stoma_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_stoma_document')]).id == template_stoma_consent_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_stoma')        
        if self.consent_form_type == 'intubation':
            template_inbatuation_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_intubation_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_intubation_document')]).id == template_inbatuation_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_intubation')            
        if self.consent_form_type == 'team_admission':
            template_team_admission_confirmation_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_team_admission_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_team_admission_document')]).id == template_team_admission_confirmation_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_team_admission')
        if self.consent_form_type == 'C_UPPER_GASTROINTESTINAL_ENDOSCOPY_DILATATION':
            template_dilatation_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_dilatation_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_dilatation_document')]).id == template_dilatation_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_dilatation_upp')
        if self.consent_form_type == 'C_UPPER_GASTROINTESTINAL_ENDOSCOPY_FOR_BLEEDING':
            template_bleeding_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_bleeding_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_bleeding_document')]).id == template_bleeding_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_bleeding_upp')
        if self.consent_form_type == 'C_UPPER_GASTROINTESTINAL_ENDOSCOPY_VARICEAL_BANDING_(OR_GLUEING)':
            template_variceal_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_variceal_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_variceal_document')]).id == template_variceal_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_variceal_upp')
        if self.consent_form_type == 'C_SIGMOIDOSCOPY':
            template_sigma_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_sigma_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_sigma_document')]).id == template_sigma_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_sigma_upp')
        if self.consent_form_type == 'Discharge_on_Request_(DOR)':
            template_discharge_id = ir_model_data.get_object_reference('hms_hospitalization', 'report_discharge_document')[1]
            if self.env['ir.ui.view'].search([('model_data_id','=','report_discharge_document')]).id == template_discharge_id:
                return self.env['report'].get_action(self, 'hms_hospitalization.report_discharge_upp')