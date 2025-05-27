from odoo import models, fields


class res_company(models.Model):
    _inherit = "res.company"

    event_registration_unique_email = fields.Boolean(
        string='event registration',
        default=False,
        help="This option allows you to print the date label on the check as per CPA.\n"
             "Disable this if your pre-printed check includes the date label.",
    )
    event_checkout_unique_email = fields.Boolean(
        string='event checkout',
        default=False,
        help="This option allows you to print the date label on the check as per CPA.\n"
             "Disable this if your pre-printed check includes the date label.",
    )
