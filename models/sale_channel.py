from odoo import models, fields

class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Sales Channel'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, unique=True)
    location_id = fields.Many2one('stock.location', string='Delivery Warehouse')
    journal_id = fields.Many2one('account.journal', string='Invoice Journal')
