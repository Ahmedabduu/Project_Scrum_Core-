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


class ProjectProject(models.Model):
    _inherit = "project.project"

    assignment_ids = fields.One2many(
        string="Project Assignments",
        comodel_name="project.assignment",
        inverse_name="project_id",
        tracking=True,
    )
    inherit_assignments = fields.Boolean(
        string="Inherit assignments",
        default=lambda self: self._default_inherit_assignments(),
    )
    limit_role_to_assignments = fields.Boolean(
        string="Limit role to assignments",
        default=lambda self: self._default_limit_role_to_assignments(),
    )

    @api.model
    def _default_inherit_assignments(self):
        company = self.env["res.company"].browse(
            self._context.get("company_id", self.env.user.company_id.id)
        )
        return company.project_inherit_assignments

    @api.model
    def _default_limit_role_to_assignments(self):
        company = self.env["res.company"].browse(
            self._context.get("company_id", self.env.user.company_id.id)
        )
        return company.project_limit_role_to_assignments

    @api.model
    def create(self, values):
        company = None
        if "company_id" in values:
            company = self.env["res.company"].browse(values["company_id"])

        if company and "inherit_assignments" not in values:
            values["inherit_assignments"] = company.project_inherit_assignments

        if company and "limit_role_to_assignments" not in values:
            values[
                "limit_role_to_assignments"
            ] = company.project_limit_role_to_assignments

        return super().create(values)
