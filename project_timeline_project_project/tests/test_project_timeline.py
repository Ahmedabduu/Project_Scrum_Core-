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

from odoo import fields
from odoo.tests.common import TransactionCase


class TestProjectTimeline(TransactionCase):
    def test_date_end_doesnt_unset(self):
        stage_id = self.ref("project.project_stage_2")
        task = self.env["project.task"].create(
            {
                "name": "1",
                "date_assign": "2018-05-01 00:00:00",
                "date_end": "2018-05-07 00:00:00",
            }
        )
        task.write({"stage_id": stage_id, "date_end": "2018-10-07 00:00:00"})
        self.assertEqual(
            task.date_end, fields.Datetime.from_string("2018-10-07 00:00:00")
        )
