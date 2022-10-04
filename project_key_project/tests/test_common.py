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

from odoo.tests.common import HttpCase, SavepointCase


class TestMixin(object):
    @staticmethod
    def _setup_records(class_or_instance):
        self = class_or_instance
        self.Project = self.env["project.project"].with_context(test_project_key=True)
        self.Task = self.env["project.task"].with_context(test_project_key=True)

        self.project_action = self.env.ref("project.open_view_project_all_config")
        self.task_action = self.env.ref("project.action_view_task")

        self.project_1 = self.Project.create({"name": "OCA"})
        self.project_2 = self.Project.create({"name": "Odoo", "key": "ODOO"})
        self.project_3 = self.Project.create({"name": "Python"})

        self.task11 = self.Task.create({"name": "1", "project_id": self.project_1.id})

        self.task12 = self.Task.create(
            {"name": "2", "parent_id": self.task11.id, "project_id": self.project_1.id}
        )

        self.task21 = self.Task.create({"name": "3", "project_id": self.project_2.id})

        self.task30 = self.Task.create({"name": "3"})

    def get_record_url(self, record, model, action):
        return "/web#id={}&view_type=form&model={}&action={}".format(
            record.id, model, action
        )

    def get_task_url(self, task):
        return self.get_record_url(task, task._name, self.task_action.id)

    def get_project_url(self, project):
        return self.get_record_url(project, project._name, self.project_action.id)


class TestCommon(SavepointCase, TestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls._setup_records(cls)


class HttpTestCommon(HttpCase, TestMixin):
    def setUp(self):
        super().setUp()
        self.env = self.env(context=dict(self.env.context, tracking_disable=True))
        self._setup_records(self)
