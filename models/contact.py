from odoo import models, fields

class Contact(models.Model):
    _name = 'mon_module.contact'
    _description = 'Contact'

    name = fields.Char(string='Nom', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Téléphone')

    category_id = fields.Many2one('mon_module.category', string="Catégorie")
 
    related_contacts = fields.Many2many(
    'mon_module.contact',
    'contact_relations',
    'contact_id',
    'related_id',
    string="Contacts liés"
)
