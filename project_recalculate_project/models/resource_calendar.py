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

from datetime import datetime, timedelta
from functools import partial

from odoo import models

from odoo.addons.resource.models.resource import make_aware


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    def get_working_days_of_date(self, start_dt=None, end_dt=None, resource=None):
        self.ensure_one()
        if start_dt is None:
            start_dt = datetime.now().replace(hour=0, minute=0, second=0)
        if end_dt is None:
            end_dt = datetime.now().replace(hour=23, minute=59, second=59)
        days = 0
        current = start_dt
        while current <= end_dt:
            end_day = current.replace(hour=23, minute=59, second=59)
            end = end_dt if end_day > end_dt else end_day
            obj = self.with_context(tz="UTC")
            working_intervals = obj._work_intervals(current, end, resource)
            if len(working_intervals):
                days += 1
            current += timedelta(days=1)
        return days

    def plan_days_to_resource(
        self, days, day_dt, compute_leaves=False, resource=None, domain=None
    ):
        day_dt, revert = make_aware(day_dt)

        # which method to use for retrieving intervals
        if compute_leaves:
            get_intervals = partial(
                self._work_intervals, resource=resource, domain=domain
            )
        else:
            get_intervals = partial(self._attendance_intervals, resource=resource)

        if days > 0:
            found = set()
            delta = timedelta(days=14)
            for n in range(100):
                dt = day_dt + delta * n
                for start, stop, meta in get_intervals(dt, dt + delta):  # noqa: B007
                    found.add(start.date())
                    if len(found) == days:
                        return revert(stop)
            return False

        elif days < 0:
            days = abs(days)
            found = set()
            delta = timedelta(days=14)
            for n in range(100):
                dt = day_dt - delta * n
                for start, stop, meta in reversed(  # noqa: B007
                    get_intervals(dt - delta, dt)
                ):
                    found.add(stop.date())
                    if len(found) == days:
                        return revert(start)
            return False

        else:
            return revert(day_dt)
