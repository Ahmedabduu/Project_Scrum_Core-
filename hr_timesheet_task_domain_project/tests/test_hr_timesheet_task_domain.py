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


class TestHrTimesheetTaskDomain(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.project = self.env["project.project"].create({"name": "Test project"})
        self.analytic_account = self.project.analytic_account_id
        self.task = self.env["project.task"].create(
            {"name": "Test task", "project_id": self.project.id}
        )
        self.line = self.env["account.analytic.line"].create(
            {
                "task_id": self.task.id,
                "account_id": self.analytic_account.id,
                "name": "Test line",
            }
        )

    def test_onchange_project_id(self):
        record = self.env["account.analytic.line"].new()
        record.task_id = self.task.id
        record.project_id = self.project.id
        action = record._onchange_project_id()
        self.assertTrue(action["domain"]["task_id"])
        self.assertEqual(record.task_id, self.task)
        record.project_id = False
        action = record._onchange_project_id()
        self.assertEqual(action["domain"]["task_id"], [])
