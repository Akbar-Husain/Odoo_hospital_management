from odoo import http
from odoo.http import request


class DoctorController(http.Controller):

	@http.route(['/hms_doctor'], type="http", auth="public", website=True)
	def doctor(self):
		doctors = request.env['banas.hms.doctor'].sudo().search([])
		values = {
			'records': doctors,
		}
		return request.render("banastech_hms.hms_doctor_cont", values)



	@http.route(['/hms_doctor/%s'], type='http', auth='public', website=True, method=['GET'])
	def doctor_submit(self, **kw):
		doctor_user = request.env['banas.hms.doctor'].sudo().search([('user_id', '!=', False)])
		print("..........................",doctor_user)
		doctor_list = []
		for doctor in doctor_user:
			doctor_list.append({
				'name': doctor.name,
				# 'code': doctor.code,
				'email': doctor.email,
				# 'specialty': doctor.specialty,
				'mobile': doctor.mobile,
				'city': doctor.city,
			})
			print(">>>>>>>>>>>>>>>>>>>>>>>>",doctor_user)
		print("..||||||||||||||.",doctor_user)
		return request.render('banastech_hms.doctor_details', {'doctor_list': doctor_list})
		# return request.redirect('/my_model/success')
