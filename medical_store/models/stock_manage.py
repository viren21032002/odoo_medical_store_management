from odoo import *
from datetime import *
from dateutil import relativedelta
from odoo.exceptions import ValidationError


class StockManagement(models.Model):
    _name = 'stock.management'
    lot_number = fields.Char('Lot Number', readonly=True, copy=False, store=True)
    name_id = fields.Many2one('medicine.registration', string="Medicine name")
    quantity = fields.Integer(string="Enter Quantity")
    mgf_date = fields.Date(string="Mgf. Date of medicine")
    exp_date = fields.Date(string="Exp. Date of medicine")
    life_span = fields.Integer(string="Lifespan of medicine",compute='_compute_medicine_lifespan', readonly=True)
    state = fields.Selection([('Expiry', 'Expiry'),
        ('Not Expiry', 'Not Expiry')
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='Expiry')

    def button_in_progress(self):
        self.write({
            'state': "Not Expiry"
        })
    @api.depends('mgf_date', 'exp_date')
    def _compute_medicine_lifespan(self):
        for rec in self:
            rec.life_span = 0
            if rec.mgf_date and rec.exp_date:
                delta = relativedelta.relativedelta(rec.exp_date, rec.mgf_date)
                # print(">>>>>>>>>>>>>>>>>>>>>",delta.months)
                rec.life_span = delta.months + (delta.years * 12)
                # print(rec.expiry_months)
    # @api.model
    # def create(self, vals):
    #     now_date = str(datetime.now().date().strftime("%Y-%m-%d"))
    #     ex_date = vals.get("exp_date")
    #     if ex_date <= now_date:
    #         raise ValidationError("This medicine is expired. Don't sell.")
    #     return super(StockManagement, self).write(vals)
    #


    # def write(self, vals):
    #     now_date=datetime.now().date().strftime("%Y-%m-%d")
    #     ex_date=vals.get("exp_date")
    #     if ex_date <= now_date:
    #         raise ValidationError("This medicine is expired. Don't sell.")
    #     return super(StockManagement, self).write(vals)

    #
    @api.model
    def create(self, vals):
        # available_stk=self.env['stock.management'].search([('name_id', '=', self.med_id.id)])
        if not vals.get('lot_number'):
            lot_number = self.env['ir.sequence'].next_by_code('lot.record')
            vals['lot_number'] = lot_number
        return super(StockManagement, self).create(vals)


    @api.model
    def default_get(self, fields):
        result=super(StockManagement, self).default_get(fields)
        if 'quantity' in fields and 'mgf_date' in fields and 'exp_date' in fields:
            result['quantity'] = 10
            result['mgf_date'] = '2023-03-31'
            result['exp_date'] = '2023-04-03'
        return result







