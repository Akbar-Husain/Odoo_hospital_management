from openerp import api, models
from openerp.exceptions import UserError


class AppointmentPrescriptionReport(models.AbstractModel):
    _name = 'report.shah_opd.report_prescription_order_app'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('shah_opd.report_prescription_order_app')
        order_ids = None

        if report.model == 'hms.appointment':
            order_ids = self.env['prescription.order'].search([('appointment', 'in', self._ids)])
        else:
            order_ids = self.env[report.model].browse(list(self._ids))
        if order_ids.prescription:
            docargs = {
                'doc_ids': self._ids,
                'doc_model': report.model,
                'docs': order_ids,
            }
            return report_obj.render('shah_opd.report_prescription_order_app', docargs)
        else :
            raise UserError(('No Prescription Report.'))

