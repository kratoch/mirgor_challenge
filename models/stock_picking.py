from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_channel_id = fields.Many2one('sale.channel', string='Sales Channel')
