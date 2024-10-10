from odoo import api, fields, models
from odoo.tools.translate import _
from datetime import datetime, date, timedelta
import dateutil.relativedelta
from odoo.exceptions import ValidationError,UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import odoo.addons.decimal_precision as dp
import time


# class ApnInduction(models.Model):
#     _name = 'apn.induction'

#     name = fields.Char('Induction')


# class ApnReversal(models.Model):
#     _name = 'apn.reversal'

#     name = fields.Char('Reversal')


class IndimediIPDDischargeInstruction(models.Model):
    _name = "ipd.discharge.instruction"
    _description = "IPD Discharge Instruction"
    
    name = fields.Char(string='Discharge Instruction', required=True)


class IndimediInstruction(models.Model):
    _name = "hms.instruction"
    _description = "Instruction List"
    
    name = fields.Char('Instruction')
    gender = fields.Selection([('m','Male'),('f','Female'),('o','Other')],string="Gender", default='m')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain =[]
        if self._context.__contains__('patient_id') and self._context.get('patient_id',False):
            patient = self.env['banastech.hms.patient'].search([('id','=',self._context.get('patient_id',False))])
            domain += [('gender','=',patient.gender)]
        if self._context.__contains__('gender') and self._context.get('gender',False):
            domain += [('gender','=',self._context.get('gender'))]
        if self._context.__contains__('instruction_group_id') and self._context.get('instruction_group_id',False):
            instruction_id = self.env['ipd.instruction'].search([('inst_group_id','=',self._context.get('instruction_group_id'))])
            instruction = []
            for inst in instruction_id:
                instruction.append(inst.inst_id.id)
            if instruction:
                domain += [('id','in',instruction)]
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()

class IndimediIPDInstructionGroup(models.Model):
    _name = "ipd.instruction.group"
    _description = "Instruction Group"

    name = fields.Char(string='Instruction Group Name(English)', required=True)
    ipd_instruction_ids = fields.One2many('ipd.instruction','inst_group_id',string="Instructions", translate=True)
    gender = fields.Selection([('m','Male'),('f','Female'),('o','Other')],string="Gender", default='m')

class IndimediIPDInstruction(models.Model):
    _name = "ipd.instruction"
    _description = "IPD Instruction"
    _rec_name = 'inst_id'

    inst_id = fields.Many2one('hms.instruction', string='Instruction', ondelete="restrict")
    ipd_id = fields.Many2one('inpatient.registration', string='IPD Instruction', ondelete="restrict")
    inst_group_id = fields.Many2one('ipd.instruction.group',string="Instruction Group")

class Hospitalization(models.Model):
    _name = "inpatient.registration"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Patient Hospitalization"

    @api.model
    def _default_checklist(self):
       vals = []
       checklists = self.env['inpatient.checklist.template'].search([])
       for checklist in checklists:
           vals.append((0, 0, {
               'name': checklist.name,
               'remark': checklist.remark,
           }))
       return vals

#     @api.model
#     def _default_patient_history(self):
#         vals = []
#         patients = self.env['naaf.patient.history'].search([])
#         for patient in patients:
#             vals.append((0, 0, {
#                 'name': patient.name,
#             }))
#         return vals

#     @api.model
#     def _default_family_history(self):
#         vals = []
#         familys = self.env['naaf.family.history'].search([])
#         for family in familys:
#             vals.append((0, 0, {
#                 'name': family.name,
#             }))
#         return vals

#     @api.model
#     def _default_pediatric_history(self):
#         vals = []
#         pediatrics = self.env['naaf.pediatric.history'].search([])
#         for pediatric in pediatrics:
#             vals.append((0, 0, {
#                 'name': pediatric.name,
#                 'yes':pediatric.yes,
#                 'no':pediatric.no,
#             }))
#         return vals

#     @api.model
#     def _default_child_growth(self):
#         vals = []
#         child_growths = self.env['naaf.child.growth'].search([])
#         for child_growth in child_growths:
#             vals.append((0, 0, {
#                 'name': child_growth.name,
#             }))
#         return vals

#     @api.model
#     def _default_activities_daily_living(self):
#         vals = []
#         daily_livings = self.env['naaf.activities.daily.living'].search([])
#         for daily_living in daily_livings:
#             vals.append((0, 0, {
#                 'name': daily_living.name,
#             }))
#         return vals

#     @api.model
#     def _default_vulnerable_assessment(self):
#         vals = []
#         vul_asses = self.env['naaf.vulnerable.assessment'].search([])
#         for vul_asse in vul_asses:
#             vals.append((0, 0, {
#                 'name': vul_asse.name,
#             }))
#         return vals

#     @api.model
#     def _default_fall_risk_assessment(self):
#         vals = []
#         risks = self.env['naaf.fall.risk.assessment'].search([])
#         for risk in risks:
#             vals.append((0, 0, {
#                 'name': risk.name,
#                 'value':risk.value,
#             }))
#         return vals


