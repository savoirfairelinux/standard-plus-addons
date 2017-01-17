# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Standard+ Issue',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Others',
    'summary': 'Standard+ Issue',
    'depends': [
        'web'
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'views/standard_plus_issue_templates.xml',
    ],
    'images': [
        'static/img/sfl_logo.png',
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
