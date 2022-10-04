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

from odoo.tests import common


class TestHrTimesheetTaskStage(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.project = self.env["project.project"].create({"name": "Test project"})
        self.analytic_account = self.project.analytic_account_id
        self.task = self.env["project.task"].create(
            {"name": "Test task", "project_id": self.project.id}
        )
        task_type_obj = self.env["project.task.type"]
        self.stage_open = task_type_obj.create(
            {
                "name": "New",
                "is_closed": False,
                "project_ids": [(6, 0, self.project.ids)],
            }
        )
        self.stage_close = task_type_obj.create(
            {
                "name": "Done",
                "is_closed": True,
                "project_ids": [(6, 0, self.project.ids)],
            }
        )
        self.line = self.env["account.analytic.line"].create(
            {
                "task_id": self.task.id,
                "account_id": self.analytic_account.id,
                "name": "Test line",
            }
        )

    def test_open_close_task(self):
        self.line.action_close_task()
        self.assertEqual(self.line.task_id.stage_id, self.stage_close)
        self.line.action_open_task()
        self.assertEqual(self.line.task_id.stage_id, self.stage_open)

    def test_toggle_task_stage(self):
        self.line.action_toggle_task_stage()
        self.assertTrue(self.line.task_id.stage_id.is_closed)
        self.assertTrue(self.line.is_task_closed)
        self.line.action_toggle_task_stage()
        self.assertFalse(self.line.task_id.stage_id.is_closed)
        self.assertFalse(self.line.is_task_closed)
