from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_winbooks_integration = fields.Boolean(
        string="Enable WinBooks Integration",
        config_parameter="invoice_winbooks_connector.enable_winbooks_integration",
    )
    winbooks_email = fields.Char(
        string="WinBooks Email",
        config_parameter="invoice_winbooks_connector.winbooks_email",
    )
    