# -*- coding: utf-8 -*-
# from odoo import http


# class LineNotify(http.Controller):
#     @http.route('/line_notify/line_notify', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/line_notify/line_notify/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('line_notify.listing', {
#             'root': '/line_notify/line_notify',
#             'objects': http.request.env['line_notify.line_notify'].search([]),
#         })

#     @http.route('/line_notify/line_notify/objects/<model("line_notify.line_notify"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('line_notify.object', {
#             'object': obj
#         })
