# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import requests
import urllib.parse
import logging

_logger = logging.getLogger(__name__)


class LineNotify(http.Controller):
    @http.route('/line/notify/callback', type='http', auth='none')
    def index(self, **kw):
        if not ('state' in kw and 'code' in kw):
            _logger.error(f'LINE Notify: Callback invalid parameter kw: {kw}')

            return request.redirect('/', 303)

        state = int(kw['state'])
        code = kw['code']

        line_notify_user = request.env['line.notify.user'].sudo().browse(state)

        if not line_notify_user.exists():
            _logger.error(f'LINE Notify: Callback user not found state: {state}')

            return request.redirect('/', 303)

        config_parameter = request.env['ir.config_parameter'].sudo()
        base_url = config_parameter.get_param('web.base.url')
        client_id = config_parameter.get_param('line_notify.client_id')
        client_secret = config_parameter.get_param('line_notify.client_secret')

        data = dict(
            grant_type='authorization_code',
            code=code,
            redirect_uri=f'{base_url}/line/notify/callback',
            client_id=client_id,
            client_secret=client_secret,
        )

        response = requests.post('https://notify-bot.line.me/oauth/token', data=data)

        if response.status_code != 200:
            _logger.error(f'LINE Notify: Callback cannot request token from LINE Notify server response: {response.text}')

            return request.redirect('/', 303)
        elif response.headers['Content-Type'] != 'application/json':
            _logger.error(f'LINE Notify: Callback request token response from LINE Notify server is not JSON response: {response.text}')

            return request.redirect('/', 303)

        body = response.json()

        if 'access_token' not in body:
            _logger.error(
                f'LINE Notify: Callback request token from LINE Notify server not sent the access token response: {response.text}')

            return request.redirect('/', 303)

        access_token = body['access_token']

        line_notify_user.write({
            'access_token': access_token,
            'state': 'connected'
        })

        action = request.env.ref('line_notify.line_notify_user_action')

        redirect_query_string = urllib.parse.urlencode({
            'menu_id': 4,
            'action': action.id,
            'model': 'line.notify.user',
            'id': line_notify_user.id,
            'view_type': 'form',
        })
        redirect_url = f'{base_url}/web#{redirect_query_string}'

        return request.redirect(redirect_url, 303)
