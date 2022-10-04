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
from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    is_task_closed = fields.Boolean(related="task_id.stage_id.is_closed")

    def action_open_task(self):
        ProjectTaskType = self.env["project.task.type"]

        for line in self.filtered("task_id.project_id"):
            stage = ProjectTaskType.search(
                [
                    ("project_ids", "=", line.task_id.project_id.id),
                    ("is_closed", "=", False),
                ],
                limit=1,
            )
            if not stage:  # pragma: no cover
                raise UserError(
                    _(
                        'There isn\'t any stage with "Closed" unchecked.'
                        " Please unmark any."
                    )
                )
            line.task_id.write({"stage_id": stage.id})

    def action_close_task(self):
        ProjectTaskType = self.env["project.task.type"]

        for line in self.filtered("task_id.project_id"):
            stage = ProjectTaskType.search(
                [
                    ("project_ids", "=", line.task_id.project_id.id),
                    ("is_closed", "=", True),
                ],
                limit=1,
            )
            if not stage:  # pragma: no cover
                raise UserError(
                    _(
                        'There isn\'t any stage with "Closed" checked. Please'
                        " mark any."
                    )
                )
            line.task_id.write({"stage_id": stage.id})

    def action_toggle_task_stage(self):
        for line in self.filtered("task_id.project_id"):
            if line.is_task_closed:
                line.action_open_task()
            else:
                line.action_close_task()
