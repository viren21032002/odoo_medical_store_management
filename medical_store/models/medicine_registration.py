from odoo import *
from dateutil import relativedelta


class MedicineRegistration(models.Model):
    _name = 'medicine.registration'
    name = fields.Char(string='Medicine name')
    dosage_type=fields.Selection([('liquid', 'liquid'), ('goli', 'goli'), ('inji', 'inji')])
    symptoms_ids = fields.Many2many('health.symptoms', 'symptoms_id', string='For symptoms')

    # expiry_months = fields.Integer(string="Total lifespan of medicine in ,months", compute='_compute_medicine_lifespan')
    stock_o2m_ids = fields.One2many('stock.management', 'name_id', 'Stock')


    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        print("\n\n\n\n",name,args,operator,limit,name_get_uid)
        args = args or []
        if name:
            args = ['|',('name',operator,name),('dosage_type',operator,name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


    def name_get(self):
        result = []
        for medicine in self:
            name = medicine.name +' [ ' + str(medicine.dosage_type) + ' ] '
            result.append((medicine.id, name))
        return result

    def function_symptoms(self):
        count1=self.env['stock.management'].search([('name_id', '=', self.name)])
        action={
            'type':'ir.actions.act_window',
            'res_model':'stock.management',
            'domain':[('name_id', '=', self.name)],
            'name': 'Stock',
            'view_mode':'tree,form'
        }
        if len(count1)==1:
            action.update({
                'views':[[False,'form']],
                'view_mode':'form',
                'res_id':count1[0].id,
            })
        else:
            action.update({
                'views':[[False,'tree'],[False,'form']],
                'view_mode':'tree,form'
            })
        return action


