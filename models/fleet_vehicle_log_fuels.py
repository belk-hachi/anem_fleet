from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FleetVehicleLogfuels(models.Model):
    _inherit = 'fleet.vehicle.log.services'
    _name = 'fleet.vehicle.log.fuels'
    _description = 'fuels for vehicles'


    service_type_id = fields.Many2one(
        'fleet.service.type', 'Service Type', required=False,
        default=lambda self: self.env.ref('fleet.type_service_service_7', raise_if_not_found=False),
    )

    payment_method = fields.Selection([
        ('carte_naftal', 'Carte NAFTAL'),
        ('bon_carburant', 'Bon de carburant'),
        ('espece', 'Espèce'),
        ('autre', 'Autre')
    ], default='carte_naftal', string='Moyen de paiement ')

    carburant_type = fields.Selection([
        ('essence', 'Essence'),
        ('gpl', 'GPL/C'),
        ('gasoil', 'Gasoil')
    ], default='essence', string='Type de carburant')

    bon = fields.Char('N° de bon')

    def _set_odometer(self):
        for record in self:
            if not record.odometer or record.odometer == 0:
                raise UserError(_('Emptying the odometer value of a vehicle is not allowed.'))
            check_existing = self.env['fleet.vehicle.odometer'].search(
                [('value', '=', record.odometer),
                 ('date', '=', record.date),
                 ('vehicle_id', '=', record.vehicle_id.id)], limit=1, order='value desc')
            if not check_existing:
                odometer = self.env['fleet.vehicle.odometer'].create({
                    'value': record.odometer,
                    'date': record.date or fields.Date.context_today(record),
                    'vehicle_id': record.vehicle_id.id,
                    'chauffeur_id': record.purchaser_id.id
                })
                self.odometer_id = odometer
            else:
                self.odometer_id = check_existing
