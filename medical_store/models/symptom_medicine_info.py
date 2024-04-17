from odoo import *


class SymptomMedicineInfo(models.Model):
    _name = 'symptom.medicine.info'

    name_id = fields.Many2one('medicine.registration', string="Medicine name")
    med_symptoms = fields.Many2many('health.symptoms',string='Number of symptoms')

    @api.onchange('name_id')
    def onchange_medicine_id(self):
        if self.name_id:
            find_symptom = self.env['medicine.registration'].search([('name', '=', self.name_id.id)])
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",find_symptom)
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",list(find_symptom.symptoms_ids))
            self.med_symptoms=find_symptom.symptoms_ids










