from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import base64

class s1_image_zoom(http.Controller):

    @http.route(['/appointment/past_investigation/<model("hms.appointment"):appointment>'], type='http', auth="public", website=True)
    def appointment_doc_s1(self, appointment=False, **kwargs):
    	print "=============app=============",appointment,kwargs
        return request.website.render("hms_image_zoom.image_session_1_preview", {'record_s1': appointment})