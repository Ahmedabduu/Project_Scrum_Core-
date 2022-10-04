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

from odoo import _, api, exceptions, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    pr_uri = fields.Char(string="PR URI", tracking=True)

    pr_required_states = fields.Many2many(related="project_id.pr_required_states")

    @api.constrains("pr_uri", "stage_id", "project_id")
    def _check_pr_uri_required(self):
        for task in self:
            stages_pr_req = task.project_id.pr_required_states
            is_stage_pr_req = task.stage_id in stages_pr_req
            if not task.pr_uri and stages_pr_req and is_stage_pr_req:
                raise exceptions.ValidationError(
                    _(
                        "Please add the URI for the pull request "
                        "before moving the task to this stage."
                    )
                )
