# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    line_notify_client_id = fields.Char(string='Client ID', config_parameter='line_notify.client_id')
    line_notify_client_secret = fields.Char(string='Client Secret', config_parameter='line_notify.client_secret')