#     @api.model
#     def _default_prewardklist(self):
#         vals = []
#         prechecklists = self.env['pre.ward.check.list.template'].search([])
#         for prechecklist in prechecklists:
#             vals.append((0,0,{
#                 'name': prechecklist.name,
#                 'remark': prechecklist.remark,
#             }))
#         return vals


    name = fields.Char(string='IP No. #', size=128, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('reserved', 'Reserved'),
        ('hosp','Hospitalized'),
        ('discharged', 'Discharged'),
        ('cancel', 'Cancelled'),
        ('done', 'Done'),], string='Status', default='draft', track_visibility='always')
    patient_id = fields.Many2one('banastech.hms.patient', ondelete="restrict", string='Patient', track_visibility='always', states={'hosp': [('readonly', True)], 'discharged': [('readonly', True)], 'done': [('readonly', True)]})
    mobile = fields.Char(related='patient_id.mobile', string='Mobile' ,readonly=True)
    image = fields.Binary(related='patient_id.image',string='Image', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    appointment_id = fields.Many2one('banastech.hms.appointment', ondelete="restrict", string='Appointment', domain="[('patient_id', '=', patient_id)]")
    hospitalization_date = fields.Datetime(string='Date of Admission', default=fields.Datetime.now, states={'hosp': [('readonly', True)], 'discharged': [('readonly', True)], 'done': [('readonly', True)]})
    company_id = fields.Many2one('res.company', ondelete="restrict", string='Institution', default=lambda self: self.env.user.company_id.id )
    department_id = fields.Many2one(related='appointment_id.department_id', ondelete="restrict", string='Department')
    attending_physician_ids = fields.Many2many('banas.hms.doctor','hosp_pri_att_doc_rel','hosp_id','doc_id',string='Attending Physician')
    relative_id = fields.Many2one('res.partner', ondelete="cascade", domain=[('type', '=', 'contact')], string='Patient Relative Name')
    relative_name = fields.Char(string="Relative Name")
    relative_with_patient = fields.Char(string="Relation with Patient")
    relative_number = fields.Char(string='Patient Relative Number')
    mlc = fields.Boolean(string='MLC')
    ward_id = fields.Many2one('banastech.hms.ward', ondelete="restrict", string='Ward/Room', states={'hosp': [('readonly', True)], 'discharged': [('readonly', True)], 'done': [('readonly', True)]})
    ward_package_id = fields.Many2one('product.product',ondelete="restrict",string='Package',domain=[('hospital_product_type','=','hosp_package')])
    bed_id = fields.Many2one ('banastech.hms.bed', ondelete="restrict", string='Bed No.', states={'hosp': [('readonly', True)], 'discharged': [('readonly', True)], 'done': [('readonly', True)]})
    admission_type = fields.Selection([
        ('routine','Routine'),
        ('lithotripsy', 'Lithotripsy'),
        ('elective','Elective'),
        ('urgent','Urgent'),
        ('emergency','Emergency')],string='Admission type',default='routine', states={'hosp': [('readonly', True)], 'discharged': [('readonly', True)], 'done': [('readonly', True)]})
    admission_reason = fields.Many2one ('banas.hms.diseases', ondelete="restrict", string='Reason for Admission', help="Reason for Admission")
    discharge_date = fields.Datetime (string='Date of Discharge')
    payment_category = fields.Selection([('cash','Cash'),('credit','Credit')], string='Payment category', default='cash', required='True')
    no_invoice = fields.Boolean(string='Invoice Exempt')
    tpa_id = fields.Many2one('hospitalization.tpa', ondelete="cascade", string='TPA')
    accomodation_history_ids = fields.One2many("patient.accomodation.history", "inpatient_id", string="Accomodation History")
#     #For CheckList
    checklist_ids = fields.One2many('inpatient.checklist', 'inpatient_id', string='Admission Checklist', default=lambda self: self._default_checklist())
    
#     # pre_operative_checklist_ids = fields.One2many('pre.operative.check.list', 'inpatient_id', string='Pre-Operative Checklist', default=lambda self: self._default_prechecklist())
#     pre_ward_checklist_ids = fields.One2many('pre.ward.check.list', 'inpatient_id', string='Transfer Checklist', default=lambda self: self._default_prewardklist())
#     #For Hospitalization Surgery
#     surgery_id = fields.Many2many('hms_surgery','hosp_patient_surgery','hosp_id','surgery_id', ondelete="restrict", string='Surgery')
    hospital_ot = fields.Many2one('banastech.hms.or', ondelete="restrict", string='Operation Theatre')
    # start_date = fields.Datetime(string='Surgery Date')
    end_date = fields.Datetime(string='End Date')
#     user_id = fields.Many2one('res.users', string='Anesthetist', ondelete="set null", help='Anesthetist data of the patient',domain=[('is_anesthetist','=',True)])
#     anaesthesia_id = fields.Many2one('anaesthesia', ondelete="set null", string="Anaesthesia")
#     #primary_physician = fields.Many2one ('hms.physician', ondelete="restrict", string='Primary Surgeon')
#     primary_physician_ids = fields.Many2many('hms.physician','hosp_pri_doc_rel','hosp_id','doc_id',string='Primary Surgeons')
#     assisting_surgeons = fields.Many2many('hms.physician','hosp_doc_rel','hosp_id','doc_id',string='Assisting Surgeons')
#     scrub_nurse = fields.Many2one('res.users', ondelete="set null", string='Scrub Nurse',domain=[('is_nurse','=',True)])
#     picking_type_id = fields.Many2one('stock.picking.type', ondelete="restrict", string='Picking Type')
#     reason_id = fields.Many2one('hms.reason', ondelete="cascade", string='Reason')
#     follow_date = fields.Datetime(string='Follow Up Date')
#     notes = fields.Text(string='Operative Notes')
#     stone_line_ids = fields.One2many('hospital_stone_line', 'inpatient_id',string='Stone')
#     prostate_line_ids = fields.One2many('hospital_prostate_line', 'inpatient_id',string='Prostate')
#     reconstructive_line_ids = fields.One2many('hospital_reconstructive_line', 'inpatient_id',string='Reconstructive')
#     ablative_line_ids = fields.One2many('hospital_ablative_line', 'inpatient_id',string='Ablative')
#     female_urology_line_ids = fields.One2many('hospital_female_urology_line', 'inpatient_id',string='Female Urology')
#     onco_urology_line_ids = fields.One2many('hospital_onco_urology_line', 'inpatient_id',string='Onco Urology')
#     # medicament_line = fields.One2many('medicament.line', 'inpatient_id',string='Medicament Line')
#     # consumable_line = fields.One2many('consumable.line', 'inpatient_id',string='Consumable Line')
#     # miscellaneous_ids = fields.One2many('miscellaneous.drugs','inpatient_id',string='Miscellaneous Drugs')
#     # antibiotic_idsantibiotic_ids = fields.One2many('antibiotic.analogesis','inpatient_id',string='Antibiotic & Analgesics')
#     # fluid_ids = fields.One2many('ip.fluid','inpatient_id',string='I/V Fluids')
#     diet_plan = fields.Many2one("hms.dietplan", ondelete="cascade", string='Diet Plan')
#     # special_precautions_id = fields.Text(string="Special Precautions")
#     # post_liquid_monitoring_line = fields.One2many('liquid.monitoring', 'post_liquid_id',string='Liquid')
#     # care_liquid_monitoring_line = fields.One2many('liquid.monitoring', 'care_liquid_id',string='Liquid')
#     # Discharge fields
#     diagnosis = fields.Text(string="Diagnosis")
    clinincal_history = fields.Text(string="Clinical Summary")
#     examination_id = fields.Text(string="Examination")
#     investigation_id = fields.Text(string="Investigation")
#     adv_on_dis = fields.Text(string="Advice on Discharge")
    invoice_id = fields.Many2one('account.move', ondelete="restrict", string='Invoice')
#     #Extra Field For Shah Hospital
    prov_diagnosis = fields.Text(string="Prov. Diagnosis")
#     prov_mm_diagnosis = fields.Many2many('prov.mm.diagnosis','hosp_prov_diagnosis_rel','prov_id','mm_diagnosis_id',string="Prov. Diagnosis")
#     prov_mm_diagnosis_dummy = fields.Many2many('prov.mm.diagnosis','hosp_prov_diagnosis_rel','prov_id','mm_diagnosis_id',string="Prov. Diagnosis")
    discharge_diagnosis = fields.Text(string="Discharge Diagnosis")
#     medication_diagnosis_ids = fields.Many2many('hms.diseases','hosp_diagnosis_rel','hosp_id','diagnosis_id',string='Medication During Hospitalization')
    discharge_status = fields.Selection([
        ('stable','Stable'),
        ('unstable', 'Unstable'),
        ('other','Other')],string='Discharge Status',default='stable')
    type_of_discharge = fields.Many2one('ipd.discharge.instruction', ondelete="cascade", string='Type of Discharge')
    past_history = fields.Text(string="Past History")
    past_surgical_history = fields.Text(string="Past Surgical History")
    op_note = fields.Text(string="Op. Note")
    followup_issue = fields.Text(string="Followup Advice")
    post_operative = fields.Text(string="Post Operative Course")
# #     treatment_at_home = fields.Text(string="Treatment to be countiued at home") 
    instruction_group_id = fields.Many2one('ipd.instruction.group',string="Instruction Group")
    instruction = fields.One2many('ipd.instruction','ipd_id',string='Instruction')
    hospitalization_injury = fields.Selection([('yes','Yes'),('no','No')],string="Hospitalization due to injury")
    cause = fields.Selection([('option1','Self-inflicted'),('option2','Road Traffic Accident'),('option3','Substance abuse /alcohol consumption')],string='if Yes,give cause')
    outside_injury = fields.Selection([('yes','Yes'),('no','No')],string="If Injury due to Substance abuse /alcohol consumption,Test Conducted to this establish this")
    medico_legal = fields.Selection([('yes','Yes'),('no','No')],string="If Medico legal")
    reported_to_police = fields.Selection([('yes','Yes'),('no','No')],string="Reported to police")
    fir_no = fields.Char(string="FIR No.")
    fir_reason = fields.Char(string="If not reported to police give reason")
#     #Patient Hisory Checklist
#     phc_date = fields.Datetime(string="Date & Time")
#     diabetes_mel = fields.Char(string="Diabetes mellitus")
#     hypertension = fields.Char(string="Hypertension")
#     other_illness = fields.Char(string="Other illness")
#     phc_past_surgical_history = fields.Text(string="Past Surgical History")
#     # course_hospital = fields.Char(string="Course in Hospital")
#     #For Basic Care Plan
    nurse_id = fields.Many2one('res.users', ondelete="cascade", string='Primary Nurse', help='Anesthetist data of the patient',domain=[('is_nurse','=',True)]) # 
    nursing_plan = fields.Text (string='Nursing Plan')
    ward_rounds = fields.One2many('ward.rounds', 'round_id',string='Ward Rounds')
    discharge_plan = fields.Text (string='Discharge Plan')
    expected_stay = fields.Char(string='Expected stay',default='4')
    remark_note = fields.Text(string="Remark")
#     latest_op_note = fields.Text(string="OP. Note")
    primary_physician = fields.Many2one(related='patient_id.primary_doctor_id' ,string='Consultant Incharge', ondelete='restrict')
    cashless = fields.Boolean(string="Cashless",default=False)
    gender = fields.Selection(related='patient_id.gender', string='Gender')
    done_summary = fields.Boolean('Done Discharge', default=False)

#     #Admission Note(Opd/Ipd)
#     admission_note_ids = fields.One2many('admission.note','inpatient_id')
    hms_surgery_dietician_ids = fields.One2many('hms.surgery.dietician', 'hms_surgery_dietician_id', string="Dietician")
    progress_note_ids = fields.One2many('hms.progress.note', 'hospitalization_id','Progess Note')

#     #Assessment-Physiotherapy
    assess_phy_pulse = fields.Float(string="Pulse" )
    assess_phy_rr = fields.Float(string="RR")
    assess_phy_bp = fields.Float(string="BP")
    assess_phy_lbp = fields.Float(string="LBP")
    assess_phy_spo2 = fields.Float(string='SPO2')
    assess_phy_pain = fields.Char(string="Pain")
    assess_res_exam = fields.Text(string="Respiratory Examination")
    spirometry = fields.Char(string="Spirometry")
    phy_remark = fields.Char(string="Remarks")
    assess_post_pulse = fields.Float(string="Pulse")
    assess_post_rr = fields.Float(string="RR")
    assess_post_bp = fields.Float(string="BP")
    assess_post_lbp = fields.Float(string="LBP")
    assess_post_spo2 = fields.Float(string='SPO2')
    assess_post_pain = fields.Char(string="Pain")
    assess_post_res_exam = fields.Text(string="Respiratory Examination")
    post_spirometry = fields.Char(string="Spirometry")
    post_phy_remark = fields.Char(string="Remarks")
    phy_notes_line = fields.One2many('phy.notes','inpatient_id', string="Physiotherapy Notes")

#     #Plan of Care
#     poc_inter_conser = fields.Selection([('yes', 'Intervention'),('no', 'Conservation')],default='no',string='POC')
#     # poc_radio_line = fields.One2many('hms.investigation.radiology.line', 'palnofcare_id', string='Radiology Line')
    
#     poc_aspectsofcare = fields.Text('Preventive aspects of care')
    poc_goals = fields.Text('Goals')
#     blood_transfusion = fields.Selection([('yes', 'Yes'),('no', 'No')],string="Blood Product Transfusion", default='no')
#     blood_transfusion_value = fields.Char('approx requirement')
#     oral_drug = fields.Boolean('Oral drug')
#     isulin_plan = fields.Boolean('Insulin Plan')
#     physiotherapy_needs = fields.Selection([('yes', 'Yes'),('no', 'No')],string="Physiotherapy need", default='no')
#     physiotherapy_need_notes = fields.Char(string='Note')
#     pain_managements = fields.Selection([('yes', 'Yes'),('no', 'No')],string="pain Management", default='no')
#     pain_management_notes = fields.Char(string='Note')
#     any_specific_monitoring = fields.Selection([('yes', 'Yes'),('no', 'No')],string="Any specific monitoring", default='no') 
#     specific_monitoring_value = fields.Char('Note')
#     nc_ryle_tube = fields.Boolean("Ryle's Tube Feeding")
#     nc_parental = fields.Boolean('Parenteral Nutrition')
#     nc_food_drug = fields.Boolean('Food-Drug')
#     nc_drug_drug = fields.Boolean('Drug-Drug')
#     nc_drug_drug_value = fields.Char('If Yes')
#     poc_procedure = fields.Char('Name of procedure')
#     poc_approx_stay = fields.Char('Approx length of stay')
#     curative_ivfluid = fields.Boolean('IV Fluid')
#     curative_antibiotic = fields.Boolean('Antibiotic')
#     curative_causative = fields.Boolean('Causative Treatment')
#     curative_anyother = fields.Boolean('Any other')
#     curative_anyother_note = fields.Char('Note')
#     cross_reference  = fields.Selection([('yes', 'Yes'),('no', 'No')],string="Cross reference",default='no')
#     nameofdoctor = fields.Many2one('hms.physician', 'Name of Doctor')
#     poc_user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user,readonly="True")
#     poc_create_timestamp = fields.Datetime('Created Date', default=lambda self: time.strftime('%Y-%m-%d %H:%M:%S'),readonly="True")
#     any_specific_equ = fields.Selection([('yes', 'Yes'),('no', 'No')],string="Any specific equipment",default='no')
#     any_specific_yes1 = fields.Char('If yes')
#     any_specific_yes2 = fields.Char('Any procedure')
#     edu_pre_aspe = fields.Boolean('Intervention')
#     preventive_aspects = fields.Boolean('Preventive aspects')
#     useofequipment = fields.Boolean('Use of equipment')
#     medication = fields.Boolean('Medication')
#     infection_control = fields.Boolean('Infection Control')
#     #Admission History and Physical Assessment Form
    bmi_line_by_doctor_ids = fields.One2many('bmi.line.by.doctor','bmi_line_by_doctor_id', string="BMI Records")
    ahpa_allergies_ids = fields.One2many('ahps.allergies','ahps_allergies_id',string="Allergies")
#     ph_hypertension = fields.Boolean(string='Hypertension')
#     ph_hypertension1 = fields.Char(string='since')
#     ph_hypertension2 = fields.Text(string='On Medication')   
#     ph_hypertensiondr = fields.Char(string='Under Treatment of Dr.')
#     ph_diabetes = fields.Boolean(string='Diabetes')
#     ph_diabetes1 = fields.Char(string='since')
#     ph_diabetes2 = fields.Text(string='On Medication')
#     ph_diabetesdr = fields.Char(string='Under Treatment of Dr.')
    ph_ischaemic_hd = fields.Boolean(string='Ischaemic Heart Disease')
    ph_ischaemic_hd1 = fields.Char(string='since')
    ph_ischaemic_hd2 = fields.Text(string='On Medication')
    ph_ischaemic_hddr = fields.Char(string='Under Treatment of Dr.')
    ph_tuberculosis = fields.Boolean(string='Tuberculosis')
    ph_tuberculosis1 = fields.Char(string='since')
    ph_tuberculosis2 = fields.Text(string='On Medication')
    ph_tuberculosisdr = fields.Char(string='Under Treatment of Dr.')
    pho_ids = fields.One2many('ph.operation','pho_id','P/H of Operation')
    phh_ids = fields.One2many('ph.hospitalization','phh_id','P/H of Hospitalization')
    pho_phh_remark = fields.Text(string="Remark")
    fh_hypertension = fields.Boolean(string='Hypertension')
    fh_hypertension_value = fields.Char(string='Note')
    fh_heart_disease = fields.Boolean(string='Heart Disease')
    fh_heart_disease_value = fields.Char(string='Note')
    fh_diabetes = fields.Boolean(string='Diabetes')
    fh_diabetes_value = fields.Char(string='Note')
    fh_tuberculosis = fields.Boolean(string='Tuberculosis')
    fh_tuberculosis_value = fields.Char(string='Note')
    fh_epilepsy = fields.Boolean(string='Epilepsy')
    fh_epilepsy_value = fields.Char(string='Note')
    fh_asthma = fields.Boolean(string='Asthma')
    fh_asthma_value = fields.Char(string='Note')
    fh_stroke = fields.Boolean(string='Stroke')
    fh_stroke_value = fields.Char(string='Note')
    fh_arthritis = fields.Boolean(string='Arthritis/Gout')
    fh_arthritis_value = fields.Char(string='Note')
    fh_cancer = fields.Boolean(string='Cancer')
    fh_cancer_value = fields.Char(string='Note')
    fh_chronic = fields.Boolean(string='Other Chronic Disease')
    fh_chronic_value = fields.Char(string='Other Chronic Disease')
    personals_history_ids = fields.One2many('personals.history.id','personals_history_id','Personal History')
    personals_historys_ids = fields.One2many('personals.historys.id','personals_historys_id','Personal History')
    chief_complain = fields.Text(string="Chief Complaint")
    sign_labreport_ids = fields.One2many('significant.lab.report','sign_labreport_id',string="Sign. Lab Reports")
    by_doctor_past_history_ids = fields.One2many('by.doctor.past.history','by_doctor_past_history_id',string='Past Histpry')
    f_menstrual_history = fields.Date(string="Menstrual History:L.M.P.Date")
    f_obstetric_history = fields.Char(string='Obstetric History:L.D.')
    f_abortion = fields.Char(string="Abortion")
    f_reg_inreg = fields.Selection([('regular', 'Regular'),('irregular', 'Irregular')], string="Regular/Irregular")
    f_others = fields.Char(string="Others")
    pe_temp = fields.Float(string="Temp(F)")
    pe_pulse = fields.Char(string="Pulse")
    pe_rr = fields.Float(string="R/R")
    pe_bp = fields.Char(string="B.P.")
    pe_lbp = fields.Char(string="B.P.")
    pe_pain = fields.Selection([('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'), ('nine', '9'), ('ten', '10')], default="one",string="Pain Score")
    pe_spo2 = fields.Float(string="SPO2")
    ge_anemia = fields.Boolean(string="Anemia")
    ge_cyanosis = fields.Boolean(string="Cyanosis")
    ge_jaundice = fields.Boolean(string="Jaundice")
    ge_gen_lymp = fields.Boolean(string="Generalized Lymphadenopathy")
    ge_pedal_oedema = fields.Boolean(string="Pedal Oedema")
    general_examination = fields.Text(string="General Examination Note")
    se_respiratory = fields.Text(string="Respiratory System")
    se_centralnervous = fields.Text(string="Central Nervous System")
    se_cardiovascular = fields.Text(string="Cardiovascular System")
    se_musculoskeletal = fields.Text(string="Musculoskeletal System")
    se_extremities = fields.Text(string="Extremities/Spine")
#     se_lymphatics = fields.Text(string="Lymphatics")
    se_abdomen = fields.Text(string="Abdomen")
#     se_skin = fields.Text(string="Skin")
    provisional_diagnosis = fields.Text(string="Provisional Diagnosis")
    medical_officers_note = fields.Text(string="Medical Officers")
    consultant_note = fields.Text(string="Consultant Note")
    planofcare_hosp = fields.Text(string="Paln of Care")
    create_user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user,readonly="True")
    create_timestamp = fields.Datetime('Created Date', default=lambda self: time.strftime('%Y-%m-%d %H:%M:%S'),readonly="True")
    admission_histphyasst_id = fields.Many2one('inpatient.registration',string="Admission History")
