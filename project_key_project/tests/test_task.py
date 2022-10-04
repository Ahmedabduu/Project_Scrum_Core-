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

from .test_common import TestCommon


class TestTask(TestCommon):
    def test_01_key(self):
        self.assertEqual(self.task11.key, "OCA-1")
        self.assertEqual(self.task12.key, "OCA-2")
        self.assertEqual(self.task21.key, "ODOO-1")
        self.assertEqual(self.task30.key, False)

    def test_02_compute_task_url(self):
        task_url = self.get_task_url(self.task11)

        self.task11._compute_task_url()
        self.assertEqual(self.task11.url, task_url)

    def test_03_create_task_project_in_context(self):
        self.Task.with_context(
            active_model="project.project", active_id=self.project_1.id
        ).create({"name": "4"})

    def test_04_no_switch_project(self):
        self.task11.write({"project_id": self.project_1.id})
        self.assertEqual(self.task11.key, "OCA-1")
        self.assertEqual(self.task12.key, "OCA-2")

    def test_05_switch_project(self):
        self.task11.write({"project_id": self.project_2.id})
        self.assertEqual(self.task11.key, "ODOO-2")
        self.assertEqual(self.task12.key, "ODOO-3")

    def test_06_name_search(self):
        oca_tasks = self.Task.name_search("OCA")
        self.assertEqual(len(oca_tasks), 2)

        non_oca_task_ids = [
            x[0] for x in self.Task.name_search("OCA", operator="not ilike")
        ]

        oca_tasks = self.Task.browse(non_oca_task_ids).filtered(
            lambda x: x.project_id.id == self.project_1.id
        )

        self.assertEqual(len(oca_tasks), 0)

    def test_07_name_search_empty(self):
        tasks = self.Task.name_search("")
        self.assertGreater(len(tasks), 0)
