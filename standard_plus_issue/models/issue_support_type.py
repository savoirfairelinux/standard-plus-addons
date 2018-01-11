# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IssueSupportType(models.Model):
    """Standard+ Issue Support Type"""

    _name = 'issue.support.type'
    _description = __doc__
    _order = 'sequence,name'

    name = fields.Char(
        string='name',
        required=True,
    )
    sequence = fields.Integer(default=1)
    active = fields.Boolean(string="Active", default=True)
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('uniq_support_name', 'unique( name )', 'Support Type must be unique.')
    ]
