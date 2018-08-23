# -*- coding: utf-8 -*-
# © 2017-2018 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Standard+ Issue',
    'version': '11.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Helpdesk',
    'summary': 'Standard+ Issue',
    'depends': [
        'base_setup',
        'web',
        'document',
        'mail',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'data/ir_config_parameter.xml',
        'data/standard_plus_issue_sequence.xml',
        'data/template_email_standard_plus_issue.xml',
        'data/standard_plus_issue_support_type.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/standard_plus_issue_templates.xml',
        'views/standard_plus_issue.xml',
        'views/res_config_settings.xml',
    ],
    'images': [
        'static/img/sfl_logo.png',
        'static/img/test_image.png',
    ],
    'js': [
        'static/src/js/systray.js'
    ],
    'qweb': [
        'static/src/xml/systray.xml',
    ],
    'installable': True,
    'application': True,
}
