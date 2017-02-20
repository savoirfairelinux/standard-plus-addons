# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StandardPlusReportLine(models.Model):
    """
    Standard+ Issue Report Line
    """
    _name = 'standard.plus.report.line'
    _description = __doc__

    lang_id = fields.Many2one('res.lang', 'Language')
    file = fields.Binary('File', required=True)
    filename = fields.Char('File Name')
    issue_id = fields.Many2one('standard.plus.issue')