#     # Assessment-Doctor(ER)
    assess_doc_temp = fields.Float(string="Temperature", digits=dp.get_precision('temperature(Assessment-Doctor-ER)'))
    assess_doc_pulse = fields.Float(string="Pulse", digits=dp.get_precision('Pulse(Assessment-Doctor-ER)'))
    assess_pain_score = fields.Selection([('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'), ('nine', '9'), ('ten', '10')], default="one",string="Pain Score")
    assess_doc_rr = fields.Float(string="RR", digits=dp.get_precision('RR(Assessment-Doctor-ER)'))
    assess_doc_bp = fields.Float(string="BP", digits=dp.get_precision('BP(Assessment-Doctor-ER)'))
    assess_doc_lbp = fields.Float(string="LBP", digits=dp.get_precision('LBP(Assessment-Doctor-ER)'))
    assess_doc_spo2 = fields.Float(string='SPO2', digits=dp.get_precision('Spo2(Assessment-Doctor-ER)'))
#     # Assessment Patient
    pa_chief_complaint = fields.Text('Chief Complaint')
    pa_abdominal_examination_note = fields.Text('Abdominal Examination')
    pa_rectal_examination_note = fields.Text('Rectal Examination')

    pa_triage = fields.Boolean('Triage acuity')
    pa_triage_life = fields.Boolean('Life Threatening Emergency')
    pa_triage_nolife = fields.Boolean('Non Life Threatening Emergency')
    pa_triage_noemery = fields.Boolean('Non Emergency')
