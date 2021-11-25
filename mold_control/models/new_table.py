# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NewTable(models.Model):
	_name = 'new.table'
	_inherits = {'mold.control': 'new_table_id'}

	new_table_id = fields.Many2one(
		'mold.control',
		string='New Table',
	)
	name = fields.Char(
		string='Molde',
		size=64,
		required=True,
	)

	# @api.model
	# def create

