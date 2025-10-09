from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_winbooks_integration = fields.Boolean(
        string="Enable Email Integration",
        config_parameter="invoice_winbooks_connector.enable_winbooks_integration",
    )

    