#     pa_triage_brought = fields.Boolean('Brought Dead')
    pa_allergies = fields.Char('Allergies')
    pa_drug = fields.Char('Drug')
    pa_food = fields.Char('Food')
    pa_other = fields.Char('Other')
    pa_review_ge = fields.Text('Review of System General appearance')
#     pa_nose = fields.Char(string='Nose')
#     pa_neck = fields.Char(string='Neck')
#     pa_back = fields.Char(string='Back')
#     pa_extremities = fields.Char(string='Extremities')
#     pa_eyes = fields.Char(string='Eyes')
#     pa_chest = fields.Char(string='Chest')
#     pa_skin = fields.Char(string='Skin')
#     pa_abdomen = fields.Char(string='Abdomen')
    pa_se_rs = fields.Char(string='R.S.')
    pa_se_cvs = fields.Char(string='C.V.S.')
    pa_se_cns = fields.Char(string='C.N.S.')
    pa_se_adb = fields.Char(string='Per abd')
    pa_se_pelvic = fields.Char(string='Pelvic')
    pa_se_rectal = fields.Text(string='Rectal')
#     pa_urine_anal = fields.Text(string='Urine analysis')
#     pa_xray = fields.Text(string='X.ray reviewed by MO')
#     pa_blood_sugar = fields.Text(string='Blood Sugar(by Glucometer)')
#     pa_ecg = fields.Text(string='ECG')
#     pa_diff_diagnosis = fields.Text(string='Differential Diagnosis')
    pa_planofcare = fields.Text(string='Assessment & Plan of Care')
    service_ids = fields.One2many('hospitalization.services', 'services_id')
#     intrim_bill_invoice_id = fields.Many2one('account.invoice',string='INV Invoice', ondelete='cascade', copy=False)


    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.patient_id and record.patient_id.name:
                name += ' - ' + record.patient_id.name
            result.append((record.id, name))
        return result

#     @api.depends('ahpa_height','ahpa_weight')
#     def _get_bmis(self):
#         for rec in self:
#             if rec.ahpa_height:
#                 rec.ahpa_bmi = round((float(rec.ahpa_weight) / ((float(rec.ahpa_height) / 100) ** 2)),2)

#     @api.onchange('prov_mm_diagnosis')
#     def onchange_complain_ids(self):
#         complain = (self.prov_mm_diagnosis - self.prov_mm_diagnosis_dummy)
#         if complain and self.prov_diagnosis:
#             self.prov_diagnosis += str("\n" + complain.name)
#         elif complain and not self.prov_diagnosis:
#             self.prov_diagnosis = complain.name
#         self.prov_mm_diagnosis_dummy = self.prov_mm_diagnosis


#     @api.depends('cm','weight')
#     def _get_bmi(self):
#         for rec in self:
#             if rec.cm:
#                 rec.bmi = round((float(rec.weight) / ((float(rec.cm) / 100) ** 2)),2)

    # @api.onchange('ward_id')
    # def onchange_ward_id(self):
    #     self.bed_id = False

#     # @api.onchange('patient_id')
#     # def onchange_patient_id(self):
#     #     print "==============================",self.patient_id.department_id.name
#     #     self.department_id = self.patient_id.department_id.name

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|',('name',operator,name),('patient_id.name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.model
    def create(self, values):
        if values.get('bed_id', None):
            bed_id = self.bed_id.search([('id', '=', values.get('bed_id', None))])
            if bed_id and bed_id.state != 'free':
                raise ValidationError(_("Bed status not Free!!"))
        res = super(Hospitalization, self).create(values)
        hospitalization_ids = self.env['inpatient.registration'].search([('hospitalization_date','>=',datetime.strftime(datetime.strptime(str(res.hospitalization_date), '%Y-%m-%d %H:%M:%S').date(), '%Y-%m-%d %H:%M:%S')),('hospitalization_date','<=',datetime.strftime(datetime.strptime(str(res.hospitalization_date), '%Y-%m-%d %H:%M:%S').date(), '%Y-%m-%d 23:59:59')),('id','!=',res.id)])
        res.name = self.env['ir.sequence'].with_context(ir_sequence_date=str(datetime.strptime(str(res.hospitalization_date), '%Y-%m-%d %H:%M:%S').date())).next_by_code('inpatient.registration') or ''
        # if hospitalization_ids:
        #     hospitalization = self.env['inpatient.registration'].browse(max(hospitalization_ids.ids))
        #     final_code = "%04d" % (int(hospitalization.name[-4:])+1,)
        #     res.name = res.name[:13] + str(final_code)
        # else:
        #     res.name = res.name[:13] + '0001'
        return res

    def action_confirm(self):
        if self.state == 'confirm' or self.state == 'reserved':
            self.bed_id.write({'state': 'occupied'})
            self.state = 'hosp'
            history_obj = self.env['patient.accomodation.history']
            for rec in self:
                history_obj.create({
                    'inpatient_id': rec.id,
                    'patient_id': rec.patient_id.id,
                    'ward_id':self.ward_id.id,
                    'bed_id':self.bed_id.id,
                    'ward_package_id':self.ward_package_id.id,
                    'start_date':datetime.now(),
                    'department_id': self.department_id.id,
                    'type': 'hosp',
                })

    def action_reserved(self):
        self.bed_id.write({'state': 'reserved'})
        self.state = 'reserved'
        history_obj = self.env['patient.accomodation.history']
        for rec in self:
            history_obj.create({
                'inpatient_id': rec.id,
                'patient_id': rec.patient_id.id,
                'ward_id':rec.ward_id.id,
                'bed_id':rec.bed_id.id,
                'start_date':datetime.now(),
                'type': 'hosp'
            })

    def action_discharge(self):
        if self.state == 'hosp':
            self.bed_id.write({'state': 'free'})
            self.state = 'discharged'
            self.discharge_date = datetime.now()
#             self.patient_id.write({'opd_foc':True,'followup_validity': datetime.now() + dateutil.relativedelta.relativedelta(months=3)})
#             hist_id = self.accomodation_history_ids.search([('inpatient_id','=', self.id), ('bed_id', '=', self.bed_id.id)])
#             if hist_id:
#                 self.accomodation_history_ids.browse([max(hist_id.ids)]).write({'end_date': datetime.now()})

#     @api.multi
#     def action_view_ip_medication(self):
#         return {
#             'name': _('Indoor Patient Medicine Request'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'prescription.order',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id','=',self.patient_id.id)],
#             'context': { 'default_patient_id': self.patient_id.id,
#                          'default_inpatient_registration_code': self.id,
#                          'default_physician_id' :self.primary_physician.id,
#                         }
#                 }

#     @api.multi
#     def action_inpatient_registration_surgery(self):
#         return {
#             'name': _('Surgery'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'inpatient.registration.surgery',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id','=',self.patient_id.id)],
#             'context' : {'default_inpatient_id': self.id, 'default_patient_id': self.patient_id.id,'default_ward_id':self.ward_id.id,'default_bed_id':self.bed_id.id}
#         }

#     @api.multi
#     def action_inpatient_registration_consent(self):
#         return {
#             'name': _('Consent'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'inpatient.consent',
#             'type': 'ir.actions.act_window',
#             'domain': [('consent_patient_name','=',self.patient_id.id)],
#             'context' : {'default_consent_patient_name': self.patient_id.id}
#         }

#     @api.multi
#     def action_view_invoice_hms(self):
#         invoice_ids = self.mapped('invoice_id')
#         imd = self.env['ir.model.data']
#         action = imd.xmlid_to_object('account.action_invoice_tree1')
#         list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
#         form_view_id = imd.xmlid_to_res_id('account.invoice_form')
#         result = {
#             'name': action.name,
#             'help': action.help,
#             'type': action.type,
#             'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
#             'target': action.target,
#             'context': action.context,
#             'res_model': action.res_model,
#             'domain': [('partner_id','=',self.patient_id.user_id.partner_id.id), ('report_type', 'in', ['inpatient']),('id','=',self.invoice_id.id)],
#         }
#         if len(invoice_ids) > 1:
#             result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
#         elif len(invoice_ids) == 1:
#             result['views'] = [(form_view_id, 'form'), (list_view_id, 'tree')]
#             result['res_id'] = invoice_ids.ids[0]
#         else:
#             result = {'type': 'ir.actions.act_window_close'}
#         return result

#     @api.multi
#     def action_view_lab(self):
#         return {
#             'name': _('Investigation'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'hms.investigation',
#             'type': 'ir.actions.act_window',
#             'domain': [('hospitalization_id','=',self.id)],
#             'context': {'default_patient_id': self.patient_id.id,'default_investigation_type':'radiology','default_hospitalization_id': self.id},
#         }

#     @api.multi
#     def action_admission_note(self):
#         return {
#             'name': _('Admission Note'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'admission.note',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id', '=', self.patient_id.id)],
#             'context': {'default_patient_id': self.patient_id.id,'default_hospitalization_id': self.id},
#         }

#     @api.multi
#     def action_cost_estimation_form(self):
#         return {
#             'name': _('Cost Estimation'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'cost.estimation',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id', '=', self.patient_id.id)],
#             'context': {'default_patient_id': self.patient_id.id,'default_hospitalization_id': self.id},
#         }

