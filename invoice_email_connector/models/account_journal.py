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
        for record in self:
            if record.WinBooks_email:
                emails = [email.strip() for email in record.WinBooks_email.split(',')]

                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

                for email in emails:
                    if email and not re.match(email_pattern, email):
                        raise ValidationError(
                            _('Invalid email format: %s\nPlease use format: email1@domain.com, email2@domain.com') % email
                        )

    @api.depends()
    def _compute_winbooks_integration_enabled(self):
        winbooks_valid = self.env['ir.config_parameter'].sudo().get_param(
            'invoice_winbooks_connector.enable_winbooks_integration'
        )
        for record in self:
            record.winbooks_integration_enabled = bool(winbooks_valid)