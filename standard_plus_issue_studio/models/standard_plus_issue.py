# -*- coding: utf-8 -*-
# © 2017-2018 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import tempfile

from odoo import api, fields, models
from odoo.addons.web_studio.controllers import export


class StandardPlusIssue(models.Model):
    _inherit = ['standard.plus.issue']

    type = fields.Selection(
        selection_add=[
            ('studio', 'Studio'),
        ],
    )

    studio_module = fields.Binary(
        string='Custom Module',
        readonly=True,
    )

    studio_module_filename = fields.Char(
        string='Filename',
        default='studio_customization.zip'
    )

    studio_retrieval_date = fields.Datetime(
        string='Retrieval Date',
        readonly=True,
    )

    @api.multi
    def action_set_submitted(
        self, context=None,
        template_ref='standard_plus_issue.email_template_standard_plus_issue'
    ):
        """
        For 'studio' type, retrieve studio_customization module and call the
        adequate email template
        """
        self.ensure_one()
        if self.type == 'studio':
            self.retrieve_studio_module()
            template_ref = (
                'standard_plus_issue_studio.'
                'email_template_standard_plus_issue_studio'
            )
        super(StandardPlusIssue, self).action_set_submitted(
            context, template_ref
        )

    @api.multi
    def retrieve_studio_module(self):
        """
        Populate 'studio_module' with a zip file containing
        studio_customization data and save timestamp.
        """
        self.ensure_one()
        studio_module = self.env['ir.module.module'].get_studio_module()
        data = self.env['ir.model.data'].search([('studio', '=', True)])
        with tempfile.TemporaryFile('wb+') as tf:
            tf.write(export.generate_archive(studio_module, data))
            tf.seek(0)
            self.studio_module = base64.b64encode(tf.read())
        self.studio_retrieval_date = fields.Datetime.now()

    @api.multi
    def prepare_mail_attachments(self):
        """
        For 'studio' type, add studio_customization zip to the attachments to
        be sent by email
        """
        attachment_ids = (
            super(StandardPlusIssue, self).prepare_mail_attachments()
        )
        if self.type == 'studio':
            AttachmentObj = self.env['ir.attachment']
            attachment = AttachmentObj.create({
                'datas': self.studio_module,
                'datas_fname': self.studio_module_filename,
                'name': self.studio_module_filename,
            })
            attachment_ids.append(attachment.id)
        return attachment_ids
