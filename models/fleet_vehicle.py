# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict

from odoo import _, fields, models, api, tools


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    photo = fields.Image(string="Image", max_width=600, max_height=400, help="La photo de la voiture")
    cgrise = fields.Image(string="cartegrise", max_width=640, max_height=800, help="Carte grise")
    affectation = fields.Image(string="affectation", max_width=640, max_height=800, help="Décision d'affectation")
    assurance = fields.Char('N° Police Assurance')


    fuel_count = fields.Integer(compute="_compute_count_all", string='Fuel Count')
    service_count = fields.Integer(compute="_compute_count_all", string='Services')
    odometer_count = fields.Integer(compute="_compute_count_all", string='Odometer')
    history_count = fields.Integer(compute="_compute_count_all", string="Drivers History Count")
    contract_count = fields.Integer(compute="_compute_count_all", string='Contract Count')

    def _compute_count_all(self):
        super(FleetVehicle, self)._compute_count_all()
        LogFuel = self.env['fleet.vehicle.log.fuels'].with_context(active_test=False)

        fuels_data = LogFuel.read_group([('vehicle_id', 'in', self.ids)], ['vehicle_id', 'active'],
                                        ['vehicle_id', 'active'], lazy=False)

        mapped_fuel_data = defaultdict(lambda: defaultdict(lambda: 0))

        for fuel_data in fuels_data:
            mapped_fuel_data[fuel_data['vehicle_id'][0]][fuel_data['active']] = fuel_data['__count']

        for vehicle in self:
            vehicle.fuel_count = mapped_fuel_data[vehicle.id][vehicle.active]

    def return_action_to_open_fuel(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window']._for_xml_id('anem_fleet.%s' % xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id, group_by=False),
                domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False

    def open_assignation_logs(self):
        action = super().open_assignation_logs()
        action['views'] = [[self.env.ref('anem_fleet.fleet_vehicle_assignation_log_view_list_anem').id, 'tree']]
        return action
