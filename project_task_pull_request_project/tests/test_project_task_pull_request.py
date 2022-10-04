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


class TestProjectTaskPullRequest(TransactionCase):
    post_install = True
    at_install = False

    def setUp(self):
        super(TestProjectTaskPullRequest, self).setUp()

        project_obj = self.env["project.project"]
        task_obj = self.env["project.task"]
        self.new_stage = self.ref("project.project_stage_0")
        self.inprogress_stage = self.ref("project.project_stage_1")
        self.done_stage = self.ref("project.project_stage_2")
        self.cancel_stage = self.ref("project.project_stage_3")

        self.project_1 = project_obj.create(
            {"name": "Test Project 1", "pr_required_states": [(4, self.done_stage)]}
        )
        self.project_2 = project_obj.create(
            {
                "name": "Test Project 2",
                "pr_required_states": [
                    (4, self.done_stage),
                    (4, self.inprogress_stage),
                ],
            }
        )

        self.task_1 = task_obj.create(
            {
                "name": "Test Task 1",
                "project_id": self.project_1.id,
                "pr_uri": False,
                "stage_id": self.new_stage,
            }
        )
        self.task_2 = task_obj.create(
            {
                "name": "Test Task 2",
                "project_id": self.project_2.id,
                "pr_uri": False,
                "stage_id": self.new_stage,
            }
        )
        self.task_3 = task_obj.create(
            {
                "name": "Test Task 3",
                "project_id": self.project_2.id,
                "pr_uri": "github.com",
                "stage_id": self.new_stage,
            }
        )

    def test_write_allowed_when_allowed(self):
        self.task_1.write({"stage_id": self.inprogress_stage})
        self.task_1.refresh()
        self.assertEquals(self.inprogress_stage, self.task_1.stage_id.id)

    def test_write_not_allowed_without_pr(self):
        with self.assertRaises(ValidationError):
            self.task_1.write({"stage_id": self.done_stage})

    def test_write_not_allowed_without_pr_multiple_stages(self):
        with self.assertRaises(ValidationError):
            self.task_2.write({"stage_id": self.inprogress_stage})

    def test_write_allowed_with_pr(self):
        self.task_3.write({"stage_id": self.done_stage})
        self.task_3.refresh()
        self.assertEquals(self.done_stage, self.task_3.stage_id.id)
