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

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProjectTaskDependency(TransactionCase):
    def setUp(self):
        super().setUp()

        self.project1 = self.env["project.project"].create(
            {"name": "Nice Project Test Dependencies One"}
        )
        self.project2 = self.env["project.project"].create(
            {"name": "Nice Project Test Dependencies Two"}
        )
        self.task1 = self.env["project.task"].create(
            {"name": "1", "project_id": self.project1.id}
        )
        self.task2 = self.env["project.task"].create(
            {
                "name": "2",
                "dependency_task_ids": [(6, 0, [self.task1.id])],
                "project_id": self.project1.id,
            }
        )
        self.task3 = self.env["project.task"].create(
            {
                "name": "3",
                "dependency_task_ids": [(6, 0, [self.task2.id])],
                "project_id": self.project1.id,
            }
        )
        self.task4 = self.env["project.task"].create(
            {
                "name": "4",
                "dependency_task_ids": [(6, 0, [self.task2.id])],
                "project_id": self.project2.id,
            }
        )

    def test_01_dependency_path(self):
        self.assertEqual(len(self.task3.dependency_task_ids), 1)

        self.assertEqual(len(self.task1.recursive_dependency_task_ids), 0)
        self.assertEqual(len(self.task3.recursive_dependency_task_ids), 2)

        self.assertEqual(len(self.task3.depending_task_ids), 0)
        self.assertEqual(len(self.task1.depending_task_ids), 1)

        self.assertEqual(len(self.task3.recursive_depending_task_ids), 0)
        self.assertEqual(len(self.task1.recursive_depending_task_ids), 3)

    def test_02_avoid_recursion(self):
        with self.assertRaises(ValidationError):
            self.task1.write({"dependency_task_ids": [(6, 0, [self.task3.id])]})

    def test_copy(self):
        new_project = self.project1.copy(
            {"name": "Nice Project Test Dependencies One Second"}
        )
        task2 = new_project.tasks.filtered(lambda t: t.name == "2")
        self.assertEqual(task2.dependency_task_ids[0].name, "1")
        task3 = new_project.tasks.filtered(lambda t: t.name == "3")
        self.assertEqual(task3.dependency_task_ids[0].name, "2")
        new_project = self.project2.copy(
            {"name": "Nice Project Test Dependencies Two Second"}
        )
        task4 = new_project.tasks.filtered(lambda t: t.name == "4")
        self.assertEqual(task4.dependency_task_ids[0].id, self.task2.id)

    def test_regression_copy(self):
        old_count = self.env["project.task.copy.map"].search_count(
            [("old_task_id", "=", self.task4.id)]
        )
        self.task4.copy()
        new_count = self.env["project.task.copy.map"].search_count(
            [("old_task_id", "=", self.task4.id)]
        )
        self.assertEqual(old_count, new_count)

    def test_open_task_button(self):
        res = self.task4.dependency_task_ids[0].button_open_task()
        self.assertEqual(res["res_id"], self.task4.dependency_task_ids[0].id)

    def test_open_blocking_tasks_button(self):
        res = self.task4.button_open_blocking_tasks()
        self.assertEqual(
            res["domain"], [("id", "in", self.task4.depending_task_ids.ids)]
        )
