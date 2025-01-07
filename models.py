from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'  # Nombre del modelo
    _description = 'Mi modelo'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
