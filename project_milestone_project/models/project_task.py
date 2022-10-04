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


class ProjectTask(models.Model):
    _inherit = "project.task"

    milestone_id = fields.Many2one(
        "project.milestone",
        string="Milestone",
        group_expand="_read_group_milestone_ids",
        domain="[('project_id', '=', project_id)]",
    )
    use_milestones = fields.Boolean(
        related="project_id.use_milestones", help="Does this project use milestones?"
    )
    milestones_required = fields.Boolean(
        related="project_id.milestones_required",
    )

    @api.model
    def _read_group_milestone_ids(self, milestone_ids, domain, order):
        if "default_project_id" in self.env.context:
            milestone_ids = self.env["project.milestone"].search(
                [("project_id", "=", self.env.context["default_project_id"])]
            )
        return milestone_ids

    @api.model
    def create(self, vals):
        if self.env.context.get("default_parent_id", False):
            parent_task = self.browse(self.env.context.get("default_parent_id"))

            if parent_task.milestone_id:
                vals.update(
                    {
                        "milestone_id": parent_task.milestone_id.id,
                    }
                )
        res = super(ProjectTask, self).create(vals)

        return res

    @api.onchange("parent_id")
    def _onchange_parent_id_milestone(self):
        if self.parent_id and self.parent_id.milestone_id:
            self.milestone_id = self.parent_id.milestone_id.id
        else:
            self.milestone_id = False
