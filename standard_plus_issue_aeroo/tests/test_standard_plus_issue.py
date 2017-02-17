# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import os

from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestStandardPlusIssue(TransactionCase):

    def setUp(self):
        super(TestStandardPlusIssue, self).setUp()

        self.IssueObj = self.env['standard.plus.issue']
        self.ReportLineObj = self.env['standard.plus.report.line']
        self.AttachmentObj = self.env['ir.attachment']

        here = os.path.abspath(os.path.dirname(__file__))
        report_path = os.path.join(here, "test_report.odt")
        with open(report_path, "rb") as report_file:
            encoded_report = base64.b64encode(report_file.read())

        self.report = self.ReportLineObj.create({
            'filename': 'test_report.odt',
            'file': encoded_report,
            'lang_id': self.env.ref("base.lang_en").id,
        })

        self.issue = self.IssueObj.create({
            'type': 'aeroo',
            'no_screenshot': True,
            'report_line_ids': [(6, 0, [self.report.id])],
            'report_source': 'lang',
        })

    def test_check_screenshots(self):
        self.issue.no_screenshot = False
        with self.assertRaises(ValidationError):
            self.issue.type = 'support'

    def test_check_report_line_ids(self):
        with self.assertRaises(ValidationError):
            self.report.lang_id = False
            self.issue.report_line_ids = [(6, 0, [self.report.id])]
        with self.assertRaises(ValidationError):
            self.issue.report_line_ids = False

    def test_action_set_submitted(self):
        attachment_count = self.AttachmentObj.search_count([])
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_submitted()
        self.assertEqual(self.issue.state, 'submitted')
        self.assertEqual(
            attachment_count, self.AttachmentObj.search_count([])
        )

    def test_prepare_mail_attachments(self):
         self.assertTrue(self.issue.no_screenshot)
         self.assertEqual(self.issue.type, 'aeroo')
         attachment_count = self.AttachmentObj.search_count([])
         self.issue.prepare_mail_attachments()
         self.assertEqual(
             attachment_count + len(self.issue.report_line_ids),
             self.AttachmentObj.search_count([])
         )
