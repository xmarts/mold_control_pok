# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WizardChangeAcceptable(models.TransientModel):
	_name = 'wizard.change.acceptable'
	_description = 'Wizard para cambiar el molde a aceptable'

	mold_control_id = fields.Many2one(
		'mold.control',
		string='Molde'
	)
	description = fields.Text(string='Motivo')

	def button_add_description(self):
		self.mold_control_id.description = self.description
		self.mold_control_id.state = 'aceptable'
