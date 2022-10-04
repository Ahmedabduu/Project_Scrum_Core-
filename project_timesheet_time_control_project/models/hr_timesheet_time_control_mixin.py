# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022-today PureNova Ltd.@AhmedAbdu
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrTimesheetTimeControlMixin(models.AbstractModel):
    _name = "hr.timesheet.time_control.mixin"
    _description = "Mixin for records related with timesheet lines"

    show_time_control = fields.Selection(
        selection=[("start", "Start"), ("stop", "Stop")],
        compute="_compute_show_time_control",
        help="Indicate which time control button to show, if any.",
    )

    @api.model
    def _relation_with_timesheet_line(self):
        """Name of the field that relates this model with AAL."""
        raise NotImplementedError

    @api.model
    def _timesheet_running_domain(self):
        """Domain to find running timesheet lines."""
        return self.env["account.analytic.line"]._running_domain() + [
            (self._relation_with_timesheet_line(), "in", self.ids),
        ]

    def _compute_show_time_control(self):
        """Decide which time control button to show, if any."""
        related_field = self._relation_with_timesheet_line()
        grouped = self.env["account.analytic.line"].read_group(
            domain=self._timesheet_running_domain(),
            fields=["id"],
            groupby=[related_field],
        )
        lines_per_record = {
            group[related_field][0]: group["%s_count" % related_field]
            for group in grouped
        }
        button_per_lines = {0: "start", 1: "stop"}
        for record in self:
            record.show_time_control = button_per_lines.get(
                lines_per_record.get(record.id, 0),
                False,
            )

    def button_start_work(self):
        """Create a new record starting now, with a running timer."""
        related_field = self._relation_with_timesheet_line()
        return {
            "context": {"default_%s" % related_field: self.id},
            "name": _("Start work"),
            "res_model": "hr.timesheet.switch",
            "target": "new",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
        }

    def button_end_work(self):
        running_lines = self.env["account.analytic.line"].search(
            self._timesheet_running_domain(),
        )
        if not running_lines:
            model = self.env["ir.model"].search([("model", "=", self._name)])
            message = _(
                "No running timer found in %(model)s %(record)s. "
                "Refresh the page and check again."
            )
            raise UserError(
                message % {"model": model.name, "record": self.display_name}
            )
        return running_lines.button_end_work()
