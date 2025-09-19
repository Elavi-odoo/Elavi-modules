from odoo import fields, models,api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    WinBooks_email = fields.Char(string="WinBooks Email")

    winbooks_integration_enabled = fields.Boolean(
        string="WinBooks Integration Enabled",
        compute="_compute_winbooks_integration_enabled"
    )

    @api.depends()
    def _compute_winbooks_integration_enabled(self):
        winbooks_valid = self.env['ir.config_parameter'].sudo().get_param(
            'invoice_winbooks_connector.enable_winbooks_integration'
        )
        for record in self:
            record.winbooks_integration_enabled = bool(winbooks_valid)