# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict

from odoo import _, fields, models, api, tools, exceptions


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    odometer_anem = fields.Float(compute='_get_odometer', string='Last Odometer',
                                 help='Odometer measure of the vehicle at the moment of this log')

    photo = fields.Image(string="Image", max_width=600, max_height=400, help="La photo de la voiture")
    cgrise = fields.Image(string="cartegrise", max_width=640, max_height=800, help="Carte grise")
    affectation = fields.Image(string="affectation", max_width=640, max_height=800, help="Décision d'affectation")
    assurance = fields.Char('N° Police Assurance')

    vidange = fields.Float(string='Prochain Vidange', help="Prochain Vidange")
    vidange_count = fields.Float(string="Km jusqu'à vidange", compute='_compute_vidange_reste')
    alert_odometer = fields.Boolean(string='Alert Odometer', compute='_compute_alerts')

    controle_date = fields.Date(string='Contrôle technique')
    jours_reste = fields.Integer(string='Days Difference', compute='_compute_alerts')
    alert_controle = fields.Boolean(string='Alert Controle technique', compute='_compute_controle_reste')

    fuel_count = fields.Integer(compute="_compute_count_all", string='Fuel Count')
    service_count = fields.Integer(compute="_compute_count_all", string='Services')
    odometer_count = fields.Integer(compute="_compute_count_all", string='Odometer')
    history_count = fields.Integer(compute="_compute_count_all", string="Drivers History Count")
    contract_count = fields.Integer(compute="_compute_count_all", string='Contract Count')

    @api.depends('vidange', 'odometer', 'controle_date')
    def _compute_alerts(self):
        now = fields.Date.today()
        for record in self:
            record.vidange_count = (record.odometer - record.vidange) * -1 if record.vidange else 0
            record.alert_odometer = record.vidange and record.vidange_count < 2000
            record.jours_reste = (record.controle_date - now).days if record.controle_date else 0
            record.alert_controle = record.jours_reste < 7 and record.controle_date

            if record.alert_odometer or record.alert_controle:
                self._tag_alerts(record)

    def _tag_alerts(self, records):
        records.filtered(lambda r: r.alert_odometer and 15 not in r.tag_ids.ids).write({'tag_ids': [(4, 15)]})
        records.filtered(lambda r: r.alert_controle and 16 not in r.tag_ids.ids).write({'tag_ids': [(4, 16)]})

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
