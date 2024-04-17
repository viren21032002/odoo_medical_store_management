from odoo import *


class MedicineInformation(models.Model):
    _name = 'health.symptoms'
    name = fields.Char(string="Symptoms")

