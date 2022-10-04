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

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import html_translate


class ProjectRole(models.Model):
    _name = "project.role"
    _description = "Project Role"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "complete_name"

    active = fields.Boolean(
        default=True,
    )
    parent_path = fields.Char(
        index=True,
    )
    parent_id = fields.Many2one(
        string="Parent Role",
        comodel_name="project.role",
        index=True,
        ondelete="cascade",
    )
    child_ids = fields.One2many(
        string="Child Roles",
        comodel_name="project.role",
        inverse_name="parent_id",
        copy=True,
    )
    complete_name = fields.Char(
        string="Complete Name",
        compute="_compute_complete_name",
        store=True,
    )
    name = fields.Char(
        string="Name",
        translate=True,
        required=True,
    )
    description = fields.Html(
        string="Description",
        translate=html_translate,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
        ondelete="cascade",
    )

    _sql_constraints = [
        (
            "name_company_uniq",
            "UNIQUE (name, company_id)",
            "Role with such name already exists in the company!",
        ),
        (
            "name_nocompany_uniq",
            ("EXCLUDE (name WITH =) WHERE (" "    company_id IS NULL" ")"),
            "Shared role with such name already exists!",
        ),
    ]

    @api.constrains("name")
    def _check_name(self):
        for role in self:
            if self.search(
                [
                    ("company_id", "=" if role.company_id else "!=", False),
                    ("name", "=", role.name),
                ],
                limit=1,
            ):
                raise ValidationError(
                    _('Role "%s" conflicts with another role due to same name.')
                    % (role.name,)
                )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for role in self:
            if role.parent_id:
                role.complete_name = _("%(parent)s / %(own)s") % {
                    "parent": role.parent_id.complete_name,
                    "own": role.name,
                }
            else:
                role.complete_name = role.name

    @api.constrains("active")
    def _check_active(self):
        for role in self:
            if (
                role.active
                and role.parent_id
                and role.parent_id not in self
                and not role.parent_id.active
            ):
                raise ValidationError(
                    _(
                        "Please activate first parent role %s"
                        % (role.parent_id.complete_name,)
                    )
                )

    def can_assign(self, user_id, project_id):
        """Extension point to check if user can be assigned to this role"""
        self.ensure_one()
        return self.active

    @api.model
    def get_available_roles(self, user_id, project_id):
        """
        Get domain on roles that can be assumed by given user on a specific
        project, depending on company and project assignments configuration.
        """
        if not user_id or not project_id:
            return self

        if not project_id.limit_role_to_assignments:
            if project_id.inherit_assignments:
                domain = [("company_id", "in", [False, user_id.company_id.id])]
            else:
                domain = [("company_id", "=", user_id.company_id.id)]
            return self.search(domain)

        domain = [("user_id", "=", user_id.id)]
        if project_id.inherit_assignments:
            domain += [
                ("project_id", "in", [False, project_id.id]),
                ("company_id", "in", [False, user_id.company_id.id]),
            ]
        else:
            domain += [
                ("project_id", "=", project_id.id),
                ("company_id", "=", user_id.company_id.id),
            ]
        return self.env["project.assignment"].search(domain).mapped("role_id")
