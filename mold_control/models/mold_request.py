# -*- coding: utf-8 -*-
from random import randint

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MoldRequest(models.Model):
	_name = 'mold.request'
	_description = 'Solicitud para creación de moldes'
	_inherit = ['company.mixin', 'mail.thread', 'mail.activity.mixin']

	code = fields.Char(string='Código')
	name = fields.Char(string='Descripción')
	partner_id = fields.Many2one(
		'res.partner',
		string='Solicitante',
		default=lambda self: self.env.user.partner_id.id
	)
	state = fields.Selection([
		('draft', 'Borrador'),
		('approved', 'Aprobada'),
		('cancel', 'Cancelada')],
		string="Estado",
		default='draft',
		tracking=True
	)
	priority = fields.Selection([
		('0', 'Low'),
		('1', 'Medium'),
		('2', 'High'),
		('3', 'Very High')]
	)
	color = fields.Integer(
		string='Color',
		default=lambda self: self._get_default_color()
	)
	product_id = fields.Many2one(
		'product.product',
		string='Modelo'
	)
	image = fields.Image(
		string='Foto del Modelo',
		related='product_id.image_1920'
	)
	mold_ids = fields.One2many(
		'mold.control',
		'mold_request_id',
		string='Moldes'
	)

	def _get_default_color(self):
		return randint(1, 11)

	@api.model
	def create(self, vals):
		request = super().create(vals)
		template = self.env.ref('mold_control.mold_request_template')
		users = self.env.ref('mold_control.mold_control_manager').users
		emails = users.mapped('email')
		template.email_to = ",".join(emails)
		#template.attachment_ids = [(6, 0, mold.attachment_ids.ids)]
		template.send_mail(request.id, force_send=True)
		return request

	def button_approved(self):
		for request in self:
			request.state = 'approved'
			request.code = self.env['ir.sequence'].next_by_code(
				'mold.request.sequence') or 'Nuevo'

	def button_create_mold(self):
		self.env['mold.control'].create({
			'name': '{} / {}'.format(self.product_id.name, self.partner_id.name),
			'mold_request_id': self.id,
			'partner_id': self.partner_id.id,
			'product_id': self.product_id.id,
		})

	def button_cancel(self):
		for request in self:
			request.state = 'cancel'