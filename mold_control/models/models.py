# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MoldControl(models.Model):
    _name = 'mold.control'
    _description = 'Control de moldes para fabricacion'

    #referencia secuencial
    name = fields.Char(
    	string='Molde',
    	size=64,
    	required=False,
    	readonly=False
    )

    #campo cliente
    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
    )

    #campos de medida
    base = fields.Float(string="Base", 
    		help="Colocar en base a cm")
    height = fields.Float(string="Altura")
    width = fields.Float(string="Anchura")

    #Generales
    maintenance = fields.Selection([('interno','Interno'),
    		('externo','Externo'),
    		('terceros','Tercero')],
    		string="Mantenimiento", 
    		help="Quien se encrga de darle mantenimiento al molde")
    origin = fields.Selection([('interno','Interno'),
    		('externo','Externo')], 
    		string="Origen")
    model = fields.Char(string="Modelo",
    					help="Referencia del modelo a usar")
    state = fields.Selection([('optimo','Optimo'),
    		('aceptable','Aceptable'),
    		('deteriorado','Deteriorado')],
			string="Estado", default='optimo')
    components = fields.Integer(string="Componentes")
    category = fields.Many2one('model.category', 
    		string="Categoria-Material", 
    		help="Material del que esta armado el molde")
    validity = fields.Date(string="Vigencia")




class ModelCategory(models.Model):
    _name = 'model.category'
    _description = 'Categoria-Materiales'

    name = fields.Char(
    	string='Nombre',
    	size=64,
    	required=False,
    	readonly=False
    )

# class mold_control(models.Model):
#     _name = 'mold_control.mold_control'
#     _description = 'mold_control.mold_control'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
