# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import os

from openerp.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestStandardPlusIssue(TransactionCase):

    def setUp(self):
        super(TestStandardPlusIssue, self).setUp()

        self.IssueObj = self.env['standard.plus.issue']
        self.ScreenshotObj = self.env['issue.screenshot']
        self.AttachmentObj = self.env['ir.attachment']
        self.support_type = self.env.ref('standard_plus_issue.issue_support_type_evolution')

        here = os.path.abspath(os.path.dirname(__file__))
        image_path = os.path.join(here, "../static/img/test_image.png")
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())

        self.screenshot = self.ScreenshotObj.create({
            'filename': 'screenshot.jpg',
            'screenshot': encoded_image,
        })

        self.issue = self.IssueObj.create({
            'screenshot_ids': [(6, 0, [self.screenshot.id])],
            'support_type_id': self.support_type.id,
        })

    def test_compute_issue_url(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        db_name = self.issue.pool.db_name
        self.assertEqual(
            self.issue.issue_url,
            "%s/web?db=%s#id=%s&view_type=form&model=standard.plus.issue"
            % (base_url, db_name, self.issue.id)
        )

    def test_default_user_id(self):
        self.assertEqual(self.issue.user_id, self.env.user)

    def test_check_screenshots(self):
        with self.assertRaises(ValidationError):
            self.issue.screenshot_ids = False

    def test_name(self):
        issue2 = self.IssueObj.create({
            'no_screenshot': True,
            'support_type_id': self.support_type.id,
        })
        self.assertEqual(
            (issue2.name[:2], int(issue2.name[2:5])),
            ('SU', (int(self.issue.name[2:5]) + 1))
        )

    def test_action_set_escalated(self):
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_escalated()
        self.assertEqual(self.issue.state, 'escalated')

    def test_action_set_submitted(self):
        attachment_count = self.AttachmentObj.search_count([])
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_submitted()
        self.assertEqual(self.issue.state, 'submitted')
        self.assertEqual(attachment_count, self.AttachmentObj.search_count([]))

    def test_action_set_addressed(self):
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_addressed()
        self.assertEqual(self.issue.state, 'addressed')

    def test_action_set_rejected(self):
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_rejected()
        self.assertEqual(self.issue.state, 'rejected')

    def test_prepare_mail_attachments(self):
        attachment_count = self.AttachmentObj.search_count([])
        self.issue.prepare_mail_attachments()
        self.assertEqual(
            attachment_count + len(self.issue.screenshot_ids),
            self.AttachmentObj.search_count([])
        )
