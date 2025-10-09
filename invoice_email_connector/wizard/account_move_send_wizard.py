
import base64
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    send_to_winbooks = fields.Boolean(string="Send to Email", default=False)


    def send_and_print_action(self):
        self.ensure_one()

        if self.send_to_winbooks:
            journal = self.invoice_ids[0].journal_id
            winbooks_email = getattr(journal, 'WinBooks_email', False)

            if not winbooks_email:
                raise UserError(_("No WinBooks email configured on the journal."))

            pdf_content = self.env['ir.actions.report']._render_qweb_pdf(
                'account.account_invoices', self.invoice_ids.ids
            )[0]
            attachment = self.env['ir.attachment'].create({
                'name': '%s.pdf' % self.invoice_ids[0].name,
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'account.move',
                'res_id': self.invoice_ids[0].id,
            })

            mail_values = {
                'subject': _('Invoice %s') % self.invoice_ids[0].name,
                'body_html': _('Please find attached the invoice %s.') % self.invoice_ids[0].name,
                'email_to': winbooks_email,
                'attachment_ids': [(4, attachment.id)],
            }
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

        return super(AccountInvoiceSend, self).send_and_print_action()

