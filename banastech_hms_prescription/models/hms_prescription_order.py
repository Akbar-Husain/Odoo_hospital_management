from odoo import api, fields, models
from odoo.tools.translate import _
from odoo import netsvc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
import time


class HMSPrescriptionOrder(models.Model):
    _name='prescription.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'creation_date desc, id desc'

    @api.model
    def _get_default_warehouse(self):
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
        return warehouse_ids and warehouse_ids[0] or False

    @api.model
    def _get_picking_type(self):
        res = self.env['stock.picking.type'].search([('name', '=', 'Receipts')], limit=1)
        return res and res[0] or False

    @api.model
    def _current_user_doctor(self):
        self.doctor_id =  False
        ids = self.env['banas.hms.doctor'].search([('user_id', '=', self.env.user.id)])
        if ids:
            self.doctor_id = ids[0].id

    @api.model
    def _patient_age_cal(self):
        for rec in self:
            rec.patient_age = rec.patient_id and rec.patient_id.age or ''


    sale_id = fields.Many2one('sale.order', ondelete="restrict", string='Sale Order', help="Sale order created for this prescription")
    purchase_id = fields.Many2one('purchase.order', ondelete="restrict", string='Purchase Order', help='Purchase order created for this prescription')
    picking_id = fields.Many2one('stock.picking', ondelete="restrict", string='Delivery Order')
    warehouse_id = fields.Many2one('stock.warehouse', ondelete="restrict", string='Warehouse', default=_get_default_warehouse)
    pathology = fields.Many2one('banas.hms.diseases', ondelete="set null", string='Disease')
    group_id = fields.Many2one('medicament.group', ondelete="set null", string='Medicaments Group')
    patient_id = fields.Many2one('banastech.hms.patient', ondelete="restrict", string='Patient', required=True)
    pregnancy_warning = fields.Boolean(string='Pregancy Warning')
    notes = fields.Text(string='Prescription Notes')
    prescription_line = fields.One2many('prescription.line', 'prescription_id', string='Prescription line')
    pharmacy = fields.Many2one('res.partner', ondelete="cascade", string='Pharmacy')
    company_id = fields.Many2one('res.company', ondelete="cascade", string='Pharmacy',default=lambda self: self.env.user.company_id)
    prescription_date = fields.Datetime(string='Prescription Date', required=True, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    prescription_warning_ack = fields.Boolean( string='Prescription verified')
    doctor_id = fields.Many2one('banas.hms.doctor', ondelete="restrict", string='Prescribing Doctor', default=_current_user_doctor)
    doc_user_prescription = fields.Many2one('res.users',ondelete="restrict", string='Packaging Type',related='doctor_id.user_id', readonly=False, store=True)
    name = fields.Char(size=256, string='Prescription ID', help='Type in the ID of this prescription', readonly=True)
    no_invoice = fields.Boolean(string='Invoice Exempt')
#     invoice_status = fields.Selection([('invoiced','Invoiced'),('tobe','To be Invoiced')],string='Invoice Status',default='tobe')
    creation_date = fields.Datetime(string='Creation Date', required=True, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    created_by = fields.Many2one('res.users', ondelete="restrict", string='Created By', required=True, default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('prescription', 'Prescribed'),
        ('po_created', 'PO Created'),
        ('canceled', 'Cancelled'),
        ('so_created', 'Sold'),
        #('invoiced', 'Invoiced'),
        ('invoice_exempt', 'Invoice Exempt')], string='State', default='draft')
#     invoice_id = fields.Many2one('account.invoice', ondelete="restrict", string='Invoice')
    appointment = fields.Many2one('banastech.hms.appointment', ondelete="restrict", string='Appointment')
    picking_type_id = fields.Many2one('stock.picking.type',ondelete="restrict", string='Picking Type',default=_get_picking_type)
    patient_age = fields.Char(compute=_patient_age_cal, string='Age')
#     #from Indoor patient medicine req
    ipmr_date = fields.Date(string='Request Date', required=True, readonly=True, default=fields.Date.context_today)
    location_id = fields.Many2one('stock.location', ondelete="restrict", string='Delivery Location')
    language = fields.Selection(related="patient_id.language", String="Language")
#     prescription = fields.Boolean()

#     @api.model
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'draft':
            return 'banastech_hms_prescription.mt_alert_patient_message_id_draft'
        elif 'state' in init_values and self.state == 'prescription':
            return 'banastech_hms_prescription.mt_alert_patient_message_id_Prescription'
        elif 'state' in init_values and self.state == 'so_created':
            return 'banastech_hms_prescription.mt_alert_patient_message_id_sold'
        elif 'state' in init_values and self.state == 'invoice_exempt':
            return 'banastech_hms_prescription.mt_alert_patient_message_id_invoiced_exempt'
        elif 'state' in init_values and self.state == 'canceled':
            return 'banastech_hms_prescription.mt_alert_patient_message_id_invoiced_cancel'
        return super(HMSPrescriptionOrder, self)._track_subtype(init_values)


    @api.onchange('warehouse_id')
    def onchange_warehouse_id(self):
        if self.warehouse_id and self.warehouse_id.company_id:
            self.company_id = self.warehouse_id.company_id

    @api.onchange('group_id')
    def on_change_group_id(self):
        product_lines = []
        for rec in self:
            for line in rec.group_id.medicine_list:
                product_lines.append((0,0,{
                    'product_id': line.template.id,
                    'dose_unit': line.dose_unit.id,
                    'dose': line.dose,
                    'active_component_ids': [(6, 0, [x.id for x in line.active_component_ids])],
                    'form' : line.form.id,
                }))
            rec.prescription_line = product_lines

    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise UserError(_('Prescription Order can be delete only in Draft state.'))
        return super(HMSPrescriptionOrder, self).unlink()

    @api.model
    def action_stock_move(self):
        stock_location_obj = self.env['stock.location']
        for rec in self:
            wf_service = netsvc.LocalService('workflow')
            picking = self.env['stock.picking'].create({
                'partner_id' : rec.patient_id.partner_id.id,
                'date' : fields.Datetime.now(),
                'company_id': rec.company_id.id,
                'picking_type_id': rec.picking_type_id.id
            })
            for line in rec.prescription_line:
                stock_move_dic = {
                    'product_id': line.product_id.id,
#                     'product_uom_qty': line.dose,
#                     'product_uom': line.dose_unit.id,
                    'date': fields.Datetime.now(),
#                     'date_expected': fields.Datetime.now(),
                    'picking_id': new_id,
#                     'invoice_state': 'none',
                    'state': 'draft',
                    'name': line.product_id.name,
                }
                stock_move_dic['location_id'] = stock_location_obj.search([('name','=','Stock')])[0]
                stock_move_dic['location_dest_id'] = stock_location_obj.search([('name','=','Customers')])[0]
                self.env['stock.move'].create(stock_move_dic)
            picking.action_confirm()
            picking.action_assign()
            picking.force_assign()
            picking.do_enter_transfer_details()
            for line in rec.prescription_line:
                transfer_id = self.env['stock.pack.operation'].search([('product_id', '=', line.product_id.id),('picking_id','=',new_id)])
                transfer_id.write({'lot_id': line.batch_no.id})
            picking.do_transfer()
        self.write({'state': 'deliver', 'picking_id': picking.id})
        return True

    def action_view_purchase(self):
        mod_obj = self.env['ir.model.data']
        form_res = mod_obj._context.get('purchase', 'purchase_order_form')
        form_id = form_res and form_res[1] or False
        tree_res = mod_obj._context.get('purchase', 'purchase_order_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase order',
            'res_model': 'purchase.order',
            'domain': [('id','=', self.purchase_id.id)],
            'view_mode': 'form',
            'res_id': self.purchase_id.id,
            # 'view_type': 'tree,form',
            # 'view_id': form_id,
            # 'views': [(form_id, 'form')],
        }

    def action_view_sale(self):
        mod_obj = self.env['ir.model.data']
        form_res = mod_obj._context.get('sale', 'view_order_form')
        form_id = form_res and form_res[1] or False
        tree_res = mod_obj._context.get('sale', 'view_order_tree')
        tree_id = tree_res and tree_res[1] or False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale order',
            'res_model': 'sale.order',
            'domain': [('id','=', self.sale_id.id)],
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.sale_id.id,
            # 'view_type': 'tree,form',
            # 'view_id': form_id,
            # 'views': [(form_id, 'form')],
        }

    def action_purchase_order(self):
        for rec in self:
            order = self.env['purchase.order'].create({
                'partner_id' : rec.patient_id.partner_id.id,
                # 'partner_id' : rec.patient_id.partner_id.id,
                'date_order' : fields.Datetime.now(),
                # 'location_id':  rec.location_id and rec.location_id.id or rec.picking_type_id.default_location_dest_id.id,
                # 'invoice_method': 'order',
            })
            for line in rec.prescription_line:
                line = self.env['purchase.order.line'].create({
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity,
                    'product_uom': line.product_id.uom_po_id.id,
                    'order_id': order.id,
#                     #'invoice_state': 'none',
                    'name': line.product_id.name,
                    'price_unit': line.product_id.lst_price,
                    'date_planned': fields.Datetime.now(),
                })
            so_id = self.env['sale.order'].search([('name', '=', order.partner_ref)])
            self.write({'state': 'po_created', 'purchase_id': order.id, 'sale_id': so_id and so_id[0].id or False})
        return True

    def action_sale_order(self):
        for ip_req in self:
            order = self.env['sale.order'].create({
                'partner_id' : ip_req.patient_id.partner_id.id,
                'date_order' : fields.Datetime.now(),
    #             'location_id': ip_req.patient_id.property_stock_customer.id,
    #             'invoice_method': 'picking',
                # 'doctor_id': ip_req.doctor_id.id,
                'origin': ip_req.name,
            })
            for line in ip_req.prescription_line:
                line = self.env['sale.order.line'].create({
                    'product_id': line.product_id.id,
                    # 'product_qty': line.quantity,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'order_id': order.id,
                    'name': line.product_id.name,
                    'price_unit': line.product_id.lst_price,
                })
            self.write({'state': 'so_created', 'sale_id': order.id})
        return True


    # @api.model
    # def action_view_invoice(self):
    #     mod_obj = self.env['ir.model.data']

    #     result = mod_obj._context.get('account', 'action_invoice_tree1')
