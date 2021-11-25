# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ModelCategory(models.Model):
	_name = 'model.category'
	_description = 'Categoria-Materiales'

	name = fields.Char(
		string='Nombre',
		size=64,
		required=False,
		readonly=False
	)
	mold_control_ids = fields.One2many(
		'mold.control',
		'category_id',
		string='Moldes'
	)
