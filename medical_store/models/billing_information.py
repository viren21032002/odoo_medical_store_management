from odoo import *
from datetime import *

from odoo.exceptions import ValidationError

class MedicineInformation(models.Model):

    _name = 'medicine.information'
    # def func1(self):
    #     med_ids =self.env['stock.management'].search([('exp_date','=',context_today().strftime('%Y-%m-%d'))])
    #     print("<><><><><>",med_ids)
    #
    # d = str(datetime.today().date())
    med_id = fields.Many2one('medicine.registration', string="Medicine", required=True)
    reference_number = fields.Char(string="Reference ID", required=True)
    batch_number = fields.Char(string="Batch number", copy=False, readonly=True)
    is_major = fields.Boolean(string='Is major')
    symptoms_ids = fields.Many2many('health.symptoms', 'medicine_information_symptoms_rel',
                                 'symp_id', 'medi_id', string='Groups')
    medicine_price = fields.Integer(string="Medicine Price")
    quantity_of_medicine = fields.Integer(string="Quantity")
    total_price = fields.Integer(string="Total amount to be paid", compute='_compute_total_amount')
    available_stock = fields.Integer(string='Available stock')
    count_symptoms = fields.Integer('count of symptoms' )



    @api.onchange('med_id')
    def onchange_name(self):
        co1 = self.env['medicine.price'].search([('medicine_id', '=', self.med_id.id)])
        co2 = self.env['medicine.registration'].search([('id', '=', self.med_id.id)])
        available_stk=self.env['stock.management'].search([('name_id', '=', self.med_id.id)])
        # symptom_count = self.env['symptom.medicine.info'].search([('name_id.id', '=', self.med_id.id)])
        # self.count_symptoms = len(list(symptom_count.med_symptoms))
        # print("////////////////symp count", len(list(symptom_count.med_symptoms)))

        if not self.available_stock:
            self.available_stock = available_stk.quantity
        if self.med_id:
            self.medicine_price = co1.name
            self.symptoms_ids = co2.symptoms_ids
        else:
            self.medicine_price=0

    @api.depends('quantity_of_medicine')
    def _compute_total_amount(self):
        for field in self:
            field.total_price=0
            if field.quantity_of_medicine:
                field.total_price=field.quantity_of_medicine*field.medicine_price
            # print("--------------------------------------------------------------")
            # print(field.total_price)
            # print("--------------------------------------------------------------")




    def symptoms_medicine(self):
        count2=self.env['symptom.medicine.info'].search([('name_id.id', '=', self.med_id.id)])
        print("~~~~~~~~~~~~~~~~~~",count2)
        action={
            'type':'ir.actions.act_window',
            'res_model':'symptom.medicine.info',
            'domain':[('name_id.id', '=', self.med_id.id)],
            'name': 'Medicine',
            'view_mode':'tree,form'
        }
        return action


    def function_symptoms(self):
        count1=self.env['stock.management'].search([('name_id.id', '=', self.med_id.id)])
        action={
            'type':'ir.actions.act_window',
            'res_model':'stock.management',
            'domain':[('name_id.id', '=', self.med_id.id)],
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

    @api.model
    def create(self, vals):
        # available_stk=self.env['stock.management'].search([('name_id', '=', self.med_id.id)])
        if not vals.get('batch_number'):
            seq=self.env['ir.sequence'].next_by_code('medicine.in')
            # print("sssssssssssssssssssssssssssssssss",seq)
            # print(len(seq))
            t_d= datetime.now()
            month2 = t_d.strftime("%b")
            vals['batch_number']=seq[0:3]+'/'+month2+'/'+seq[4::]

            # print("<<<<<<<<<<<<<<",type(vals['company_name']))
        return super(MedicineInformation, self).create(vals)


