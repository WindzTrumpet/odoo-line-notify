from odoo import fields, models
from odoo.exceptions import UserError
import urllib.parse
import requests
import logging

_logger = logging.getLogger(__name__)


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

    def action_revoke(self):
        self.ensure_one()
        self.revoke()

    def action_test_send(self):
        self.send('Test send message')

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Test Send Message',
                'message': 'Test message sent successfully.',
            },
        }

    def send(self, message, image_file=None):
        headers = dict(
            Authorization=f'Bearer {self.access_token}',
        )
        data = dict(
            message=message,
        )
        files = dict()

        if image_file:
            files['imageFile'] = image_file

        response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data, files=files)

        if response.status_code != 200:
            _logger.error(f'LINE Notify: cannot send notify response: {response.text}')

            self.env['line.notify.log'].sudo().create({
                'line_notify_user_id': self.id,
                'message': message,
                'state': 'fail',
                'error_message': response.text,
            })
            self._cr.commit()

            raise UserError('Cannot send notify.')

        self.env['line.notify.log'].sudo().create({
            'line_notify_user_id': self.id,
            'message': message,
            'state': 'success'
        })

    def revoke(self):
        self.ensure_one()

        headers = dict(
            Authorization=f'Bearer {self.access_token}',
        )
        response = requests.post('https://notify-api.line.me/api/revoke', headers=headers)

        if response.status_code != 200:
            _logger.error(f'LINE Notify: cannot revoke access token response: {response.text}')

            raise UserError('Cannot revoke at this time. Please try again later.')

        self.write({
            'access_token': None,
            'state': 'not_connected'
        })

