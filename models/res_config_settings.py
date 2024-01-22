# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    vidange_km_alert = fields.Integer(string='Kélometrage alerte avant le vidange', default=2000, config_parameter='anem_fleet.vidange_km_alert')
    controle_date_alert = fields.Integer(string='controle technique alerte avant l''expriration', default=7, config_parameter='anem_fleet.controle_date_alert')

    vidange_tag_id = fields.Many2one('fleet.vehicle.tag', string='Étiquette vidange', config_parameter='anem_fleet.vidange_tag_id')
    controle_tag_id = fields.Many2one('fleet.vehicle.tag', string='Étiquette Controle technique', config_parameter='anem_fleet.controle_tag_id')