#     @api.multi
#     def action_create_invoice(self):
#         account_invoice_obj = self.env['account.invoice']
#         account_invoice_line_obj = self.env['account.invoice.line']
#         part_id = self.patient_id.user_id.partner_id
#         for order_id in self:
#             inv = {
#                 'account_id': part_id.property_account_receivable_id.id,
#                 'partner_id': part_id.id,
#                 'patient_id': order_id.patient_id.id,
#                 'date_invoice': fields.date.today(),
#                 'origin': self.name,
#                 'treating_doctor_id':self.primary_physician.id,
#                 'report_type':'inpatient',
#                 'hospital_id':self.id,
#             }
#             inv_id = account_invoice_obj.create(inv)
#             if order_id.surgery_id and order_id.surgery_id.surgery_product_id:
#                 inv_line = {
#                     'product_id': order_id.surgery_id.surgery_product_id.id,
#                     'invoice_id': inv_id.id,
#                     'price_unit':order_id.surgery_id.surgery_product_id.lst_price,
#                     'account_id': order_id.surgery_id.surgery_product_id.property_account_income_id.id,
#                     'uom_id': order_id.surgery_id.surgery_product_id.uom_id.id,
#                     'quantity': 1,
#                     'name':  order_id.surgery_id.surgery_product_id.name
#                 }
#                 acc = account_invoice_line_obj.create(inv_line)
#             # if order_id.accomodation_history_ids:
#             #     for bed_history in order_id.accomodation_history_ids:
#             #         account_id = False
#             #         if bed_history.bed_id.product_id.id:
#             #             account_id = bed_history.bed_id.product_id.property_account_income_id.id
#             #         if not account_id:
#             #             prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#             #             account_id = prop and prop.id or False
#             #         inv_line = {
#             #             'product_id': bed_history.bed_id.product_id.id,
#             #             'name':  bed_history.bed_id.product_id.name,
#             #             'uom_id': bed_history.bed_id.product_id.uom_id.id,
#             #             'price_unit': bed_history.bed_id.product_id.lst_price,
#             #             'invoice_id': inv_id.id,
#             #             'quantity': bed_history.days,
#             #             'account_id': account_id,
#             #         }
#             #         acco = account_invoice_line_obj.create(inv_line)
#             # for surgery in self.env['inpatient.registration.surgery'].search([('inpatient_id', '=', order_id.id)]):
#             #     print "<<<<<<<<sur>>>>>>>>>"
#             #     if surgery.medicament_line:
#             #         print "<<<<<<<>>>>>>>>>"
#             #         for list_medicament in surgery.medicament_line:
#             #             print "for>>>>>>>>>>"
#             #             inv_line = {
#             #                 'product_id': list_medicament.product_id.id,
#             #                 'name':  list_medicament.product_id.name,
#             #                 'uom_id': list_medicament.product_id.uom_id.id,
#             #                 'quantity':list_medicament.qty,
#             #                 'price_unit': list_medicament.product_id.lst_price,
#             #                 'invoice_id': inv_id.id,
#             #                 'account_id': list_medicament.product_id.property_account_income_id.id or account_id,
#             #             }
#             #             print "inv_line >>>>>>>>>>>>>", inv_line
#             #             accr = account_invoice_line_obj.create(inv_line)
#             self.invoice_id = inv_id.id
#         #self.state = 'done'
        
#     #MEDICATION MODEL BLOCK
# #     @api.multi
# #     def button_indoor_medication(self):
# #         inpatient_medi_obj=self.env['prescription.order']
# #         res = {
# #             'name': _('Treatment Sheet'),
# #             'view_type': 'form',
# #             'view_mode': 'form',
# #             'res_model': 'hms.treatment',
# #             'type': 'ir.actions.act_window',
# #             'context': {
# #                         'default_patient_id': self.patient_id.id,
# #                         'default_diagnosis_id': self.admission_reason.id,
# #                         'default_attending_physician_ids': self.attending_physician_ids.ids,
# #                         'default_pres_group_id': self.treatment_ids.pres_group_id.id or False,
# #                         'default_hospitalization_id': self.id,
# #                         'from_button':self.id
# #                         },
# #             'target': 'new',
# #             'flags': {'form': {'action_buttons': True}},
# #         }
# #         return res
    
#     #INTRIM BILL INVOICE START
#     @api.multi
#     def create_intrim_bill(self):
#         imd = self.env['ir.model.data']
#         action = imd.xmlid_to_object('account.action_invoice_tree1')
#         list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
#         form_view_id = imd.xmlid_to_res_id('account.invoice_form')
#         account_invoice_obj = self.env['account.invoice']
#         account_invoice_line_obj = self.env['account.invoice.line'] 
#         lst = []
#         order_id = self

#         #Package#
#         account_id = False
#         if self.ward_package_id.id:
#             account_id = self.ward_package_id.property_account_income_id.id
#         if not account_id:
#             prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#             account_id = prop and prop.id or False
#         inv_line = {
#             'name': order_id.ward_package_id.name,
#             'price_unit': order_id.ward_package_id.lst_price,
#             'account_id': account_id,
#             'quantity': 1,
#             'discount': 0.0,
#             'uom_id': order_id.ward_package_id.uom_id.id,
#             'product_id': order_id.ward_package_id.id,
#             'account_analytic_id': False,
#         }
#         lst.append((0,0,inv_line))
        
#         #Service#
#         product_id_list = [product.hospitalisatione_service.id  for product in order_id.service_ids]
#         new_product_list = set(product_id_list)
#         for product in new_product_list:
#             quantity = 0
#             for record_line in order_id.service_ids:
#                 if record_line.hospitalisatione_service.id == product :
#                     quantity +=1
#                     line = record_line
#             account_id = line.hospitalisatione_service.property_account_income_id.id
#             if not account_id:
#                 prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#                 account_id = prop and prop.id or False
#             inv_line = {
#                 'name': line.hospitalisatione_service.name,
#                 'inv_date':line.date_time_service,
#                 'price_unit': line.hospitalisatione_service.lst_price,
#                 'account_id': account_id,
#                 'quantity': quantity,
#                 'discount': 0.0,
#                 'uom_id': line.hospitalisatione_service.uom_id.id,
#                 'product_id': line.hospitalisatione_service.id,
#                 'account_analytic_id': False,
#             }
#             lst.append((0,0,inv_line))
#         for order_id in self:
#             inv = {
#                 'account_id': order_id.patient_id.partner_id.property_account_receivable_id.id,
#                 'partner_id': order_id.patient_id.partner_id.id,
#                 'patient_id': order_id.patient_id.id,
#                 'type': 'out_invoice',
#                 'name': order_id.name,
#                 'origin': order_id.name,
#                 'currency_id': order_id.env.user.company_id.currency_id.id,
#                 'report_type': 'hospital',
#                 'appointment_id': order_id.id,
#                 'consultant_doctor_id':order_id.patient_id.primary_doctor.id,
#                 'treating_doctor_id':order_id.patient_id.primary_doctor.id,
#                 'invoice_line_ids':lst,
#             }
#             inv_id = account_invoice_obj.create(inv)
#         self.intrim_bill_invoice_id = inv_id.id
#         result = {
#             'name': action.name,
#             'help': action.help,
#             'type': action.type,
#             'views': [[form_view_id, 'form'],[list_view_id, 'tree'],[False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
#             'target': action.target,
#             'res_model': action.res_model,
#             'res_id': inv_id.id,
#             'domain': [
#                 ('report_type', 'in', ['hospital'])
#             ],
#             #'context': context,
#         }
#         return result


#         # inv_obj = self.env['account.invoice']
#         # ir_property_obj = self.env['ir.property']
#         # inv_line_obj = self.env['account.invoice.line']
#         # account_id = False
#         # invoice_id = False
#         # res = {
#         #     'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
#         #     'partner_id': self.patient_id.partner_id.id,
#         #     'patient_id': self.patient_id.id,
#         #     'type': 'out_invoice',
#         #     'name': self.name,
#         #     'origin': self.name,
#         #     'currency_id': self.env.user.company_id.currency_id.id,
#         #     'report_type': 'hospital',
#         #     'appointment_id': self.id,
#         #     'consultant_doctor_id':self.patient_id.primary_doctor.id,
#         #     'treating_doctor_id':self.patient_id.primary_doctor.id,
#         # }


#         # invoice = inv_obj.create(res)
#         # if self.service_ids.date_time_service in invoice.invoice_line_ids.mapped('inv_date') and self.service_ids.hospitalisatione_service.id in invoice.invoice_line_ids.mapped('product_id'):
#         #     print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         # inv_line = []
#         # #Services
#         # for line in self.service_ids:
#         #     if line.audit_checkbox == True:
#         #         account_id = line.hospitalisatione_service.property_account_income_id.id
#         #         if not account_id:
#         #             prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
#         #             account_id = prop and prop.id or False
#         #         inv_line.append((0, 0, {
#         #             'name': line.hospitalisatione_service.name,
#         #             #'inv_date':line.date_time_service,
#         #             'price_unit': line.hospitalisatione_service.lst_price,
#         #             'account_id': account_id,
#         #             'quantity': 1.0,
#         #             'discount': 0.0,
#         #             'uom_id': line.hospitalisatione_service.uom_id.id,
#         #             'product_id': line.hospitalisatione_service.id,
#         #             'account_analytic_id': False,
#         #         }))
#         #         print "***********************************8",inv_line
#         # res['invoice_line_ids'] = inv_line
        
