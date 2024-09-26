from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_channel_id = fields.Many2one('sale.channel', string='Sales Channel')