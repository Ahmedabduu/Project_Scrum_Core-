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

import werkzeug

from odoo import http

# from odoo.http import request


class ProjectBrowser(http.Controller):
    def get_record_url(self, model, domain, action_xml_id):
        env = http.request.env()

        records = env[model].search(domain)
        record_id = records and records.id or -1
        action_id = env.ref(action_xml_id).id

        return "/web#id={}&view_type=form&model={}&action={}".format(
            record_id, model, action_id
        )

    def get_task_url(self, key):
        return self.get_record_url(
            "project.task", [("key", "=ilike", key)], "project.action_view_task"
        )

    def get_project_url(self, key):
        return self.get_record_url(
            "project.project",
            [("key", "=ilike", key)],
            "project.open_view_project_all_config",
        )

    @http.route(["/projects/<string:key>"], type="http", auth="user")
    def open_project(self, key, **kwargs):
        return werkzeug.utils.redirect(self.get_project_url(key), 301)

    @http.route(["/tasks/<string:key>"], type="http", auth="user")
    def open_task(self, key, **kwargs):
        return werkzeug.utils.redirect(self.get_task_url(key), 301)
