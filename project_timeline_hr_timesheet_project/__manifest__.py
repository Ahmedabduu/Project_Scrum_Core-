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

{
    "name": "Project Timeline - Timesheet  Manage",
    "summary": "Shows the progress of tasks on the timeline view.",
    "license": "AGPL-3",
    "category": "Project Management",
    "version": "14.0.1.0.0",
    "depends": ["project_timeline_project_project", "hr_timesheet"],
    "data": ["templates/assets.xml", "views/project_task_view.xml"],
    "installable": True,
    "auto_install": True,
}
