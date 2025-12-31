from odoo import http
from odoo.http import request
import json
import os

class ContactAPI(http.Controller):

    def _write_json(self):
        contacts = request.env['mon_module.contact'].sudo().search([])

        data = []
        for c in contacts:
            data.append({
                'name': c.name,
                'email': c.email,
                'phone': c.phone,
                'category': c.category_id.name if c.category_id else None,
                'related_contacts': [r.name for r in c.related_contacts],
            })

        file_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'contacts.json'
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data

    # -------- GET --------
    @http.route('/mon_module/contacts', type='http', auth='public', methods=['GET'], csrf=False)
    def get_contacts(self, **kwargs):
        return request.make_response(
            json.dumps(self._write_json(), ensure_ascii=False),
            headers=[('Content-Type', 'application/json')]
        )

    # -------- POST --------
    @http.route('/mon_module/contacts', type='http', auth='public', methods=['POST'], csrf=False)
    def contacts_api(self, **kwargs):
        # lire le JSON depuis le body
        try:
            body = request.httprequest.get_data(as_text=True)
            data = json.loads(body)
        except Exception:
            data = {}

        # si name manquant → juste retourner la liste
        if not data.get('name'):
            return request.make_response(
                json.dumps(self._write_json(), ensure_ascii=False),
                headers=[('Content-Type', 'application/json')]
            )

        # créer le contact
        vals = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
        }

        if data.get('category'):
            category = request.env['mon_module.category'].sudo().search(
                [('name', '=', data.get('category'))], limit=1
            )
            if not category:
                category = request.env['mon_module.category'].sudo().create({
                    'name': data.get('category')
                })
            vals['category_id'] = category.id

        request.env['mon_module.contact'].sudo().create(vals)

        return request.make_response(
            json.dumps(self._write_json(), ensure_ascii=False),
            headers=[('Content-Type', 'application/json')]
        )
