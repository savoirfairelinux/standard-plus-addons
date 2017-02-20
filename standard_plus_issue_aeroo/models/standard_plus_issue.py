# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StandardPlusIssue(models.Model):
    _inherit = ['standard.plus.issue']

    type = fields.Selection(
        selection_add=[
            ('aeroo', 'Aeroo'),
        ],
    )

    report_name = fields.Char(
        string='Report Name',
    )

    report_out_format = fields.Selection(
        string='Output Format',
        selection=[
            ('odt', 'ODT'),
            ('pdf', 'PDF'),
            ('doc', 'DOC'),
        ],
        default='odt',
    )

    report_source = fields.Selection(
        string='Source Type',
        selection=[
            ('file', 'One File'),
            ('lang', 'Different Template per Language'),
        ],
        default='file',
    )

    report_lang_determinant = fields.Selection(
        string='Language Determinant',
        selection=[
            ('partner', 'Partner'),
            ('employee', 'Employee'),
            ('other', 'Other'),
        ],
        help="Used to determine the language of the "
             "record being printed in the report.",
        default='partner',
    )

    report_line_ids = fields.One2many(
        string='Template by Language',
        comodel_name='standard.plus.report.line',
        inverse_name='issue_id',
    )

    @api.constrains('no_screenshot', 'screenshot_ids', 'type')
    def _check_screenshots(self):
        if self.type != 'aeroo':
            super(StandardPlusIssue, self)._check_screenshots()


    @api.constrains('type', 'report_source', 'report_line_ids')
    def _check_report_line_ids(self):
        """
        Check if report templates are correctly uploaded
        """
        if self.type == 'aeroo':
            if not self.report_line_ids:
                raise ValidationError(_(
                    "Please upload a report template."
                ))
            if self.report_source == 'lang' and (
                len(self.report_line_ids) != (
                    len(self.report_line_ids.mapped('lang_id'))
                )
            ):
                raise ValidationError(_(
                    "Please specify a language for each template."
                ))

    @api.multi
    def action_set_submitted(
        self, context=None,
        template_ref='standard_plus_issue.email_template_standard_plus_issue'
    ):
        self.ensure_one()
        if self.type == 'aeroo':
            template_ref = (
                'standard_plus_issue_aeroo.'
                'email_template_standard_plus_issue_aeroo'
            )
        super(StandardPlusIssue, self).action_set_submitted(
            context, template_ref
        )

    @api.multi
    def prepare_mail_attachments(self):
        """
        For 'aeroo' type, add report templates to the attachments to
        be sent by email
        """
        attachment_ids = (
            super(StandardPlusIssue, self).prepare_mail_attachments()
        )
        AttachmentObj = self.env['ir.attachment']
        for report_line in self.report_line_ids:
            attachment = AttachmentObj.create({
                'datas': report_line.file,
                'datas_fname': report_line.filename,
                'name': report_line.filename,
            })
            attachment_ids.append(attachment.id)
        return attachment_ids
