import werkzeug

from odoo import http, _
from odoo.http import request, route, url_encode
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_event.controllers.main import WebsiteEventController
from werkzeug.utils import redirect
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class WebsiteSaleInherit(WebsiteSale):

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        # if request.httprequest.method == "POST" and 'submitted' in kw:
        #     email = kw.get('email')
        #     if email:
        #         existing_user = request.env['res.users'].sudo().search([
        #             ('partner_id.email', '=', email),
        #             ('share', '=', True)
        #         ], limit=1)
        #
        #         if existing_user:
        #             message = "The email you entered is already associated with an account. Please log in."
        #             params = url_encode({
        #                 'message': message,
        #                 'redirect': '/event'
        #             })
        #             return redirect(f"/web/login?{params}")
        #
        # return super().address(**kw)
        # Check if the unique email validation is enabled
        company = request.env.company
        if company.event_checkout_unique_email and request.env.user._is_public():
            if request.httprequest.method == "POST" and 'submitted' in kw:
                email = kw.get('email')

                if email:
                    existing_user = request.env['res.users'].sudo().search([
                        ('partner_id.email', '=', email),
                        ('share', '=', True)
                    ], limit=1)

                    if existing_user:
                        message = _("The email you entered is already associated with an account. Please log in.")
                        params = url_encode({
                            'message': message,
                            'redirect': '/event'

                        })
                        return redirect(f"/web/login?{params}")

        return super().address(**kw)


class WebsiteEventController(WebsiteEventController):

    @http.route('/event/check_email_portal', type='json', auth='public', methods=['POST'])
    def check_email_portal(self, email):

        # """Check if email has portal account"""
        # try:
        #     if not request.session.uid:
        #         return {
        #             'has_account': False,
        #             'email': email
        #         }
        #
        #     user_count = request.env['res.users'].sudo().search_count([
        #         ('email', '=', email),
        #         ('share', '=', True),
        #         ('active', '=', True)
        #     ])
        #
        #     return {
        #         'has_account': user_count > 0,
        #         'email': email
        #     }
        # except Exception as e:
        #     return {
        #         'error': str(e),
        #         'has_account': False
        #     }

        company = request.env.company
        print(company.event_registration_unique_email)
        if company.event_registration_unique_email == True:
            """Check if email has portal account"""
            try:
                if not request.session.uid:
                    return {
                        'has_account': False,
                        'email': email
                    }

                user_count = request.env['res.users'].sudo().search_count([
                    ('email', '=', email),
                    ('share', '=', True),
                    ('active', '=', True)
                ])

                return {
                    'has_account': user_count > 0,
                    'email': email
                }
            except Exception as e:
                return {
                    'error': str(e),
                    'has_account': False
                }

    @http.route(['''/event/<model("event.event"):event>/registration/confirm'''],
                type='http', auth="public", methods=['POST'], website=True)
    def registration_confirm(self, event, **post):

        # if not request.env['ir.http']._verify_request_recaptcha_token('website_event_registration'):
        #     raise UserError(_('Suspicious activity detected by Google reCaptcha.'))
        #
        # # Check if the user is logged in
        # if request.env.user._is_public():
        #     print("User is NOT logged in :")
        #     _logger.info("User is NOT logged in (public user).")
        #     registrations_data = self._process_attendees_form(event, post)
        #     for registration in registrations_data:
        #         email = registration.get('email')
        #         if email:
        #             existing_partner = request.env['res.partner'].sudo().search([
        #                 ('email', '=', email),
        #                 ('user_ids', '!=', False),
        #                 ('user_ids.active', '=', True)
        #             ], limit=1)
        #             if existing_partner:
        #                 message = "The email you entered is already associated with an account. Please log in."
        #                 params = url_encode({
        #                     'message': message,
        #                     'redirect': '/event'
        #                 })
        #                 return redirect(f"/web/login?{params}")
        #
        # return super().registration_confirm(event, **post)
        # Check if the unique email validation is enabled for registration
        company = request.env.company
        print(company.event_registration_unique_email)
        if company.event_registration_unique_email == True:
            if not request.env['ir.http']._verify_request_recaptcha_token('website_event_registration'):
                raise UserError(_('Suspicious activity detected by Google reCaptcha.'))

            # Check if the user is logged in
            if request.env.user._is_public():
                print("User is NOT logged in :")
                _logger.info("User is NOT logged in (public user).")
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
                            message = _("The email you entered is already associated with an account. Please log in.")
                            params = url_encode({
                                'message': message,
                                'redirect': '/event'
                            })
                            return redirect(f"/web/login?{params}")

        return super().registration_confirm(event, **post)
