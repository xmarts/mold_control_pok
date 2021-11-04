# -*- coding: utf-8 -*-
# from odoo import http


# class MoldControl(http.Controller):
#     @http.route('/mold_control/mold_control/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mold_control/mold_control/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mold_control.listing', {
#             'root': '/mold_control/mold_control',
#             'objects': http.request.env['mold_control.mold_control'].search([]),
#         })

#     @http.route('/mold_control/mold_control/objects/<model("mold_control.mold_control"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mold_control.object', {
#             'object': obj
#         })
