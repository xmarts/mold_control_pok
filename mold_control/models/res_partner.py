# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
	_inherit = ['res.partner']

	mold_control_ids = fields.One2many(
		'mold.control',
		'partner_id',
		string='Moldes'
	)
