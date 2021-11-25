# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MoldRequestStage(models.Model):
	_name = 'mold.control'
	_description = 'Control de moldes para fabricacion'
	_inherit = ['company.mixin', 'mail.thread']
	#_rec_name = 'partner_id'