import base64

from odoo import api, fields, models


class AccountMoveSend(models.AbstractModel):
    _inherit = 'account.move.send'

    def _generate_and_send_invoices(
            self, moves, from_cron=False, allow_raising=True, allow_fallback_pdf=False, **custom_settings
    ):

        custom_email = custom_settings.pop('custom_email', None)

        if custom_email:
            for move in moves:
                template = custom_settings.get('mail_template')
                if template:
                    subject = template._render_template(
                        template.subject, 'account.move', [move.id]
                    )[move.id]
                    body_html = template._render_template(
                        template.body_html, 'account.move', [move.id]
                    )[move.id]
                    email_from = template._render_template(
                        template.email_from, 'account.move', [move.id]
                    )[move.id] if template.email_from else self.env.user.email_formatted

                    pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
                        'account.account_invoices', [move.id]
                    )
                    attachment = self.env['ir.attachment'].create({
                        'name': f"{move.name or 'invoice'}.pdf",
                        'type': 'binary',
                        'datas': base64.b64encode(pdf_content),
                        'res_model': 'account.move',
                        'res_id': move.id,
                        'mimetype': 'application/pdf',
                    })

                    mail_values = {
                        'subject': subject,
                        'body_html': body_html,
                        'email_from': email_from,
                        'email_to': custom_email,
                        'recipient_ids': [(5, 0, 0)],
                        'res_id': move.id,
                        'model': 'account.move',
                        'attachment_ids': [(4, attachment.id)],
                    }

                    mail = self.env['mail.mail'].create(mail_values)
                    mail.send()


        return super()._generate_and_send_invoices(
            moves,
            from_cron=from_cron,
            allow_raising=allow_raising,
            allow_fallback_pdf=allow_fallback_pdf,
            **custom_settings
        )