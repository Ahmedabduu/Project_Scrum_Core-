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

from odoo import api, fields, models


class ProjectMilestone(models.Model):
    _name = "project.milestone"
    _order = "project_id,sequence"
    _description = "Project Milestone"

    name = fields.Char(string="Milestone", required=True)
    target_date = fields.Date(help="The date when the Milestone should be complete.")
    progress = fields.Float(
        compute="_compute_milestone_progress",
        store=True,
        help="Percentage of Completed Tasks vs Incomplete Tasks.",
    )
    project_id = fields.Many2one("project.project", string="Project", index=True)
    project_task_ids = fields.One2many(
        "project.task", "milestone_id", string="Project Tasks"
    )
    fold = fields.Boolean(string="Kanban Folded?")
    sequence = fields.Integer()

    @api.model
    def create(self, vals):
        seq = self.env["ir.sequence"].next_by_code("project.milestone") or 0
        vals["sequence"] = seq
        return super().create(vals)

    @api.depends("project_task_ids.stage_id", "project_task_ids.stage_id.is_closed")
    def _compute_milestone_progress(self):
        for record in self:
            total_tasks_count = 0.0
            closed_tasks_count = 0.0
            for task_record in record.project_task_ids:
                total_tasks_count += 1
                if task_record.stage_id.is_closed:
                    closed_tasks_count += 1
            if total_tasks_count > 0:
                record.progress = (closed_tasks_count / total_tasks_count) * 100
            else:
                record.progress = 0.0
