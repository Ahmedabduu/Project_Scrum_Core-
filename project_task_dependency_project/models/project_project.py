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

from odoo import models


class ProjectProject(models.Model):
    _inherit = "project.project"

    def copy(self, default=None):
        self.ensure_one()
        res = super(ProjectProject, self.with_context(project_copy=True)).copy(default)

        mappings = self.env["project.task.copy.map"].search(
            [("new_task_id.project_id", "=", res.id)]
        )
        for task in res.tasks:
            mapping = mappings.filtered(lambda t: t.new_task_id.id == task.id)
            new_dependencies = []
            for dep in mapping.old_task_id.dependency_task_ids:
                dep_mapping = mappings.filtered(lambda t: t.old_task_id.id == dep.id)
                new_dependencies.append(
                    dep_mapping and dep_mapping.new_task_id.id or dep.id
                )
            task.write({"dependency_task_ids": [(6, 0, new_dependencies)]})
        return res
