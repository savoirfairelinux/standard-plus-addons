# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests import TransactionCase
from odoo import fields


class TestStandardPlusIssue(TransactionCase):

    def setUp(self):
        super(TestStandardPlusIssue, self).setUp()

        self.IssueObj = self.env['standard.plus.issue']
        self.DataObj = self.env['ir.model.data']
        self.AttachmentObj = self.env['ir.attachment']

        self.issue = self.IssueObj.create({
            'no_screenshot': True,
            'type': 'studio',
        })

        self.studio_custom_data = self.DataObj.create({
            'name': 'test_studio',
            'model': 'res.partner',
            'module': 'studio_customization',
            'studio': True,

        })

    def test_action_set_submitted(self):
        attachment_count = self.AttachmentObj.search_count([])
        self.assertEqual(self.issue.state, 'draft')
        self.assertFalse(self.issue.studio_retrieval_date)
        self.issue.action_set_submitted()
        self.assertTrue(self.issue.studio_module)
        self.assertTrue(self.issue.studio_retrieval_date)
        self.assertEqual(self.issue.state, 'submitted')
        self.assertEqual(
            attachment_count, self.AttachmentObj.search_count([])
        )

    def test_prepare_mail_attachments(self):
        self.assertTrue(self.issue.no_screenshot)
        self.assertEqual(self.issue.type, 'studio')
        attachment_count = self.AttachmentObj.search_count([])
        self.issue.prepare_mail_attachments()
        self.assertEqual(
            attachment_count + 1, self.AttachmentObj.search_count([])
        )
