import re
from odoo import fields, models,api,_
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    WinBooks_email = fields.Char(string="Email")
    winbooks_integration_enabled = fields.Boolean(
        string="WinBooks Integration Enabled",
        compute="_compute_winbooks_integration_enabled"
    )

    @api.constrains('WinBooks_email')
    def _check_winbooks_email(self):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        for rec in self:
            if rec.WinBooks_email:
                emails = [e.strip() for e in rec.WinBooks_email.split(',') if e.strip()]
                for email in emails:
                    if not re.match(email_pattern, email):
                        raise ValidationError(_("Invalid email format: %s") % email)

    @api.depends()
    def _compute_winbooks_integration_enabled(self):
        winbooks_valid = self.env['ir.config_parameter'].sudo().get_param(
            'invoice_winbooks_connector.enable_winbooks_integration'
        )
        for record in self:
            record.winbooks_integration_enabled = bool(winbooks_valid)