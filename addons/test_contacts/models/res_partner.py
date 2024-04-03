from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    GENDER_SELECTION = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    x_coordinate = fields.Float(string='X Coordinate', required=True)
    y_coordinate = fields.Float(string='Y Coordinate', required=True)
    gender = fields.Selection(GENDER_SELECTION, string='Gender', required=False)