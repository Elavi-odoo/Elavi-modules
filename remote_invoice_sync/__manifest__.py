{
    "name": "Remote Invoice Sync",
    "version": "19.0",
    "summary": "Sync invoices from a remote Odoo via JSON-2 API",
    "category": "Accounting",
    "depends": ["account"],
    "data": [
        "data/cron.xml",
        "views/remote_invoice_sync_views.xml",
    ],
    "installable": True,
    "application": False,
}
