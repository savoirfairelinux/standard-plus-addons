# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StandardPlusIssue(models.Model):
    """
    Standard+ Issue
    """
    _name = 'standard.plus.issue'
    _description = __doc__
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Reference',
        readonly=True,
    )

    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('escalated', 'Escalated'),
            ('submitted', 'Submitted'),
            ('addressed', 'Addressed'),
            ('rejected', 'Rejected'),
        ],
        default='draft',
        required=True,
    )

    type = fields.Selection(
        string='Type',
        selection=[
            ('support', 'Support'),
        ],
        default='support',
        required=True,
    )

    module_id = fields.Many2one(
        string='Module',
        comodel_name='ir.module.module',
        domain="[('state', '=', 'installed'), "
               "('application', '=', True)]",
    )

    model_id = fields.Many2one(
        string='Object',
        comodel_name='ir.model',
    )

    user_id = fields.Many2one(
        string="User",
        comodel_name='res.users',
        readonly=True,
        default=lambda self: self.env.user.id,
    )

    priority = fields.Selection(
        string='Priority',
        selection=[
            ('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')
        ],
        default='2',
    )

    description_before = fields.Text(
        string='Description of the Observed Behavior',
    )

    description_after = fields.Text(
        string='Description of the Desired Behavior',
    )

    no_screenshot = fields.Boolean(
        default=False,
    )

    screenshot_ids = fields.One2many(
        string='Screenshots',
        comodel_name='issue.screenshot',
        inverse_name='issue_id',
    )

    notes = fields.Text(
        string='Notes',
    )

    property_support_email = fields.Char(
        string='Support Email Address',
        company_dependent=True,
    )

    issue_url = fields.Char(
        string='URL of the Issue',
        compute='_compute_issue_url',
    )

    @api.multi
    def _compute_issue_url(self):
        """
        Compute the URL of the issue
        """
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        db_name = self.pool.db_name
        for rec in self:
            rec.issue_url = (
                "%s/web?db=%s#id=%s&view_type=form&model=standard.plus.issue"
                % (base_url, db_name, rec.id)
            )

    @api.constrains('no_screenshot', 'screenshot_ids')
    def _check_screenshots(self):
        """
        Check if a screenshot has been joined if no_screenshot is not checked
        """
        if not self.no_screenshot and not self.screenshot_ids:
            raise ValidationError(_(
                'Please join a screenshot.'
            ))

    @api.model
    def create(self, vals):
        """
        Add a reference (sequence)
        """
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'standard.plus.issue'
        )
        return super(StandardPlusIssue, self).create(vals)

    @api.multi
    def action_set_escalated(self):
        """
        Change the state to 'escalated'
        """
        self.ensure_one()
        self.state = 'escalated'

    @api.multi
    def action_set_submitted(
            self, context=None,
            template_ref=(
                'standard_plus_issue.email_template_standard_plus_issue'
            )
    ):
        """
        Change the state to 'submitted' and send email
        """
        self.ensure_one()
        self.send_by_email(self.prepare_mail_attachments(), template_ref)
        self.state = 'submitted'

    @api.multi
    def action_set_addressed(self):
        """
        Change the state to 'addressed'
        """
        self.ensure_one()
        self.state = 'addressed'

    @api.multi
    def action_set_rejected(self):
        """
        Change the state to 'rejected'
        """
        self.ensure_one()
        self.state = 'rejected'

    @api.multi
    def send_by_email(self, attachment_ids, template_ref):
        """
        Send the issue by email to the support
        """
        self.ensure_one()
        template = self.env.ref(template_ref)
        vals = {
            'attachment_ids': attachment_ids,
            'email_to': self.property_support_email,
        }
        template.send_mail(self.id, force_send=True, email_values=vals)
        self.env['ir.attachment'].browse(attachment_ids).unlink()

    @api.multi
    def prepare_mail_attachments(self):
        """
        Add the screenshots to the attachments to be sent by email
        """
        self.ensure_one()
        AttachmentObj = self.env['ir.attachment']
        attachment_ids = []
        for screenshot in self.screenshot_ids:
            attachment = AttachmentObj.create({
                'datas': screenshot.screenshot,
                'datas_fname': screenshot.filename,
                'name': screenshot.filename,
            })
            attachment_ids.append(attachment.id)
        return attachment_ids
