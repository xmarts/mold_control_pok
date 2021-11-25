# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MoldRevision(models.Model):
	_name = 'mold.revision'
	_description = 'Revisión para moldes'

	user_id = fields.Many2one(
		'res.users',
		string='Usuario',
		default=lambda self: self.env.user
	)
	name = fields.Char(
		string='Observación',
		required=True
	)
	state = fields.Selection([
		('optimo', 'Optimo'),
		('aceptable', 'Aceptable'),
		('deteriorado','Deteriorado')],
		string="Estado",
		required=True,
		tracking=True
	)
	mold_id = fields.Many2one(
		'mold.control',
		string='Molde',
	)

