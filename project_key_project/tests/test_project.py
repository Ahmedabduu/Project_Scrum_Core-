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

from odoo.tools import mute_logger

from .test_common import TestCommon


class TestProject(TestCommon):
    def test_01_key(self):
        self.assertEqual(self.project_1.key, "OCA")
        self.assertEqual(self.project_2.key, "ODOO")
        self.assertEqual(self.project_3.key, "PYT")

    def test_02_change_key(self):
        self.project_1.key = "XXX"

        self.assertEqual(self.task11.key, "XXX-1")
        self.assertEqual(self.task12.key, "XXX-2")

    def test_03_name_search(self):

        projects = self.Project.name_search("ODO")
        self.assertEqual(len(projects), 1)

        non_odoo_projects = [
            x[0] for x in self.Project.name_search("ODO", operator="not ilike")
        ]

        odoo_projects = self.Project.browse(non_odoo_projects).filtered(
            lambda x: x.id == self.project_2.id
        )

        self.assertEqual(len(odoo_projects), 0)

    def test_04_name_search_empty(self):
        projects = self.Project.name_search("")
        self.assertGreater(len(projects), 0)

    def test_05_name_onchange(self):
        project = self.Project.new({"name": "Software Development"})
        project._onchange_project_name()
        self.assertEqual(project.key, "SD")

    def test_06_name_onchange(self):
        project = self.Project.new({})
        project._onchange_project_name()
        self.assertEqual(project.key, "")

    @mute_logger("odoo.models.unlink")
    def test_07_delete(self):
        self.project_1.task_ids.unlink()
        self.project_1.unlink()

        self.project_2.task_ids.unlink()
        self.project_2.unlink()

        self.project_3.unlink()

    def test_08_generate_empty_project_key(self):
        empty_key = self.Project.generate_project_key(False)
        self.assertEqual(empty_key, "")

    def test_09_name_onchange_with_key(self):
        project = self.Project.new({"name": "Software Development", "key": "TEST"})
        project._onchange_project_name()
        self.assertEqual(project.key, "TEST")

    def test_10_generate_unique_key_with_counter(self):
        project = self.Project.create({"name": "OCA"})
        self.assertEqual(project.key, "OCA1")
