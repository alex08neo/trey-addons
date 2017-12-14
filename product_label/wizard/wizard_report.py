# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import models, fields, api


class WizProductLabel(models.TransientModel):
    _name = 'wiz.product.label'
    _description = 'Wizard to report label'

    def _get_default_report(self):
        report_ids = self.env['ir.actions.report.xml'].search(
            [('name', 'ilike', '(product_label)')])
        return report_ids[0]

    report_id = fields.Many2one(
        comodel_name='ir.actions.report.xml',
        string='Report',
        domain=[('name', 'ilike', '(product_label)')],
        default=_get_default_report,
        required=True
    )

    def getPrice(self, product):
        pricelists = self.env['product.pricelist'].search([
            ('name', 'ilike', 'Public Pricelist'), ('type', '=', 'sale')])

        if not pricelists.exists():
            pricelists = self.env['product.pricelist'].search([
                ('type', '=', 'sale')])

        if pricelists:
            prices = pricelists[0].price_get(product.id, 1)
            price_unit = prices[pricelists[0].id]
            price = product.taxes_id.compute_all(price_unit, 1)
            return price['total_included']
        else:
            return 0.00

    @api.multi
    def button_print(self):
        datas = {'ids': self.env.context['active_ids']}

        return {
            'type': 'ir.actions.report.xml',
            'report_name': self.report_id.report_name,
            'datas': datas,
            'context': {
                'render_func': 'render_product_label',
                'report_name': self.report_id.report_name
            },
        }
