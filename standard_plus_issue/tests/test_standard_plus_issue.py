# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestStandardPlusIssue(TransactionCase):

    def setUp(self):
        super(TestStandardPlusIssue, self).setUp()

        self.IssueObj = self.env['standard.plus.issue']
        self.ScreenshotObj = self.env['issue.screenshot']

        self.screenshot = self.ScreenshotObj.create({
            'filename': 'screenshot.jpg',
        })

        self.issue = self.IssueObj.create({
            'screenshot_ids': [(6, 0, [self.screenshot.id])],
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
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_submitted()
        self.assertEqual(self.issue.state, 'submitted')

    def test_action_set_addressed(self):
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_addressed()
        self.assertEqual(self.issue.state, 'addressed')

    def test_action_set_rejected(self):
        self.assertEqual(self.issue.state, 'draft')
        self.issue.action_set_rejected()
        self.assertEqual(self.issue.state, 'rejected')