#         # self.intrim_bill_invoice_id = invoice.id
#     #INTRIM BILL INVOICE END


#     @api.multi
#     def button_indoor_medication(self):
#         inpatient_medi_obj=self.env['prescription.order']
#         treatment_ids = self.env['hms.treatment'].search([('hospitalization_id','=',self.id)])
#         treatment = False
#         if treatment_ids:
#             latest_treatment_id = max(treatment_ids.ids)
#             treatment = self.env['hms.treatment'].browse(latest_treatment_id)
#         res = {
#             'name': _('Treatment Sheet'),
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'hms.treatment',
#             'type': 'ir.actions.act_window',
#             'context': {
#                         'default_patient_id': self.patient_id.id,
#                         'default_diagnosis_id': self.admission_reason.id,
#                         'default_attending_physician_ids': self.attending_physician_ids.ids,
#                         'default_pres_group_id': treatment and treatment.pres_group_id.id or False,
#                         'default_hospitalization_id': self.id,
#                         },
#             'target': 'new',
#             'flags': {'form': {'action_buttons': True}},
#         }
#         return res


#     @api.multi
#     def button_progress_note(self):
#         progress_note_ids = self.env['hms.progress.note'].search([('hospitalization_id','=',self.id)])
#         progress = False
#         if progress_note_ids:
#             latest_progress_note_id = max(progress_note_ids.ids)
#             progress = self.env['hms.progress.note'].browse(latest_progress_note_id)
#         res = {
#             'name': _('Progress Note'),
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'hms.progress.note',
#             'type': 'ir.actions.act_window',
#             'context': {
#                         'default_patient_id': self.patient_id.id,
#                         'default_hospitalization_id': self.id,
#                         },
#             'target': 'new',
#             'flags': {'form': {'action_buttons': True}},
#         }
#         return res

    def action_cancel(self):
        self.state = 'cancel'
        for data in self:
            data.bed_id.write({'state': 'free'}) 

    def action_done(self):
        self.state = 'done'
        # result = []
#         for hospital in self:
#             if hospital.surgery_id:
#                 result.append((0,0,{
#                     'name': hospital.surgery_id.name,
#                     'description': hospital.surgery_id.description,
#                     'diseases':hospital.admission_reason.id,
#                     'patient_id':hospital.patient_id.id,
#                     'surgery_product_id':hospital.surgery_id.surgery_product_id,
#                 }))
#             self.patient_id.surgery = result

#     @api.multi
#     def action_draft(self):
#         self.state = 'draft'

    def action_create_confirm(self):
        self.state = 'confirm'
        app_obj = self.env['banastech.hms.appointment']
        appointments_ids = app_obj.search([('patient_id','=',self.patient_id.id),('state','=','done')])
        if appointments_ids:
            latest_appointment_id = max(appointments_ids.ids)
            latest_appointment = app_obj.browse(latest_appointment_id)
    #         self.opd_note = latest_appointment.chief_complain {opd_note field in }

#     @api.multi
#     def write(self,values):  
#         if self.state == 'done':
#             raise UserError(_('Hospitalization is Already Done, You can not change any Record Now. Conatct your Administrator for more Information.'))
#         else:
#             res = super(Hospitalization, self).write(values)
#             for data in self:
#                 if data.state == 'hosp':
#                     data.patient_id.write({'patient_status': 'Hospitalized'})
#                 elif data.state == 'discharged':
#                     data.patient_id.write({'patient_status': 'Discharged'})
#                 if data.tpa_id.id:
#                     data.hospital_ot.write({'state': 'occupied', 'patient_id': data.patient_id.id, 'hospitalize_id': data.id, 'start_date': data.start_date, 'end_date': data.end_date})
#             return res

    # @api.model
    # def view_discharge_summary(self):
    #     if self.state in ['hosp','discharged','done']:
    #         op_value = ''
    #         for rec in self:
    #             for history in rec.accomodation_history_ids:
    #                 if self.bed_id == history.bed_id:
    #                     history.end_date = datetime.now()
    #             if rec.surgery_id and rec.surgery_id.description:
#                     op_value += "Name of Operation :" + rec.surgery_id.description
#                     if rec.start_date:
#                         op_value += '(' + str((datetime.strptime(rec.start_date, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5,minutes=30)).strftime("%d-%m-%Y %I:%M %p"))+ ')'
#                 if rec.side:
#                     op_value += '\nSide : ' + rec.side
#                 if rec.incision:
#                     op_value += '\nIncision : ' + rec.incision
#                 if rec.approach:
#                     op_value += '\nApproch : ' + rec.approach
#                 if rec.procedure:
#                     op_value += '\nProcedure : ' + rec.procedure
#                 if rec.implant_name and rec.implant_name.name:
#                     op_value += '\nImplant Name : ' + rec.implant_name.name
#                 if rec.implant_company and rec.implant_company.name:
#                     op_value += '\nCompany Name : ' + rec.implant_company.name
#                 if rec.implant_size:
#                     op_value += '\nImpant Size :' + rec.implant_size
#                 rec.latest_op_note = op_value
#                 rec.past_surgical_history = rec.phc_past_surgical_history
#                 rec.past_history = (rec.diabetes_mel or '')+ "\n" + (rec.hypertension or '' )+ "\n" + (rec.other_illness or '')

    @api.model
    def done_discharge_summary(self, fields):
        self.done_summary = True

#     @api.multi
#     def action_estimate_report(self):
#         estimate_ids = self.env['hms.estimate'].search([('inpatient_id','=',self.id)], limit=1)
#         if estimate_ids:
#             return self.env['report'].get_action(estimate_ids, 'shah_estimate.report_hospital_estimate_document')
#         else :
#             raise UserError(('No Estimate Report Exists.'))

#     @api.multi
#     def action_zero_report(self):
#         insurance_ids = self.env['hms.insurance.zero_error'].search([('hosp_id','=',self.id)], limit=1)
#         if insurance_ids:
#             return self.env['report'].get_action(insurance_ids, 'hms_insurance.report_zero_error_document')
#         else:
#             raise UserError(('No 0-0 Report Exists.'))

#     @api.multi
#     def action_discharge_report(self):
#         return self.env['report'].get_action(self, 'hms_hospitalization.report_hospital_discharge_document')

#     @api.multi
#     def action_hospitalization_surgery_form(self):
#         action = self.env.ref('hms_hospitalization.action_hospitalization_surgery_form')
#         form_view_id = self.env.ref('hms_hospitalization.view_hospitalization_surgery_form')
#         result = {
#             'name': 'Surgery',
#             'help': action.help,
#             'type': action.type,
#             'views': [[form_view_id.id, 'form']],
#             'target': action.target,
#             'context': action.context,
#             'res_model': action.res_model,
#             'domain': [('id','=',self.id)],
#         }
#         if len(self.ids) == 1:
#             result['views'] = [(form_view_id.id, 'form')]
#             result['res_id'] = self.ids[0]
#         else:
#             result = {'type': 'ir.actions.act_window_close'}
#         return result


class WardRoundDetail(models.Model):
    _name = "ward.round.detail"
    _rec_name="name"

    name = fields.Char('Name')


# class Anaesthesia(models.Model):
#     _name = "anaesthesia"
#     _rec_name="name"

#     name = fields.Char('Anaesthesia Name', required=True)


class HospitalizationTpa(models.Model):
    _name = "hospitalization.tpa"

    name = fields.Char(string='Name')


#Admission Checklist
class AdmissionCheckListTemplate(models.Model):
    _name="inpatient.checklist.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")


class AdmissionCheckList(models.Model):
    _name="inpatient.checklist"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    inpatient_id = fields.Many2one("inpatient.registration", ondelete="cascade", string="Hospitalization")

# # class PreoperativeInvestigationTemplate(models.Model):
# #     _name = 'preoperative.investigation.template'

# #     name = fields.Char(string="Investigation")

# # class PreoperativeInformationTemplate(models.Model):
# #     _name = 'preoperative.information.template'

# #     name = fields.Char(string="Content")


# class PreOpetativeCheckList(models.Model):
#     _name="pre.operative.check.list"

#     name = fields.Char(string="Name")
#     is_done = fields.Boolean(string="Done", default=False)
#     remark = fields.Char(string="Remarks")
#     inpatient_id = fields.Many2one("inpatient.registration", ondelete="cascade", string="Hospitalization")


# #Pre Ward Checklist
# class PreWardCheckListTemplate(models.Model):
#     _name="pre.ward.check.list.template"

#     name = fields.Char(string="Name")
#     remark = fields.Char(string="Remarks")


# class PreWardCheckList(models.Model):
#     _name="pre.ward.check.list"

#     name = fields.Char(string="Name")
#     is_done = fields.Boolean(string="Transferring Nurse", default=False)
#     is_done1 = fields.Boolean(string="Receiving Nurse (OT)", default=False)
#     is_done2 = fields.Boolean(string="Transferring Nurse", default=False)
#     is_done3 = fields.Boolean(string="Receiving Nurse (Ward/ICU)", default=False)
#     remark = fields.Char(string="Remarks")
#     inpatient_id = fields.Many2one("inpatient.registration", ondelete="cascade", string="Hospitalization")

