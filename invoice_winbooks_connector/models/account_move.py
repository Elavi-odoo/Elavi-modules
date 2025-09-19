from odoo import models, _
from odoo.exceptions import UserError
import base64

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_send_winbooks_email(self):
        for move in self:
            journal = move.journal_id
            winbooks_email = journal.WinBooks_email
            if not winbooks_email:
                raise UserError(_("No WinBooks email configured on the journal %s.") % journal.display_name)

            pdf_content = self.env['ir.actions.report']._render_qweb_pdf(
                'account.account_invoices', move.ids
            )[0]

            attachment = self.env['ir.attachment'].create({
                'name': f'{move.name}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'account.move',
                'res_id': move.id,
            })

            mail = self.env['mail.mail'].create({
                'subject': f'Invoice {move.name}',
                'body_html': f'Please find attached invoice {move.name}',
                'email_to': winbooks_email,
                'attachment_ids': [(4, attachment.id)],
            })
            mail.send()

        return {
            'type': 'ir.actions.act_window_close'
        }
