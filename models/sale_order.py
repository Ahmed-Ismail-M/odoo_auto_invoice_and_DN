from odoo import api, fields, models, exceptions


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """ Override the original confirm action to automatically create invoice and validate delivery note"""
        res = super(SaleOrder, self).action_confirm() 
        stock_pickings = self.env['stock.picking'].search([('sale_id', '=', self.id)]) # get the created delivery note objects
        for picking in stock_pickings:
            picking.button_validate() # validate the D N 
        created_inv = self._create_invoices( grouped=False, final=True, date=None) # create new invoice for the quotation
        created_inv.action_post() # post the invoice to accounting
        return res  
