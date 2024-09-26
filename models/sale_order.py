from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_channel_id = fields.Many2one('sale.channel', string='Sales Channel', required=True)
    credit_status = fields.Selection(
        [('no_limit', 'No Credit Limit'), ('available', 'Credit Available'), ('blocked', 'Credit Blocked')],
        string='Credit Status', readonly=True, default='no_limit', compute='_compute_credit_status', store=True
    )

    @api.depends('partner_id', 'sale_channel_id', 'amount_total')
    def _compute_credit_status(self):
        for order in self:
            if order.partner_id and order.sale_channel_id:
                credit_groups = order.partner_id.credit_group_ids.filtered(
                    lambda g: g.sale_channel_ids.ids == order.sale_channel_id.ids)
                if credit_groups:
                    credit_group = credit_groups[0]
                    credit_available = credit_group.credit_available
                    if order.amount_total > credit_available:
                        order.credit_status = 'blocked'
                    else:
                        order.credit_status = 'available'
                else:
                    order.credit_status = 'no_limit'
            else:
                order.credit_status = 'no_limit'

    def action_confirm(self):
        if self.credit_status == 'blocked':
            raise UserError(_('Cannot confirm sale order because the credit status is "Credit Blocked".'))
        res = super(SaleOrder, self).action_confirm()
        for picking in self.picking_ids:
            if self.sale_channel_id:
                picking.location_id = self.sale_channel_id.location_id
        return res

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super(SaleOrder, self)._create_invoices(grouped, final, date)
        for invoice in invoices:
            if self.sale_channel_id:
                invoice.journal_id = self.sale_channel_id.journal_id
        return invoices
