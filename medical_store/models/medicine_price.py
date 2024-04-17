from odoo import *


class MedicinePrice(models.Model):
    _name = 'medicine.price'
    medicine_id=fields.Many2one('medicine.registration', string="Medicine")
    name=fields.Integer(string="Enter price")
