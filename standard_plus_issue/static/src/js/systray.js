odoo.define('standard_plus_issue.systray', function (require) {
"use strict";

var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var SflSupport = Widget.extend({
    template:'standard_plus_issue.sfl_support',
});

SflSupport.prototype.sequence = 900;
SystrayMenu.Items.push(SflSupport);

});