# #Patient Accomodation History
class PatientAccomodationHistory(models.Model):
    _name = "patient.accomodation.history"
    _rec_name = "patient_id"

    @api.model
    def _rest_days(self):
        # self.ensure_one()
        for registration in self:
            if registration.end_date and registration.start_date:
                diff = (datetime.strptime(registration.end_date, DEFAULT_SERVER_DATETIME_FORMAT) - datetime.strptime(registration.start_date, DEFAULT_SERVER_DATETIME_FORMAT)).days
                self.days = diff if diff > 0 else 1
            else:
                self.days = 0

    inpatient_id = fields.Many2one('inpatient.registration', ondelete="cascade", string='Inpatient', required=True)
    patient_id = fields.Many2one('banastech.hms.patient', ondelete="restrict", string='Patient', required=True)
    ward_id = fields.Many2one('banastech.hms.ward', ondelete="restrict", string='Ward/Room')
    bed_id = fields.Many2one('banastech.hms.bed', ondelete="restrict", string='Bed No.')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    days = fields.Integer(compute=_rest_days, string='Total Rest Days')
    type = fields.Selection([('hosp', 'Hospitalization'), ('surgery', 'Surgery')], string="Type")
    department_id = fields.Many2one("banas.hms.department", "Department")
    ward_package_id = fields.Many2one('product.product',ondelete="restrict",string='Package',domain=[('is_observer','=',True)])

# class IndimediReason(models.Model):
#     _name= "hms.reason"

#     name = fields.Char(string="Reason")


# class StoneNotes(models.Model):
#     _name = 'hospital_stone'

#     name = fields.Char(string='Name')


# class StoneLines(models.Model):
#     _name = 'hospital_stone_line'

#     stone = fields.Many2one('hospital_stone', ondelete="cascade", string='Description')
#     size = fields.Integer(string='Size')
#     mm_label = fields.Char(' ', readonly=True,default='mm')
#     inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')


# class ProstateNotes(models.Model):
#     _name = 'hospital_prostate'

#     name = fields.Char(string='Name')


# class ProstateLines(models.Model):
#     _name = 'hospital_prostate_line'

#     prostate = fields.Many2one('hospital_prostate', ondelete="cascade", string='Description')
#     size = fields.Integer('Size')
#     inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')


# class ReconstructiveNotes(models.Model):
#     _name = 'hospital_reconstructive'

#     name = fields.Char(string='Name')


# class ReconstructiveLines(models.Model):
#     _name = 'hospital_reconstructive_line'

#     reconstructive = fields.Many2one('hospital_reconstructive', ondelete="cascade", string='Description')
#     size = fields.Integer(string='Size')
#     inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')


# class AblativeNotes(models.Model):
#     _name = 'hospital_ablative'

#     name = fields.Char(string='Name')


# class AblativeLines(models.Model):
#     _name = 'hospital_ablative_line'

#     ablative = fields.Many2one('hospital_ablative', ondelete="cascade", string='Description')
#     size = fields.Integer(string='Size')
#     inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')


# class FemaleUrologyNotes(models.Model):
#     _name = 'hospital_female_urology'

#     name = fields.Char(string='Name')


# class FemaleUrologyLines(models.Model):
#     _name = 'hospital_female_urology_line'

#     female_urology = fields.Many2one('hospital_female_urology', ondelete="cascade", string='Description')
#     size = fields.Integer(string='Size')
#     inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')


# class OncoUrologyNotes(models.Model):
#     _name = 'hospital_onco_urology'

#     name = fields.Char(string='Name')


# class OncoUrologyLines(models.Model):
#     _name = 'hospital_onco_urology_line'

#     onco_urology = fields.Many2one('hospital_onco_urology', ondelete="cascade", string='Description')
#     size = fields.Integer(string='Size')
#     inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')


class WardRounds(models.Model):
    _name = "ward.rounds"
    _rec_name = 'instruction'

    instruction = fields.Many2one("ward.round.detail", ondelete="restrict", string='Instruction')
    remarks = fields.Char(string='Remarks')
    round_id = fields.Many2one('inpatient.registration', ondelete="restrict",string='Inpatient')
    date = fields.Date(string='Date')
    execution_time = fields.Datetime(string='Execution Time')
    executed_by = fields.Many2one('res.users', ondelete="restrict", string='Executed By', domain=[('is_observer','=',True),('is_nurse','=',True)])

# class IndimediAppointment(models.Model):
#     _inherit = 'banastech.hms.appointment'

#     hospital_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Hospitalization', help="Enter the patient hospitalization code",invisible=True)
#     past_surgeries_ids= fields.One2many('past.surgeries', 'appointment_id', string='Past Surgeries')

#     @api.multi
#     def button_hospitalize(self):
#          return {
#             'name': _('Hospitalizations'),
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'inpatient.registration',
#             'type': 'ir.actions.act_window',
#             'domain': [('patient_id','=',self.patient_id.id)],
#             'context': {'default_patient_id': self.patient_id.id,'default_appointment_id': self.id},
#         }

#     @api.multi
#     def appointment_waiting(self):
#         res = super(IndimediAppointment, self).appointment_waiting()
#         if self.patient_id.past_surgeries_ids:
#             self.past_surgeries_ids = self.patient_id.past_surgeries_ids
#         return res

#     @api.multi
#     def appointment_done(self):
#         if self.past_surgeries_ids:
#             self.patient_id.past_surgeries_ids = self.past_surgeries_ids
#         return super(IndimediAppointment, self).appointment_done()
# class ResCompany(models.Model):
#     _inherit = "res.company"

#     registration_date = fields.Char(string='Date of Registration')
#     pan_no_hosp = fields.Char(string='PAN No')

class ResPartnerHospitalization(models.Model):
    _inherit = "res.partner"

    is_nurse = fields.Boolean("Nurse")
    is_observer = fields.Boolean("Observer")
#     is_anesthetist = fields.Boolean("Anesthetist")
#     is_medicalofficer = fields.Boolean("Medical Officer")
#     vendors_cin = fields.Char(string='CIN')
#     vendors_gst_no = fields.Char(string='GST No.')
#     vendors_dl_no = fields.Char(string='Dl. No.')
#     vendors_dl_exp_date = fields.Datetime(string='DL Exp. Date',default=fields.Datetime.now)
#     vendors_dl_date_check = fields.Datetime(string='DL Exp',default=fields.Datetime.now)
#     vendors_dl_exp_true = fields.Boolean(string='Exp.')

#     @api.model
#     def create(self, values):
#         res = super(ResPartnerHospitalization, self).create(values)
#         diff = (datetime.strptime(res.vendors_dl_exp_date, DEFAULT_SERVER_DATETIME_FORMAT) - datetime.strptime(res.vendors_dl_date_check, DEFAULT_SERVER_DATETIME_FORMAT)).days
#         if diff < 7:
#             res.vendors_dl_exp_true = True
#         return res

# class AdmissionNote(models.Model):
#     _name = 'admission.note'
#     _rec_name = 'patient_id'

#     patient_id = fields.Many2one('hms.patient', string="Patient",)
#     hospitalization_id = fields.Many2one('inpatient.registration', string = 'Hospitalization')
#     inpatient_id = fields.Many2one("inpatient.registration", ondelete="cascade", string="Hospitalization")
#     surgery_id = fields.Many2many('hms_surgery','hosp_patient_surgery','hosp_id','surgery_id', ondelete="restrict", string='Surgery')
#     consultant_id = fields.Many2one('hms.physician', string='Consultant')
#     ad_note_diagnosis_id = fields.Many2one('hms.diseases',string='Diagnosis')
#     surgery_datetime = fields.Datetime(string="Date & Time of Surgery", default=fields.Datetime.now)
#     orally_after = fields.Char(string="Nothing orally after:")
#     food_before = fields.Char(string="Solid food before:")
#     liquid_allow = fields.Char(string="Liquids allowed till")
#     medicines = fields.Text(string="Medicines")
#     inv_to_done = fields.Text(string="Investigations to be done:")
#     pcv_ffp = fields.Char(string="Arrangement of PCV/FFP:")
#     colon_prep = fields.Char(string="Colon Preparation:")
#     phy_ref = fields.Char(string="Physician Reference:")
#     anesthesia_ref = fields.Char(string="Anesthesia Reference:")
#     other_instruction = fields.Char(string="Others:")
#     iv_fluids = fields.Char(string="IV Fluids:")
#     iv_antibiotics = fields.Char(string="IV Antibiotics:")
#     dvt_prophylaxis = fields.Char(string="DVT Prophylaxis")
#     others_op_order = fields.Char(string="Others:")


