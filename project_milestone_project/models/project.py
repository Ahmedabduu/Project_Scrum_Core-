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


class Project(models.Model):
    _inherit = "project.project"

    milestone_ids = fields.One2many(
        "project.milestone", "project_id", string="Milestones", copy=True
    )
    use_milestones = fields.Boolean(help="Does this project use milestones?")

    milestones_required = fields.Boolean()

    @api.onchange("use_milestones")
    def _onchange_use_milestones(self):
        if not self.use_milestones and self.milestones_required:
            self.milestones_required = False
