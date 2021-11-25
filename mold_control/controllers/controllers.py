# -*- coding: utf-8 -*-

import json

from odoo import fields, http, tools, _
from odoo.http import request, Response
from odoo.exceptions import ValidationError
from odoo.addons.web.controllers.main import content_disposition


CONTENT_TYPE = {
	"docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
	"jpeg": "image/jpeg",
	"jpg": "image/jpeg",
	"pdf": "application/pdf",
	"png": "image/png",
	"ppt": "application/vnd.ms-powerpoint",
	"pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
	"xls": "application/vnd.ms-excel",
	"xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


class PokController(http.Controller):

	@staticmethod
	def _validate_header():
		""" Header Validation """

		parameter = request.env["ir.config_parameter"].sudo()
		auth = (
			request.httprequest.headers.environ.get('HTTP_AUTHORIZATION')
		)
		cp_user = parameter.get_param("auth")
		assert auth == "{}".format(cp_user), "Authentication Error"

	@http.route("/formulario", type='http', auth="public", website=True)
	def form_ficha(self):
		data = {}
		# sectors = request.env['buen.gobierno.sector'].sudo().search([])
		#provinces = request.env['res.country.state'].sudo().search([])
		#partners = request.env['res.partner'].sudo().search([])
		# canton = request.env['l10n_ec_ote.canton'].sudo().search([])
		# parish = request.env['l10n_ec_ote.parish'].sudo().search([])
		# data.update({
		# 	#'sectors': sectors,
		# 	'provinces': provinces,
		# 	'partners': partners,
		# 	#'cantons': canton,
		# 	#'parishs': parish,
		# })
		return request.render("mold_control.form_template", data)

	@http.route(
		"/ficha-action", type='http',
		auth="public", method='POST',
		website=True
	)
	def ficha_action(self, **kw):
		#customer_id = request.env['res.partner'].search([('email', '=', 'elymar.alfaro@gmail.com')]
		customer_id = request.env['res.partner'].sudo().search(
			[('email', '=', kw.get('partner_email'))])
		if not customer_id:
			customer_id = request.env['res.partner'].sudo().create({
				'name': kw.get('partner_name'),
				'email': kw.get('partner_email'),
				'phone': kw.get('partner_phone'),
				'comment': kw.get('asunto'),
			})
		request_id = request.env['mold.request'].sudo().create({
			'name': kw.get('asunto'),
			'priority': kw.get('prioridad'),
			'partner_id': customer_id.id,
		})
		return request.render("mold_control.ficha_thank_you", {})

	@http.route(
		'/api/orders', auth='public',
		methods=['POST'], csrf=False, type='http'
	)
	def waybill_set(self):
		""" Waybill Set Cyberpuerta """
		try:
			self._validate_header()
			mold_id = request.env['mold.control'].sudo().create(
				json.loads(request.httprequest.data))
			return Response(mold_id, status=200, mimetype='application/json')
		except Exception as e:
			return Response(response=str(e), status=400)

	@http.route("/files", auth="public")
	def download(self, **kw):
		dir = '/home/ealfaro/' #Directorio de descarga
		complete_path = dir + kw.get("name")  #Ruta completa con archivo
		data = open(complete_path, "rb").read()
		return http.request.make_response(data, [
			("Content-Type", CONTENT_TYPE[kw.get("name").split('.')[1]]),
			("Content-Disposition", content_disposition(kw.get("name")))
		]
		                                  )