class HMSSurgeryDietician(models.Model):
    _name = 'hms.surgery.dietician'
    _description = 'Dietician'
    _rec_name = 'hms_surgery_dietician_id'

    date_dietician = fields.Datetime('Date', required="True",default=fields.Datetime.now)
    patient_id = fields.Many2one('banastech.hms.patient',ondelete="restrict", string='Patient')
    diet_height = fields.Float('Height(cm)', digits=(16,2))
    diet_weight = fields.Float('Weight(kg)')
    diet_bmi = fields.Float(string='BMI', digits=(16,2), compute="_get_bmi_diet", store=True)
    diet_past_clinical_history = fields.Text(string="Past Clinical History")
    diet_bio_chemical = fields.Text(string="Bio-Chemical Parameters")
    diet_meals = fields.Char(string="Meals Eaten/Day")
    diet_gi_symptoms = fields.Many2many('dietician.gi.symptoms',string="GI Symptoms")
    diet_typesoffeeds = fields.Selection([('fd','Full Diet'),('sd','Soft Diet'),('ld','Liquid Diet'),('rtf','RT Feed'),('nbm','NBM'),('ao','Any Other')],string="Types of Feed")
    diet_typesoffeeds_value = fields.Char(string="Value")
    diet_well_nourished = fields.Char(string="Well Nourished(A)")
    diet_moderatery = fields.Char(string="Moderately Mainourished(B)")
    diet_severely = fields.Char(string="Severely Mainourished(C)")
    hms_surgery_dietician_id = fields.Many2one('inpatient.registration',ondelete="restrict",string="Dietician")

    @api.depends('diet_height','diet_weight')
    def _get_bmi_diet(self):
        for rec in self:
            if rec.diet_height:
                rec.diet_bmi = round((float(rec.diet_weight) / ((float(rec.diet_height) / 100) ** 2)),2)

class GISymptoms(models.Model):
    _name = 'dietician.gi.symptoms'

    name = fields.Char('Name')

class HMSProgessNote(models.Model):
    _name = 'hms.progress.note'

    patient_id = fields.Many2one('banastech.hms.patient', 'Patient')
#     patient_progess_ids = fields.One2many('patient.progess','patient_progess_id',string="Patient Progess")
    oral_rt = fields.Float(string="Oral/RT")
    fj_nj = fields.Float(string="FJ/NJ")
    iv_fluids = fields.Float(string="IV Fluids")
    io_total_input = fields.Float(string="Total Input",compute="_get_total_input")
#     ib = fields.Float(string="I/B(ml)")
#     ib_value = fields.Char(string="Value")
#     cb = fields.Float(string="C/B(ml)")
#     cb_value = fields.Char(string="Value")
#     stool = fields.Float(string="Stool")
#     stool_value = fields.Char(string="Value")
#     icd1 = fields.Float(string="ICD 1(ml)")
#     icd1_value = fields.Char(string="Value")
#     icd2 = fields.Float(string="ICD 2(ml)")
#     icd2_value = fields.Char(string="Value")
#     pcd1 = fields.Float(string="PCD 1(ml)")
#     pcd1_value = fields.Char(string="Value")
#     pcd2 = fields.Float(string="PCD 2(ml)")
#     pcd2_value = fields.Char(string="Value")
#     urine = fields.Float(string="Urine(ml)")
#     urine_value = fields.Char(string="Value")
#     rt_aspirates = fields.Float(string="RT aspirates(ml)")
#     rt_aspirates_value = fields.Char(string="Value")
#     drain1 = fields.Float(string="Drain-1(ml)")
#     drain1_value = fields.Char(string="Value")
#     drain2 = fields.Float(string="Drain-2(ml)")
#     drain2_value = fields.Char(string="Value")
#     total_output = fields.Float(string="Total Output",compute="_get_total_output")
#     total_output_value = fields.Char(string="Value")
    important_event = fields.Text(string='Important Event')
    todays_plan = fields.Text(string="Today's Plan")
    hospitalization_id = fields.Many2one('inpatient.registration',string='Hospitalization')

    @api.depends('oral_rt', 'fj_nj', 'iv_fluids')
    def _get_total_input(self):
        for ip in self:
            ip.io_total_input = ip.oral_rt+ip.fj_nj+ip.iv_fluids

#     @api.depends('ib','cb','stool','icd1','icd2','pcd1','pcd2','urine','rt_aspirates','drain1','drain2')
#     def _get_total_output(self):
#         for op in self:
#             op.total_output = op.ib+op.cb+op.stool+op.icd1+op.icd2+op.pcd1+op.pcd2+op.urine+op.rt_aspirates+op.drain1+op.drain2

# class HMSPatientProgess(models.Model):
#     _name = 'patient.progess'

#     date = fields.Date(string="Date")
#     chief_complain = fields.Char(string="Chief Complain")
#     temp = fields.Char(string="Temp")
#     progess_note_pain_score = fields.Selection([('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'), ('nine', '9'), ('ten', '10')], default="one",string="Pain Score")
#     pulse = fields.Char(string="Pulse")
#     respiration = fields.Char(string="Respiration")
#     spo2 = fields.Char(string="Spo2")
#     bp = fields.Char(string="BP")
#     stool = fields.Char(string="Stool")
#     urine = fields.Char(string="Urine")
#     login = fields.Many2one('res.users', string="Login", default=lambda self: self.env.user, readonly="True")
#     patient_progess_id = fields.Many2one('hms.progress.note',string="Patient Progess")


class PhyNotes(models.Model):
    _name = 'phy.notes'

    inpatient_id = fields.Many2one("inpatient.registration", ondelete="cascade", string="Hospitalization")
    phy_notes_date = fields.Datetime(string="Date & Time", default=fields.datetime.today())
    phy_particulars = fields.Char(string="Particulars")
    assess_phy_id = fields.Many2one('res.users', string="Physiotherapist", default=lambda self: self.env.user)


class SignLABReports(models.Model):
    _name = 'significant.lab.report'

    report_date = fields.Date('Date',default=datetime.now())
    report_name = fields.Char('Test')
    report_result = fields.Char('Result')
    report_attachment = fields.Binary(string='Attachment')
    sign_labreport_id = fields.Many2one('inpatient.registration',string="Lab Reports")

class PHOperation(models.Model):
  _name = 'ph.operation'

  pho_date = fields.Datetime(string='Date')
  pho_diagnosis = fields.Char(string='Diagnosis')
  pho_result = fields.Char(string="Result")
  pho_drhosp = fields.Char(string="Doctor/Hospital")
  pho_id = fields.Many2one('inpatient.registration',string="PHO")

class PHHospitalization(models.Model):
  _name = 'ph.hospitalization'

  phh_diagnosis = fields.Char(string='Diagnosis')
  phh_year = fields.Char(string="Year")
  phh_duration = fields.Char(string="Duration")
  phh_id = fields.Many2one('inpatient.registration',string="PHH")

class PersonalsHistoryID(models.Model):
  _name = 'personals.history.id'

  name = fields.Selection([('diet','Diet'),('sleep','Sleep'),('micturition','Micturition'),('bowel_habits','Bowel Habits')],string="Personal History")
  value = fields.Char(string='Value')
  personals_history_id = fields.Many2one('inpatient.registration',string="Personal History")

class PersonalsHistorysID(models.Model):
  _name = 'personals.historys.id'

  name = fields.Selection([('smoking','Smoking'),('alcohol','Alcohol'),('drugs','Drugs'),('tabacco','Tobacco')],string="Addiction History")
  value = fields.Boolean(string='Y/N')
  duration = fields.Char(string='Value')
  personals_historys_id = fields.Many2one('inpatient.registration',string="Personal History")

class AHPSAllergies(models.Model):
    _name = 'ahps.allergies'

    allergicto = fields.Char(string='Allergic to')
    reaction = fields.Char(string='Reaction')
    ahps_allergies_id = fields.Many2one('inpatient.registration',string='Allergies')

class HMSDoctorBMIRecord(models.Model):
    _name = 'bmi.line.by.doctor'

    weight = fields.Float('Weight(kg)')
    cm = fields.Float('Height(cm)', digits=(16,2))
    bmi = fields.Float('BMI',compute="_get_bmi",digits=(16,2), store=True)
    bmi_line_by_doctor_id = fields.Many2one('inpatient.registration', string="BMI")

    @api.depends('cm','weight')
    def _get_bmi(self):
        for rec in self:
            if rec.cm:
                rec.bmi = round((float(rec.weight) / ((float(rec.cm) / 100) ** 2)),2)

# class ProvMMDiagnosis(models.Model):
#     _name = 'prov.mm.diagnosis'

#     name = fields.Char(string='Prov. Diagnosis',required=True)

class HospitalisationServices(models.Model):
    _name = 'hospitalization.services'

    services_id = fields.Many2one('inpatient.registration')
    date_time_service = fields.Date(string="Date",default=fields.Date.context_today)
    hospitalisatione_service = fields.Many2one('product.product', string="Service")
    audit_checkbox = fields.Boolean(string="Checked?")
    hospitalisation_service_provider_id = fields.Char(string="Provider", default=lambda self: self.env.user.name)
    hospitalisation_service_auditor  = fields.Char(string="Auditor", default=lambda self: self.env.user.name)

class ByDoctorPastHistory(models.Model):
    _name = 'by.doctor.past.history'

    by_dr_disease = fields.Many2one('past.history.disease',string='Disease')
    by_dr_since = fields.Char(string='Since')
    by_dr_medication = fields.Char(string='On Medication')
    by_dr_tr_doctor = fields.Char(string='Treating Doctor')
    by_doctor_past_history_id = fields.Many2one('inpatient.registration',string='Past History')

class PastHistoryDisease(models.Model):
    _name = 'past.history.disease'

    name = fields.Char(string='Name')


# class InheritAccountInvoiceLine(models.Model):
#     _inherit = 'account.invoice.line'

#     inv_date = fields.Date(string='Date')