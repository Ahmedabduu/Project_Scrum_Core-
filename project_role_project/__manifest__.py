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
    "name": "Project Roles  Manage",
    "version": "14.0.1.0.0",
    "category": "Project",
    "author": "Ahmed Abdu",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "summary": "Project role-based roster",
    "depends": ["project", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/project_role.xml",
        "views/project_assignment.xml",
        "views/project_project.xml",
        "views/project_role.xml",
        "views/res_config_settings.xml",
    ],
    "maintainers": ["PureNova"],
}
