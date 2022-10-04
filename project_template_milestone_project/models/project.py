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

from odoo import models


class ProjectTemplate(models.Model):
    _inherit = "project.project"

    def create_project_from_template(self):
        res = super().create_project_from_template()
        project = self.env["project.project"].browse(res["res_id"])
        # LINK THE NEWLY CREATED TASKS TO THE NEWLY CREATED MILESTONES
        for new_task_record in project.task_ids:
            for new_milestone_record in project.milestone_ids:
                if new_task_record.milestone_id.name == new_milestone_record.name:
                    new_task_record.milestone_id = new_milestone_record.id
        return res
