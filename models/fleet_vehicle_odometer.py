# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class FleetVehicleOdometer(models.Model):
    _inherit = "fleet.vehicle.odometer"

    company_id = fields.Many2one('res.company', 'Company', compute='_compute_get_company_id')

    # get the company_id from the vehicle
    @api.depends('vehicle_id')
    def _compute_get_company_id(self):
        for record in self:
            record.company_id = record.vehicle_id.company_id
