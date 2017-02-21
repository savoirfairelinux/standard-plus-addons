# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Standard+ Issue Aeroo',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Helpdesk',
    'summary': 'Standard+ Issue Aeroo',
    'depends': [
        'standard_plus_issue',
        'report_aeroo',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'data/template_email_standard_plus_issue.xml',
        'security/ir.model.access.csv',
        'views/standard_plus_issue.xml',
    ],
    'installable': True,
    'application': False,
}
