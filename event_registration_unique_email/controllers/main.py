import werkzeug

from odoo import http, _
from odoo.http import request, route, url_encode
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.utils import redirect
from odoo.addons.website_event.controllers.main import WebsiteEventController
import logging

from odoo.odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WebsiteSaleInherit(WebsiteSale):

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        print("address child")
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


class WebsiteEventController(WebsiteEventController):

    @http.route(['''/event/<model("event.event"):event>/registration/confirm'''],
                type='http', auth="public", methods=['POST'], website=True)
    def registration_confirm(self, event, **post):

        if not request.env['ir.http']._verify_request_recaptcha_token('website_event_registration'):
            raise UserError(_('Suspicious activity detected by Google reCaptcha.'))

        registrations_data = self._process_attendees_form(event, post)
        for registration in registrations_data:
            email = registration.get('email')
            if email:
                existing_partner = request.env['res.partner'].sudo().search([
                    ('email', '=', email),
                    ('user_ids', '!=', False),
                    ('user_ids.active', '=', True)
                ], limit=1)
                if existing_partner:
                    message = "The email you entered is already associated with an account. Please log in."
                    params = url_encode({
                        'message': message,
                        'redirect': '/event'
                    })
                    return redirect(f"/web/login?{params}")

        return super().registration_confirm(event, **post)
