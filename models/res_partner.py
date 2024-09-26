from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_control = fields.Boolean(string='Credit Control')
    credit_group_ids = fields.Many2many('credit.group', string='Credit Groups')

    @api.constrains('credit_group_ids')
    def _check_credit_group(self):
        for partner in self:
            if partner.credit_control and not partner.credit_group_ids:
                raise ValidationError(_('You must select at least one credit group if credit control is enabled.'))
