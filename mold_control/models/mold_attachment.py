# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MoldAttachment(models.Model):
	_name = 'mold.attachment'
	_description = 'Adjuntos'

	name = fields.Char(
		string='Descripción',
		size=64,
		required=False,
		readonly=False
	)
	attachment = fields.Binary(string='Archivo')
	attachment_filename = fields.Char(string='Nombre de Archivo')
	mold_control_id = fields.Many2one(
		'mold.control',
		string='Molde'
	)
