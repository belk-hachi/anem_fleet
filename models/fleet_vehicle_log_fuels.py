from odoo import api, fields, models


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

    bon = fields.Char('N° de bon')
