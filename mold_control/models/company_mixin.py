# -*- coding: utf-8 -*-

from odoo import models, fields


class CompanyMixin(models.AbstractModel):
	_name = 'company.mixin'
	_description = 'Modelo abstracto para agregar campo de compañía'

	company_id = fields.Many2one(
		'res.company',
		string='Compañía',
		default=lambda self: self.env.user.company_id
	)
	state_2 = fields.Selection([
		('draft', 'Borrador'),
		('done', 'Hecho')],
		string='Estado 2',
		tracking=True
	)

	def button_draft(self):
		self.state_2 = 'draft'

	def button_done(self):
		self.state_2 = 'done'
