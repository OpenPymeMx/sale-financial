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

from openerp import api, fields, models


class sale_force_currency_rate(models.TransientModel):
    _name = 'sale.force.currency.rate'
    _description = 'Force currency rate'

    @api.model
    def _default_currency_rate(self):
        sale_order = self.env['sale.order'].browse(
            self._context.get('active_id', False),
        )
        currency = sale_order.currency_id.with_context(
            date=sale_order.date_order or fields.Date.context_today(self),
        )
        return currency.compute(1.0, sale_order.company_id.currency_id)

    currency_rate = fields.Float(
        'Forced currency rate',
        default=lambda self: self._default_currency_rate(),
        help='You can force the currency rate on the sale order with this '
        'field. It will be also set on the invoice.',
    )

    @api.multi
    def force_currency_rate(self):
        self.ensure_one()
        sale_order = self.env['sale.order'].browse(
            self._context.get('active_id', False),
        )
        sale_order.currency_rate = self.currency_rate
        return {'type': 'ir.actions.act_window_close'}
