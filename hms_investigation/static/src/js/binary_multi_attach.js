odoo.define('hms_investigation.multi_attach', function(require){
"use strict";
var core = require('web.core');
var FormView = require('web.FormView');

var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;

FormView.include({
	events: {
        'click .multi_seq_binary': 'add_multiple_attr',
		'change .multi_seq_binary': 'onchange_binary_field',
	},
    add_multiple_attr: function(event){
        var $target = $(event.target);
        $target.attr("multiple", "")
    },
	onchange_binary_field: function(event){
		var $target = $(event.target);
		_.each($target[0].files, function(file){
			var querydata = new FormData();
            querydata.append('ufile', file);
            querydata.append('multi_seq', $('.multi_seq input').val());
            $.ajax({
                url: '/hms/multi_attach',
                type: 'POST',
                data: querydata,
                contentType: "application/json; charset=utf-8",
                cache: false,
                processData: false,  
                contentType: false,
                success: function(id){
                },
            });
		});
	},
});
})