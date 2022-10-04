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

from .common import TestProjectCases


class ProjectTaskMaterial(TestProjectCases):
    def test_manager_add_task_material_wrong(self):
        """
        TEST CASE 1
        The user is adding some materials in the task
        with different wrong values

        """
        try:
            # Material with `quantity = 0.0`
            self.action.write(
                {
                    "material_ids": [
                        (0, 0, {"product_id": self.product.id, "quantity": 0.0})
                    ]
                }
            )
        except ValidationError as err:
            self.assertEqual(
                str(err.args[0]),
                "Quantity of material consumed must be greater than 0.",
            )

        try:
            # Material with `negative quantity`
            self.action.write(
                {
                    "material_ids": [
                        (0, 0, {"product_id": self.product.id, "quantity": -10.0})
                    ]
                }
            )
        except ValidationError as err:
            self.assertEqual(
                str(err.args[0]),
                "Quantity of material consumed must be greater than 0.",
            )

    def test_manager_add_task_material_right(self):
        """
        TEST CASE 2
        The user is adding some materials in the task
        with right values

        """
        # Material with `quantity = 1.0`
        self.action.write(
            {"material_ids": [(0, 0, {"product_id": self.product.id, "quantity": 4.0})]}
        )
        self.assertEqual(len(self.task.material_ids.ids), 1)
