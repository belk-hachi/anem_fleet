# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions


class FleetVehicleOdometer(models.Model):
    _inherit = "fleet.vehicle.odometer"

    company_id = fields.Many2one('res.company', 'Company', compute='_compute_get_company_id')
    chauffeur_id = fields.Many2one('res.partner', string="Conducteur", readonly=False, store=True)
    active = fields.Boolean('Active', default=True, tracking=True)


    # get the company_id from the vehicle
    @api.depends('vehicle_id')
    def _compute_get_company_id(self):
        for record in self:
            record.company_id = record.vehicle_id.company_id

# @api.constrains('value', 'date')
# def check_odometer(self):
#     for odometer in self:
#         if odometer.date and odometer.value:
#             # Check for newer date and greater value
#             newer_record = self.search([('id', '!=', odometer.id), ('date', '>', odometer.date)], limit=1)
#             if newer_record and newer_record.value >= odometer.value:
#                 raise exceptions.ValidationError('Newer record with greater or equal odometer value exists.')
#             # Check for oldest date and lowest value
#             oldest_record = self.search([('id', '!=', odometer.id), ('date', '<', odometer.date)], limit=1,
#                                         order='date asc')
#             if oldest_record and oldest_record.value <= odometer.value:
#                 raise exceptions.ValidationError('Oldest record with lower or equal odometer value exists.')
#             # Check for value between previous and next records
#             previous_record = self.search([('id', '!=', odometer.id), ('date', '<', odometer.date)], limit=1,
#                                           order='date desc')
#             next_record = self.search([('id', '!=', odometer.id), ('date', '>', odometer.date)], limit=1,
#                                       order='date asc')
#             if previous_record and previous_record.value > odometer.value:
#                 raise exceptions.ValidationError('Odometer value should be greater than previous record.')
#             if next_record and next_record.value < odometer.value:
#                 raise exceptions.ValidationError('Odometer value should be less than next record.')
