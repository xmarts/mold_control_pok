# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MoldTag(models.Model):
	_name = 'mold.tag'
	_description = 'Etiquetas para moldes'
	_sql_constraints = [
		('name_unique', 'UNIQUE(name)', "Ya existe esta etiqueta!")
	]

	name = fields.Char(
		string='Etiqueta',
		size=64,
		required=True
	)
	color = fields.Integer(string='Color')
