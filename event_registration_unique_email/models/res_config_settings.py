from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    event_registration_unique_email = fields.Boolean(
        related='company_id.event_registration_unique_email',
        string="Print Date Label",
        readonly=False,
        help="This option allows you to print the date label on the check as per CPA.\n"
             "Disable this if your pre-printed check includes the date label."
    )
    event_checkout_unique_email = fields.Boolean(
        related='company_id.event_checkout_unique_email',
        string="Print Date Label",
        readonly=False,
        help="This option allows you to print the date label on the check as per CPA.\n"
             "Disable this if your pre-printed check includes the date label."
    )
