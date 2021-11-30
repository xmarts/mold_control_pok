# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RepairOrder(models.Model):
	_inherit = ['repair.order']

	mold_control_id = fields.Many2one(
		'mold.control',
		string='Molde'
	)
