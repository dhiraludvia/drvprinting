# -*- coding: utf-8 -*-
# from odoo import http
# from odoo.http import request

# class Drvprinting(http.Controller):
#     @http.route('/', type='http', auth='public', website=True)
#     def index(self, **kw):
#         return request.render('drvprinting.homepage_view')


# class Drvprinting(http.Controller):
#     @http.route('/drvprinting/drvprinting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/drvprinting/drvprinting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('drvprinting.listing', {
#             'root': '/drvprinting/drvprinting',
#             'objects': http.request.env['drvprinting.drvprinting'].search([]),
#         })

#     @http.route('/drvprinting/drvprinting/objects/<model("drvprinting.drvprinting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('drvprinting.object', {
#             'object': obj
#         })
