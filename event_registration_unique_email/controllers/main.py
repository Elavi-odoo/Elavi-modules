from odoo import http
from odoo.http import request, route, url_encode
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.utils import redirect


class WebsiteSaleInherit(WebsiteSale):

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        if request.httprequest.method == "POST" and 'submitted' in kw:
            email = kw.get('email')
            if email:
                existing_user = request.env['res.users'].sudo().search([
                    ('partner_id.email', '=', email),
                    ('share', '=', True)
                ], limit=1)

                if existing_user:
                    message = "The email you entered is already associated with an account. Please log in."
                    params = url_encode({
                        'message': message,
                        'redirect': '/event'
                    })
                    return redirect(f"/web/login?{params}")

        return super().address(**kw)
