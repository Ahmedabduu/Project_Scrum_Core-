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

from odoo import api, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "hr.timesheet.time_control.mixin"]

    @api.model
    def _relation_with_timesheet_line(self):
        return "project_id"

    @api.depends("allow_timesheets")
    def _compute_show_time_control(self):
        result = super()._compute_show_time_control()
        for project in self:
            # Never show button if timesheets are not allowed in project
            if not project.allow_timesheets:
                project.show_time_control = False
        return result

    def button_start_work(self):
        result = super().button_start_work()
        # When triggering from project is usually to start timer without task
        result["context"].update({"default_task_id": False})
        return result
