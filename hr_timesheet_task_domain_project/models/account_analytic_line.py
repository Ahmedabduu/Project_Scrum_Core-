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

from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.onchange("project_id")
    def _onchange_project_id(self):
        task = self.task_id
        res = super()._onchange_project_id()
        if res is None:
            res = {}
        if self.project_id:  # Show only opened tasks
            task_domain = [
                ("project_id", "=", self.project_id.id),
                ("stage_id.is_closed", "=", False),
            ]
            res_domain = res.setdefault("domain", {})
            res_domain.update({"task_id": task_domain})
        else:  # Reset domain for allowing selection of any task
            res["domain"] = {"task_id": []}
        if task.project_id == self.project_id:
            # Restore previous task if belongs to the same project
            self.task_id = task
        return res
