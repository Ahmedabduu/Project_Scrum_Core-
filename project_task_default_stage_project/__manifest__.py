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
    "name": "Project Task Default Stage  Manage",
    "summary": "Recovery default task stages for projects",
    "version": "14.0.1.1.0",
    "category": "Project",
    "author": "Ahmed Abdu",
    "license": "AGPL-3",
    "depends": ["project"],
    "data": ["views/project_view.xml", "data/project_data.xml"],
    "installable": True,
}
