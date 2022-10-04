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

from .test_common import HttpTestCommon


class TestController(HttpTestCommon):
    def test_01_project_browse(self):
        self.authenticate("admin", "admin")
        response = self.url_open("/projects/" + self.project_1.key)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.url.endswith(self.get_project_url(self.project_1)), response.url
        )

    def test_02_task_browse(self):
        self.authenticate("admin", "admin")
        response = self.url_open("/tasks/" + self.task11.key)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.url.endswith(self.get_task_url(self.task11)), response.url
        )
