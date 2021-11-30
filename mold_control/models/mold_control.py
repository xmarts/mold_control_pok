# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.http import request


class MoldControl(models.Model):
    _name = 'mold.control'
    _description = 'Control de moldes para fabricacion'
    _inherit = ['company.mixin', 'mail.thread']
    #_rec_name = 'partner_id'

    name = fields.Char(
        string='Molde',
        size=64,
        default="Molde"
    )
    active = fields.Boolean(
        string='Activo',
        default=True
    )
    code = fields.Char(string='Código')
    description = fields.Text(
        string='Motivo para cambiar a aceptable',
        readonly=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Propietario",
        help="Propietario del molde",
        default=lambda self: self.env.user.partner_id.id
    )
    mold_request_id = fields.Many2one(
        'mold.request',
        string='Solicitud'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Modelo'
    )
    list_price = fields.Float(
        related='product_id.list_price',
        string='Precio de venta de producto'
    )
    base = fields.Float(
        string="Base",
        help="Colocar en base a cm",
    )
    height = fields.Float(
        string="Altura",
    )
    width = fields.Float(
        string="Anchura",
    )
    days = fields.Integer(
        string='Días para vencimiento',
        default=30
    )
    attachment_count = fields.Integer(
        string='Contador de adjuntos',
        compute='_compute_attachment_count'
    )
    register_date = fields.Date(string='Fecha de registro')
    expiration_date = fields.Date(
        string='Fecha de vencimiento',
        compute='_compute_expiration_date',
        store=True
    )
    area = fields.Float(
        string='Área',
    #	compute='_compute_area'
    )
    volumen = fields.Float(
        string='Volumen',
        compute='_compute_volumen'
    )
    wh_id = fields.Many2one(
        'stock.warehouse',
        string='Almacén'
    )
    image = fields.Binary(string='Imagen')
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Adjuntos'
    )
    #Generales
    maintenance = fields.Selection([
        ('interno', 'Interno'),
        ('externo', 'Externo'),
        ('terceros', 'Tercero')],
        string="Mantenimiento",
        help="Quien se encrga de darle mantenimiento al molde",
        readonly=False,
        default='interno'
    )
    origin = fields.Selection(
        [('interno', 'Interno'),
        ('externo', 'Externo')],
        string="Origen"
    )
    model = fields.Char(
        string="Modelo",
        help="Referencia del modelo a usar"
    )
    state = fields.Selection([
        ('optimo', 'Optimo'),
        ('aceptable', 'Aceptable'),
        ('deteriorado','Deteriorado')],
        string="Estado",
        default='optimo',
        tracking=True
    )
    tag_ids = fields.Many2many(
        'mold.tag',
        string='Etiquetas'
    )
    components = fields.Integer(string="Componentes")
    category_id = fields.Many2one(
        'model.category',
        string="Categoria-Material",
        help="Material del que esta armado el molde"
    )
    validity = fields.Date(string="Vigencia")
    revision_ids = fields.One2many(
        'mold.revision',
        'mold_id',
        string="Revisiones",
    )
    repair_order_ids = fields.One2many(
        'repair.order',
        'mold_control_id',
        string="Reparaciones",
    )

    def button_aceptable(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cambiar a Aceptable',
            'view_mode': 'form',
            'res_model': 'wizard.change.acceptable',
            'target': 'new',
            'context': {'default_mold_control_id': self.id},
        }

    def button_repair(self):
        self.env['repair.order'].create({
            'mold_control_id': self.id,
	        'location_id': self.env.ref('stock.location_order').id,
	        'partner_id': self.partner_id.id,
            'product_id': self.product_id.id,
	        'product_uom': self.product_id.uom_id.id,
        })


    def button_send_mail(self):
        for mold in self:
            menu = self.env.ref("mold_control.mold_control_optimo_menu")
            action = menu.action
            url = (
                "{}#id={}&action={}&model={}&view_type=form&menu_id={}".format(
                    request.httprequest.environ["HTTP_REFERER"],
                    str(mold.id),
                    str(action.id),
                    mold._name,
                    str(menu.id)
                )
            )

            template = self.env.ref('mold_control.mold_control_state_template')
            template.email_to = mold.partner_id.email
          #  template.attachment_ids = [(6, 0, mold.attachment_ids.ids)]
            template.with_context(url=url).send_mail(mold.id, force_send=True)

        # else:
        # 	raise ValidationError(
        # 		'El estado no es deteriorado, por lo que no se puede cambiar'
        # 	)

    def _compute_attachment_count(self):
        for mold in self:
            mold.attachment_count = self.env['mold.attachment'].search_count(
                [('mold_control_id', '=', mold.id)])

    def button_add_attachment(self):
        form_view_ref = self.env.ref('mold_control.mold_attachment_form', False)
        tree_view_ref = self.env.ref('mold_control.mold_attachment_list', False)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Añadir Adjunto',
            'view_mode': 'tree,form',
            'res_model': 'mold.attachment',
            'context': {'default_mold_control_id': self.id},
            'domain': [('mold_control_id', '=', self.id)],
            'views': [(tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
        }

    def button_optimo(self):
        for mold in self:
            mold.state = 'optimo'

    def button_deteriorado(self):
        for mold in self:
            mold.state = 'deteriorado'

    @api.depends('register_date', 'days')
    def _compute_expiration_date(self):
        #self.expiration_date = False
        #self.expiration_date = self.register_date + timedelta(days=self.days)
        for mold in self:
            mold.expiration_date = False
            if mold.register_date and mold.days:
                mold.expiration_date = mold.register_date + timedelta(days=mold.days)

    @api.depends('height', 'width', 'base')
    def _compute_volumen(self):
        self.volumen = 0
        for mold in self:
            mold.volumen = mold.height * mold.base * mold.width

    @api.onchange('maintenance')
    def _onchange_maintenance(self):
        for mold in self:
            mold.model = mold.maintenance

    @api.constrains('product_id')
    def _constrains_name(self):
        for mold in self:
            if not mold.product_id:
                raise ValidationError('Usted no ha seleccionado un producto')

    def _send_notification(self, body, subject, mold_id):
        msg_id = self.env["mail.message"].create({
            "message_type": "notification",
            "subtype_id": self.env.ref("mail.mt_comment").id,
            "body": body,
            "subject": subject,
            "partner_ids": [
                (4, self.env.user.partner_id.id)
            ],
            "model": self._name,
            "res_id": mold_id.id
            })
        notification = self.env['mail.notification'].create({
            "res_partner_id": self.env.user.partner_id.id,
            "mail_message_id": msg_id.id,
            "notification_type": "inbox",
        })

    @api.model
    def create(self, vals):
        if  self.env.context.get('peid_id'):
            vals['pei_id'] = self.env.context.get('peid_id')
        mold = super().create(vals)
        mold.code = self.env['ir.sequence'].next_by_code(
            'mold.control.sequence') or 'Nuevo'
        template = self.env.ref('mold_control.notificacion_creacion_molde')
        template.email_to = self.env.user.login
        template.attachment_ids = [(6, 0, mold.attachment_ids.ids)]
        template.send_mail(mold.id, force_send=True)
        self._send_notification(
            "Se ha creado un registro nuevo {}".format(mold.code),
            "Registro nuevo",
            mold
        )
        #mold.code = self.env.ref('mold_control.sequence_mold_control').next_by_id()
        return mold

    def write(self, vals):
        #for mold in self:
        # if vals['name'] == 'Molde1':
        #     raise ValidationError(' No puede editar el registro porque el nombre es igual a Molde1')
        mold = super().write(vals)
        template = self.env.ref('mold_control.notificacion_modificacion_molde')
        template.email_to = self.env.user.login
        template.send_mail(self.id, force_send=True)
        return mold

    def unlink(self):
        for mold in self:
            if mold.state == 'optimo':
                raise ValidationError('No se puede eliminar un registro en estado optimo')
        return super().unlink()

    @api.model
    def _cron_mold_creation(self):
        l = (1,2,3)
        for v in l:
            self.env['mold.control'].create({
                'name': 'Molde creado por el cron {}'.format(v)
            })

    @api.model
    def _cron_mold_state_validation(self):
        mold_ids = self.search([])
        for mold in mold_ids:
            if mold.revision_ids:
                mold.state = mold.revision_ids[-1].state
                if mold.revision_ids[-1].state == 'deteriorado':
                    mold.active = False






