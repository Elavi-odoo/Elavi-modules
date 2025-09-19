import base64

from odoo import _, fields, models,api

from odoo18.odoo.exceptions import UserError


class AccountMoveSendWizard(models.TransientModel):
    _inherit = 'account.move.send.wizard'



    @api.depends('move_id')
    def _compute_sending_method_checkboxes(self):
        super()._compute_sending_method_checkboxes()

        for wizard in self:
            if wizard.sending_method_checkboxes:
                wizard.sending_method_checkboxes['winbooks'] = {
                    'checked': False,
                    'label': 'WinBooks',
                }


    def action_send_and_print(self, allow_fallback_pdf=False):
        if self.sending_methods and 'winbooks' in self.sending_methods:
            winbooks_email = self.env['ir.config_parameter'].sudo().get_param(
                'invoice_winbooks_connector.winbooks_email'
            )

            if not winbooks_email:
                raise UserError(_("No WinBooks email configured. Please set it in Settings."))

            pdf_content = self.env['ir.actions.report']._render_qweb_pdf(
                'account.account_invoices', self.move_id.ids
            )[0]

            attachment = self.env['ir.attachment'].create({
                'name': f'{self.move_id.name}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'account.move',
                'res_id': self.move_id.id,
            })

            mail = self.env['mail.mail'].create({
                'subject': self.mail_subject or f'Invoice {self.move_id.name}',
                'body_html': self.mail_body or f'Please find attached invoice {self.move_id.name}',
                'email_to': winbooks_email,
                'attachment_ids': [(4, attachment.id)],
            })
            mail.send()

            original_methods = list(self.sending_methods)
            original_methods.remove('winbooks')
            self.sending_methods = original_methods

        if self.sending_methods:
            return super().action_send_and_print(allow_fallback_pdf=allow_fallback_pdf)
        else:
            return {'type': 'ir.actions.act_window_close'}








