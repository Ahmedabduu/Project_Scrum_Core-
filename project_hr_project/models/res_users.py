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

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    hr_category_ids = fields.Many2many(
        comodel_name="hr.employee.category",
        string="HR categories",
        compute="_compute_hr_category_ids",
        help="Technical field for computing dynamically employee categories "
        "linked to the user in the current company.",
    )

    @api.depends("company_id", "employee_ids", "employee_ids.category_ids")
    def _compute_hr_category_ids(self):
        for user in self:
            user.hr_category_ids = user.employee_ids.filtered(
                lambda x: x.company_id == user.company_id
            )[:1].category_ids