#         id = result and result[1] or False
#         result = self.env['ir.actions.act_window'].read([id])[0]
#         #compute the number of invoices to display
#         inv_ids = []
#         inv_ids = [inv.id for inv in self.invoice_id]
#         #choose the view_mode accordingly
#         if len(inv_ids)>1:
#             result['domain'] = "[('id','in',["+','.join(map(str, inv_ids))+"])]"
#         else:
#             res = mod_obj._context.get('account', 'invoice_form')
#             result['views'] = [(res and res[1] or False, 'form')]
#             result['res_id'] = inv_ids and inv_ids[0] or False
#         return result

#     @api.multi
#     def action_view_picking(self):
#         mod_obj = self.env['ir.model.data']
#         result = mod_obj._context.get('stock', 'action_picking_tree')
#         id = result and result[1] or False
#         result = self.env['ir.actions.act_window'].read([id])[0]
#         #compute the number of invoices to display
#         picking_ids = [pic.id for pic in self.picking_id]
#         #choose the view_mode accordingly
#         if len(picking_ids)>1:
#             result['domain'] = "[('id','in',["+','.join(map(str, picking_ids))+"])]"
#         else:
#             res = mod_obj._context.get('stock', 'view_picking_form')
#             result['views'] = [(res and res[1] or False, 'form')]
#             result['res_id'] = picking_ids and picking_ids[0] or False
#         return result

    @api.model
    def print_prescription(self):
        datas = {
            'model': 'prescription.order',
            'ids': self.ids,
            'form': self.read(),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'patient.prescription.order', 'datas': datas}

    def button_reset(self):
        self.write({'state': 'draft'})

    def button_confirm(self):
        for app_id in self:
            if not app_id.prescription_line:
                raise UserError(_('You cannot confirm a prescription order without any order line.'))

            self.write({
                'state': 'prescription' ,#if app_id.no_invoice==False else 'invoice_exempt',
                'name': self.env['ir.sequence'].next_by_code('prescription.order') or '/'
            })

class HMSAppointment(models.Model):
    _inherit='banastech.hms.appointment'

    @api.model
    def button_pres_req(self, values):
        return {
            'res_model': 'prescription.order',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'view_id' : self.env.ref('banastech_hms_prescription.view_banastech_hms_prescription_order_form').id,
            # 'name': _('Prescriptions'),
            # 'view_type': 'form',
            'domain': [('appointment', '=', self.id)],
            # 'context': {'default_patient_id': self.patient_id.id,'default_doctor_id':self.doctor_id.id,'default_appointment': self.id},
        }