# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MoldRequestStage(models.Model):
	_name = 'mold.request.stage'
	_description = 'Control de etapas para solicitud de moldes'
	_inherit = ['company.mixin']

	name = fields.Char(
		string='Nombre de la etapa',
		required=True
	)
	active = fields.Boolean(
		string='Activo',
		default=True
	)
	sequence = fields.Integer(string='Secuencia')
	# auto_validation_kanban_state = fields.Boolean(
	# 	string='Estado kanban automático',
	# )
	description = fields.Text(string='Descripción')
	# disabled_rating_warning = fields.Text(
	# 	string='Advertencia de clasificación deshabilitada',
	# )
	fold = fields.Boolean(string='Doblado en Kanban')