from odoo import api, fields, models
from odoo.tools.translate import _

# class SaleOrderLineProduct(models.Model):
#     _inherit = 'sale.order.line'

#     @api.onchange('product_uom_qty', 'batch_no', 'sale_on_cost')
#     def onchange_batch(self):
#         if not self.batch_no:
#             return {'value': {}} 
#         data = self.env['stock.production.lot'].browse(batch_no)
#         if data.qty_lot < product_uom_qty and data.qty_count:
#             return {'warning': {'title': 'Warning!', 'message': _('Not enough stock of batch ! : You plan to sell %s Unit(s) but you only have %s Unit(s) available ') % (product_uom_qty, data.qty_lot)}}

#         if self.sale_on_cost:
#             if data.purchase_uom.factor_inv > 1 :
#                 return {'value': {'exp_date': data.use_date, 'price_unit': data.purchase_price / data.purchase_uom.factor_inv}}
#             else:
#                 return {'value': {'exp_date': data.use_date, 'price_unit': data.purchase_price}}
#         else:
#             return {'value': {'exp_date': data.use_date, 'price_unit': data.sale_price}}  

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    purchase_price = fields.Float(string='Purchase Charges')
    # purchase_uom = fields.Many2one('product.uom', ondelete='restrict', string='Purchase UOM')
    mrp = fields.Float(string='MRP', required=True)       
    # sale_uom = fields.Many2one('product.uom', ondelete='restrict', string='Sale UOM')
    sale_price = fields.Float(string='Sale Charges')

    # @api.model
    # def default_get(self, fields):
    #     res = super(StockProductionLot, self).default_get(fields)
    #     context = self._context or {}
    #     product_id = context.get('product_id')
    #     if context.get('product_id'):
    #         move = self.env['stock.move'].search([('product_id','=',product_id)])
    #         for item in move:
    #             product = self.env['product.product'].browse(product_id)
    #         if 'sale_uom' in fields:
    #             res.update({'sale_uom': product.uom_id.id})
    #         if 'purchase_uom' in fields:
    #             res.update({'purchase_uom': product.uom_po_id.id})
    #     return res