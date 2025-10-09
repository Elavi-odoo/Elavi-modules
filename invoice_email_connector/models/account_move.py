from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_send_winbooks_email(self):
        global winbooks_email
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
