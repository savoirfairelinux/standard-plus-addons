/**
 * © 2017 Savoir-faire Linux
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
 */

odoo.define('standard_plus_issue.systray', function (require) {
"use strict";

var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var SflSupport = Widget.extend({
    template:'standard_plus_issue.sfl_support',

    events: {
	click: 'on_click',
    },

    on_click: function(event) {
	event.preventDefault();
	this.do_action(
	    'standard_plus_issue.action_standard_plus_issue_systray',
	    {clear_breadcrumbs: true}
	);
    },
});

SflSupport.prototype.sequence = 900;
SystrayMenu.Items.push(SflSupport);

});
