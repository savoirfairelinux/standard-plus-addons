# -*- coding: utf-8 -*-
# © 2018 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class BaseConfigSettings(models.TransientModel):

    _inherit = 'base.config.settings'

    property_support_email = fields.Char(
        string='Support Email',
    )

    @api.model
    def get_default_support_email(self, fields):
        support_email = self.env['ir.config_parameter'].sudo(
        ).get_param('property_support_email')
        return {'property_support_email': support_email}

    @api.multi
    def set_support_email(self):
        for rec in self:
            self.env['ir.config_parameter'].set_param(
                'property_support_email', rec.property_support_email or '')
