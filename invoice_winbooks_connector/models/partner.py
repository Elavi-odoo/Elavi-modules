from odoo import fields, models,api,_

from odoo18.odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_sending_method = fields.Selection(
        selection_add=[('winbooks', 'WinBooks')],
    )


