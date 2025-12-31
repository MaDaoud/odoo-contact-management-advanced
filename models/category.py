from odoo import models, fields

class Category(models.Model):
    _name = 'mon_module.category'
    _description = 'Catégorie de contact'

    name = fields.Char(string="Nom de la catégorie", required=True)
    description = fields.Text(string="Description")
    contact_ids = fields.One2many('mon_module.contact', 'category_id', string="Contacts")
