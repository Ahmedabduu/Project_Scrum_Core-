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


class ProjectRecalculateWizard(models.TransientModel):
    _name = "project.recalculate.wizard"
    _description = "Project recalculate wizard"

    project_id = fields.Many2one(
        comodel_name="project.project", readonly=True, string="Project"
    )
    calculation_type = fields.Selection(
        string="Calculation type", related="project_id.calculation_type", readonly=True
    )
    project_date = fields.Date(readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super(ProjectRecalculateWizard, self).default_get(fields_list)
        res["project_id"] = self.env.context.get("active_id", False)
        project = self.env["project.project"].browse(res["project_id"])
        res["project_date"] = (
            project.date_start
            if project.calculation_type == "date_begin"
            else project.date
        )
        return res

    def confirm_button(self):
        return self.project_id.project_recalculate()
