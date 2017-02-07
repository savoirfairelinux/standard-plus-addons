# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IssueScreenshot(models.Model):
    """
    Issue Screenshot
    """
    _name = 'issue.screenshot'

    screenshot = fields.Binary(
        string='Screenshot',
    )

    filename = fields.Char(
        string="Filename",
    )

    comment = fields.Char(
        string='Comment',
    )

    issue_id = fields.Many2one(
        comodel_name='standard.plus.issue',
    )
