###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    tracking_method = fields.Selection(
        selection_add=[
            ('seur', 'SEUR'),
        ],
    )

    def _get_tracking_link_seur(self, picking):
        if not picking or not picking.carrier_tracking_ref:
            return ''
        carrier_tracking_ref = picking.carrier_tracking_ref
        return self.env['ir.config_parameter'].sudo().get_param(
            'delivery_carrier.tracking_link.seur') % carrier_tracking_ref

    def fixed_get_tracking_link(self, picking):
        res = super().fixed_get_tracking_link(picking)
        if self.tracking_method == 'seur':
            return self._get_tracking_link_seur(picking)
        return res

    def base_on_rule_get_tracking_link(self, picking):
        res = super().base_on_rule_get_tracking_link(picking)
        if self.tracking_method == 'seur':
            return self._get_tracking_link_seur(picking)
        return res
