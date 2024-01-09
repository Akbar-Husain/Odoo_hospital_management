odoo.define('shah_opd.shah_list_view', function (require) {
"use strict";

var core = require('web.core');
var data = require('web.data');
var FormView = require('web.FormView');
var common = require('web.list_common');
var ListView = require('web.ListView');
var utils = require('web.utils');
var Widget = require('web.Widget');

var _t = core._t;


ListView.List.include({
    init: function (group, opts) {
        var self = this;
        this.group = group;
        this._super.apply(this, arguments);
        
        this.$current = $('<tbody>')
            .delegate('input[readonly=readonly]', 'click', function (e) {
                e.preventDefault();
            })
            .delegate('th.oe_list_record_selector', 'click', function (e) {
                e.stopPropagation();
                var selection = self.get_selection();
                var checked = $(e.currentTarget).find('input').prop('checked');
                $(self).trigger(
                        'selected', [selection.ids, selection.records, ! checked]);
            })
            .delegate('td.oe_list_record_delete', 'click', function (e) {
                e.stopPropagation();
                var $row = $(e.target).closest('tr');
                $(self).trigger('deleted', [[self.row_id($row)]]);
                // IE Edge go crazy when we use confirm dialog and remove the focused element
                if(document.hasFocus && !document.hasFocus()) {
                    $('<input />').appendTo('body').focus().remove();
                }
            })
            .delegate('td.oe_list_field_cell button', 'click', function (e) {
                e.stopPropagation();
                var $target = $(e.currentTarget),
                      field = $target.closest('td').data('field'),
                       $row = $target.closest('tr'),
                  record_id = self.row_id($row);
                
                if ($target.attr('disabled')) {
                    return;
                }
                if (!(field == 'action_open_preview')){
                    $target.attr('disabled', 'disabled');
                }

                $(self).trigger('action', [field.toString(), record_id, function (id) {
                    $target.removeAttr('disabled');
                    return self.reload_record(self.records.get(id));
                }]);
            })
            .delegate('a', 'click', function (e) {
                e.stopPropagation();
            })
            .delegate('tr', 'click', function (e) {
                var row_id = self.row_id(e.currentTarget);
                if (row_id) {
                    e.stopPropagation();
                    if (!self.dataset.select_id(row_id)) {
                        throw new Error(_t("Could not find id in dataset"));
                    }
                    self.row_clicked(e);
                }
            });

    },

});
});


