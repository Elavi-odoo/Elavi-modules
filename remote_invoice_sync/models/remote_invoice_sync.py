import requests
import base64
from odoo import models, fields, api, _

class RemoteInvoiceSync(models.Model):
    _name = "remote.invoice.sync"
    _description = "Remote Odoo Invoice Sync"
    _order = "name"

    name = fields.Char("Name", required=True)
    active = fields.Boolean("Active", default=True)
    company_id = fields.Many2one("res.company", string="Company", required=True)
    url = fields.Char("Remote Odoo URL", required=True)
    db_name = fields.Char("Remote DB Name", required=True)
    api_key = fields.Char("API Key", required=True)
    last_sync = fields.Datetime("Last Sync")
    status = fields.Selection(
        [("success","Success"),("error","Error"),("pending","Pending")],
        string="Status", default="pending"
    )
    last_error = fields.Text("Last Error")
    retry_count = fields.Integer("Retry Count", default=0)
    max_retry = fields.Integer("Max Retry", default=5, help="Maximum retry attempts for failed syncs")

    def sync_all(self):
        """Cron job: sync all active remote databases with retry support"""
        for remote in self.search([("active", "=", True)]):
            # Skip if exceeded max retry
            if remote.status == "error" and remote.retry_count >= (remote.max_retry or 5):
                continue
            remote.sync_single()

    def sync_single(self):
        """Sync a single remote database"""
        headers = {
            "Authorization": f"bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Odoo-Database": self.db_name,
        }

        domain = [
            ["move_type", "=", "out_invoice"],
            ["state", "=", "posted"]
        ]
        if self.last_sync:
            domain.append(["write_date", ">", self.last_sync])

        payload = {
            "domain": domain,
            "fields": ["id","name","invoice_date","partner_id","invoice_line_ids"],
            "limit": 50,
        }

        try:
            res = requests.post(
                f"{self.url}/account.move/search_read",
                json=payload,
                headers=headers,
                timeout=60
            )
            res.raise_for_status()
            invoices = res.json()
        except Exception as e:
            self.status = "error"
            self.last_error = str(e)
            self.retry_count += 1

            # if retry count exceeds max, mark as final error
            if self.retry_count >= (self.max_retry or 5):
                self.status = "error"
                self.last_error += "\nMax retries reached."
            return

        for inv in invoices:
            try:
                local = self.env["account.move"].search([
                    ("x_remote_id","=",inv["id"]),
                    ("company_id","=",self.company_id.id)
                ], limit=1)

                # Partner
                partner = self.env["res.partner"].search([
                    ("x_remote_id","=",inv["partner_id"][0])
                ], limit=1)
                if not partner:
                    partner = self.env["res.partner"].create({
                        "name": inv["partner_id"][1],
                        "x_remote_id": inv["partner_id"][0],
                    })

                vals = {
                    "move_type": "out_invoice",
                    "partner_id": partner.id,
                    "invoice_date": inv.get("invoice_date"),
                    "company_id": self.company_id.id,
                    "x_remote_id": inv["id"]
                }

                if local:
                    local.write(vals)
                    local.invoice_line_ids.unlink()
                else:
                    local = self.env["account.move"].create(vals)

                # Invoice lines (labels only)
                line_ids = []
                if inv.get("invoice_line_ids"):
                    line_payload = {
                        "domain":[["id","in",inv["invoice_line_ids"]]],
                        "fields":["name","quantity","price_unit"]
                    }
                    line_res = requests.post(
                        f"{self.url}/account.move.line/search_read",
                        json=line_payload,
                        headers=headers,
                        timeout=60
                    )
                    lines = line_res.json()
                    for l in lines:
                        line_ids.append((0,0,{
                            "name": l["name"],
                            "quantity": l["quantity"],
                            "price_unit": l["price_unit"],
                        }))
                if line_ids:
                    local.write({"invoice_line_ids": line_ids})

                # PDF
                pdf_res = requests.post(
                    f"{self.url}/account.move/get_invoice_pdf",
                    json={"ids":[inv["id"]]},
                    headers=headers,
                    timeout=60
                )
                pdf_data = pdf_res.json()
                if pdf_data:
                    self.env["ir.attachment"].create({
                        "name": f"{inv['name']}.pdf",
                        "type": "binary",
                        "datas": pdf_data["data"],
                        "res_model": "account.move",
                        "res_id": local.id,
                        "mimetype": "application/pdf"
                    })

                local.write({"x_sync_error": False, "x_sync_retry": 0})

            except Exception as e:
                if local:
                    local.write({
                        "x_sync_error": str(e),
                        "x_sync_retry": (local.x_sync_retry or 0) + 1
                    })

        self.last_sync = fields.Datetime.now()
        self.status = "success"
        self.last_error = False
        self.retry_count = 0
