from odoo import fields, models, api


class LINENotifyLog(models.Model):
    _name = 'line.notify.log'
    _description = 'LINE Notify Log'

    line_notify_user_id = fields.Many2one('line.notify.user', string='LINE Notify User', required=True, ondelete='cascade')
    message = fields.Text(required=True)
    state = fields.Selection([
        ('fail', 'Fail'),
        ('success', 'Success'),
    ], required=True)
    error_message = fields.Char()
