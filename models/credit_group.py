from email.policy import default

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreditGroup(models.Model):
    _name = 'credit.group'
    _description = 'Credit Group'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, unique=True)
    sale_channel_ids = fields.Many2many('sale.channel', string='Sales Channels')
    global_credit = fields.Monetary(string='Global Credit', required=True, currency_field='currency_id')
    credit_used = fields.Monetary(string='Credit Used', compute='_compute_credit_used', currency_field='currency_id',
                                  store=True)
    credit_available = fields.Monetary(string='Credit Available', compute='_compute_credit_available',
                                       currency_field='currency_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env['res.currency'])

    @api.depends('sale_channel_ids', 'global_credit')
    def _compute_credit_used(self):
        for group in self:
            credit_used = 0
            company_currency = self.currency_id
            sale_orders = self.env['sale.order'].search([
                ('sale_channel_id', 'in', group.sale_channel_ids.ids),
                ('state', 'in', ['sale'])
            ])
            invoices = self.env['account.move'].search([
                ('sale_channel_id', 'in', group.sale_channel_ids.ids),
                ('state', 'not in', ['draft'])
            ])

            for order in sale_orders:
                if order.invoice_status == 'not_invoiced':
                    amount_total = order.amount_total
                    if order.currency_id != company_currency:
                        amount_total = order.currency_id._convert(amount_total, company_currency, self.env.company,
                                                                  fields.Date.today())
                    credit_used += amount_total

            for invoice in invoices:
                amount_residual = invoice.amount_residual
                if invoice.currency_id != company_currency:
                    amount_residual = invoice.currency_id._convert(amount_residual, company_currency, self.env.company,
                                                                   fields.Date.today())
                credit_used += amount_residual

            group.credit_used = credit_used


    @api.depends('global_credit', 'credit_used')
    def _compute_credit_available(self):
        for group in self:
            group.credit_available = group.global_credit - group.credit_used

    @api.constrains('global_credit')
    def _check_global_credit(self):
        for group in self:
            if group.global_credit < 0:
                raise ValidationError(_('Global credit cannot be negative.'))
