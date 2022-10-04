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


def populate_date_start(cr, registry):
    """
    The date_start was introduced to be used instead of date_assign.
    To keep same behaviour on upgrade, initialize it
    to have the same data as before.
    """
    cr.execute(
        "UPDATE project_task "
        "SET date_start = date_assign "
        "WHERE date_start IS NULL "
        "AND date_assign IS NOT NULL"
    )
