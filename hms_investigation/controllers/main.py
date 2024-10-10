# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request
from openerp.tools.translate import _
import base64

class hms_image_zoom(http.Controller):

    @http.route('/hms/multi_attach', auth="public", website=True, type='http', csrf=False)
    def multi_attach(self, **kwargs):
        Model = request.session.model('document.management')
        attachment_id = Model.create({
            'is_document': base64.encodestring(kwargs['ufile'].read()),
            'multi_seq': kwargs['multi_seq'],
            'name': kwargs['ufile'].filename,
        }, request.context)

    @http.route(['/investigation/<model("hms.investigation"):investigation>'], type='http', auth="public", website=True)
    def investigation_doc(self, investigation=False, **kwargs):
        return request.website.render("hms_image_zoom.image_preview", {'record': investigation})

    @http.route(['/patient/appointment/<model("hms.appointment"):appointment>'], type='http', auth="public", website=True)
    def investigation_doc_old(self, appointment=False, **kwargs):
        ret = []
        domain = [('patient_id', '=', appointment.patient_id.id), ('investigation_type', '=', 'radiology')]
        if appointment.state != 'done':
            domain += '|', ('appointment_id', '!=', appointment.id), ('appointment_id', '=', False)
        investigation_ids = request.env['hms.investigation'].search(domain)
        for inv in investigation_ids:
            if inv.doc_ids:
                ret.append(inv)
        return request.website.render("hms_image_zoom.image_preview", {'record': ret})

    @http.route(['/appointment/<model("hms.appointment"):appointment>'], type='http', auth="public", website=True)
    def appointment_doc(self, appointment=False, **kwargs):
        ret = []
        investigation_ids = request.env['hms.investigation'].search([('appointment_id', '=', appointment.id)])
        for inv in investigation_ids:
            if inv.doc_ids:
                ret.append(inv)
        return request.website.render("hms_image_zoom.image_preview", {'record': ret})

    @http.route(['/patient/<model("hms.patient"):patient>'], type='http', auth="public", website=True)
    def patient_doc(self, patient=False, **kwargs):
        return request.website.render("hms_image_zoom.image_preview", {'record': patient})

