# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2015 Akretion (http://www.akretion.com). All Rights Reserved
#   @author Benoît GUILLOT <benoit.guillot@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    currency_rate = fields.Float(
        'Forced currency rate',
        help='You can force the currency rate on the sale with this '
        'field. This will also force it on the invoice.',
    )

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals = super(SaleOrder, self)._prepare_invoice(
            cr, uid, order, lines, context=context)
        invoice_vals.update({'currency_rate': order.currency_rate})
        return invoice_vals


class sale_advance_payment_inv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
        result = super(sale_advance_payment_inv, self)._prepare_advance_invoice_vals(
            cr, uid, ids, context=context,
        )
        for sale_id, inv_values in result:
            order = self.pool.get('sale.order').browse(
                cr, uid, sale_id, context=context)
            inv_values.update({'currency_rate': order.currency_rate})
        return result
