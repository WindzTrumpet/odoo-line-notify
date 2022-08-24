from odoo import fields, models
import urllib.parse


class LINENotifyUser(models.Model):
    _name = 'line.notify.user'
    _description = 'LINE Notify User'

    name = fields.Char(required=True)
    access_token = fields.Char(string='Access Token', readonly=True)
    state = fields.Selection([
        ('not_connected', 'Not Connected'),
        ('connected', 'Connected'),
    ], required=True, default='not_connected')

    def action_connect(self):
        self.ensure_one()

        url = 'https://notify-bot.line.me/oauth/authorize?'
        query_string = urllib.parse.urlencode({
            'response_type': 'code',
            'client_id': 'iOcRVUFUpOVjQMH1ba18iI',
            'redirect_uri': 'http://localhost:8069/line/notify/callback',
            'scope': 'notify',
            'state': self.id,
        })
        url += query_string

        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': url,
        }
