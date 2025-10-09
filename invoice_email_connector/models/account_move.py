from odoo import models, _,fields
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    has_invoice_attachments = fields.Boolean(
        string='Has Invoice Attachments',
        compute='_compute_has_invoice_attachments'
    )

    def _compute_has_invoice_attachments(self):
        for move in self:
            attachments = self.env['ir.attachment'].search_count([
                ('res_model', '=', 'account.move'),
                ('res_id', '=', move.id),
            ])
            move.has_invoice_attachments = attachments > 0

    def action_send_winbooks_email(self):
        global winbooks_email
        integration_enabled = self.env['ir.config_parameter'].sudo().get_param(
            'invoice_winbooks_connector.enable_winbooks_integration',
            default=False
        )
        if not integration_enabled:
            raise UserError(_("Email Integration is disabled in settings."))

        for move in self:
            journal = move.journal_id
            winbooks_email = journal.WinBooks_email
            if not winbooks_email:
                raise UserError(_("No email configured on the journal %s.") % journal.display_name)

        all_attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'account.move'),
            ('res_id', 'in', self.ids),
        ])
        if not all_attachments:
            raise UserError(_("No attachments."))
        mail = self.env['mail.mail'].create({
            'subject': 'All Vendor Bills',
            'body_html': 'Please check your attachments.',
            'email_to': winbooks_email,
            'attachment_ids': [(4, att.id) for att in all_attachments],
        })
        mail.send()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Email sent successfully!',
                'type': 'success',
            }
        }
