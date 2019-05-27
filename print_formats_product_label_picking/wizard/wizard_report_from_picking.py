# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import api, models, fields, _, exceptions


class WizProductLabelFromPicking(models.TransientModel):
    _inherit = 'wiz.product.label'

    picking_quantity = fields.Selection(
        selection=[
            ('one', 'One label for each product'),
            ('line', 'One label for each line'),
            ('total', 'Total product quantity'),
            ('free', 'Free print')],
        string='Quantity',
        default='total')
    state = fields.Selection(
        string='State',
        selection=[('step_1', 'Step 1'),
                   ('step_2', 'Step 2'),
                   ('done', 'Done')],
        required=True,
        default='step_1')
    line_ids = fields.One2many(
        comodel_name='wiz.product.label.line',
        inverse_name='label_id',
        string='Lines')

    @api.multi
    def _reopen_view(self):
        view = self.env.ref('print_formats_product_label_picking.'
                            'wizard_product_label_from_picking')
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.ids[0],
            'res_model': self._name,
            'view_id': view.id,
            'target': 'new',
            'context': {}}

    @api.multi
    def button_next_step(self):
        self.ensure_one()
        if self.picking_quantity == 'free':
            picking_ids = self.env.context['active_ids']
            for picking in self.env['stock.picking'].browse(picking_ids):
                if not picking.pack_operation_ids:
                    raise exceptions.Warning(
                        _('No operations to print the picking: %s.') % (
                            picking.name))
                for operation in picking.pack_operation_ids:
                    self.env['wiz.product.label.line'].create({
                        'label_id': self.id,
                        'operation_id': operation.id,
                        'quantity': int(operation.product_qty)})
            self.state = 'step_2'
        else:
            self.state = 'done'
        return self._reopen_view()

    @api.multi
    def button_print_from_picking(self):
        move_ids = []
        operation_ids = []
        picking_ids = self.env.context['active_ids']
        if self.picking_quantity in ['line', 'one']:
            moves = self.env['stock.move'].search([
                ('picking_id', 'in', picking_ids)])
            move_ids = [m.id for m in moves]
        if self.picking_quantity == 'one':
            [move_ids.append(m.id) for m in moves if m.id not in move_ids]
        elif self.picking_quantity == 'total':
            for picking in self.env['stock.picking'].browse(picking_ids):
                [[operation_ids.append(op.id)
                  for item in range(int(op.product_qty))]
                 for op in picking.pack_operation_ids]
            if not operation_ids:
                raise exceptions.Warning(_(
                    'No operations, to print this type of label you must '
                    'transfer the picking.'))
        elif self.picking_quantity == 'free':
            [[operation_ids.append(line.operation_id.id)
              for item in range(int(line.quantity))]
             for line in self.line_ids]
        if not move_ids and not operation_ids:
            raise exceptions.Warning(_('No labels for print'))
        object_ids = (
            self.picking_quantity in ('total', 'free') and operation_ids or
            move_ids)
        render_func = 'render_product_picking_label'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': self.report_id.report_name,
            'datas': {
                'ids': object_ids,
                'picking_quantity': self.picking_quantity},
            'context': {
                'render_func': render_func,
                'report_name': self.report_id.report_name}}


class WizProductLabelFromPickingLine(models.TransientModel):
    _name = 'wiz.product.label.line'
    _description = 'Wizard Product Label Line'

    label_id = fields.Many2one(
        comodel_name='wiz.product.label',
        string='Label',
        required=True)
    operation_id = fields.Many2one(
        comodel_name='stock.pack.operation',
        string='Related Packing Operations',
        required=True)
    product_id = fields.Many2one(
        related='operation_id.product_id')
    picking_id = fields.Many2one(
        related='operation_id.picking_id')
    quantity = fields.Integer(
        string='Quantity')
