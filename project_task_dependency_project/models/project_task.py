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
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    dependency_task_ids = fields.Many2many(
        string="Dependencies",
        comodel_name="project.task",
        relation="project_task_dependency_task_rel",
        column1="task_id",
        column2="dependency_task_id",
    )

    recursive_dependency_task_ids = fields.Many2many(
        string="Recursive Dependencies",
        comodel_name="project.task",
        compute="_compute_recursive_dependency_task_ids",
    )

    depending_task_ids = fields.Many2many(
        string="Depending Tasks",
        comodel_name="project.task",
        help="Tasks that are dependent on this task.",
        compute="_compute_depending_task_ids",
    )

    recursive_depending_task_ids = fields.Many2many(
        string="Recursive Depending Tasks",
        comodel_name="project.task",
        help="Tasks that are dependent on this task (recursive).",
        compute="_compute_recursive_depending_task_ids",
    )

    dependent_tasks_count = fields.Integer(
        string="Dependent Tasks", compute="_compute_dependent_tasks_count"
    )

    @api.depends("dependency_task_ids")
    def _compute_dependent_tasks_count(self):
        for task in self:
            task.dependent_tasks_count = len(task.depending_task_ids)

    @api.depends("dependency_task_ids")
    def _compute_recursive_dependency_task_ids(self):
        for task in self:
            task.recursive_dependency_task_ids = task.get_dependency_tasks()

    @api.depends("dependency_task_ids")
    def _compute_depending_task_ids(self):
        for task in self:
            task.depending_task_ids = task.get_depending_tasks(task)

    @api.depends("dependency_task_ids")
    def _compute_recursive_depending_task_ids(self):
        for task in self:
            task.recursive_depending_task_ids = task.get_depending_tasks(task, True)

    def get_dependency_tasks(self):
        self.ensure_one()
        dependency_tasks = self.dependency_task_ids
        tasks_stack = dependency_tasks
        processed_tasks = self.env["project.task"]
        while tasks_stack:
            actual_task = fields.first(tasks_stack)
            processed_tasks |= actual_task
            dependency_tasks |= actual_task.dependency_task_ids
            tasks_stack = dependency_tasks - processed_tasks
        return dependency_tasks

    @api.model
    def get_depending_tasks(self, task, recursive=False):
        if not isinstance(task.id, models.NewId):
            depending_tasks = self.search([("dependency_task_ids", "in", task.id)])
            if recursive:
                for t in depending_tasks:
                    depending_tasks += self.get_depending_tasks(t, recursive)
            return depending_tasks

    @api.constrains("dependency_task_ids")
    def _check_dependency_recursion(self):
        if not self._check_m2m_recursion("dependency_task_ids"):
            raise ValidationError(
                _("You cannot create recursive dependencies between tasks.")
            )

    def copy(self, default=None):
        res = super().copy(default)
        if self.env.context.get("project_copy"):
            self.env["project.task.copy.map"].create(
                {"old_task_id": self.id, "new_task_id": res.id}
            )
        return res

    def button_open_task(self):
        action = {
            "name": _("Task"),
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "res_id": self.id,
            "view_mode": "form",
            "view_type": "form",
        }
        return action

    def button_open_blocking_tasks(self):
        action = {
            "name": _("Task"),
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "kanban,form,list",
            "view_type": "form",
            "domain": [("id", "in", self.depending_task_ids.ids)],
        }
        return action
