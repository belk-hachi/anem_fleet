from odoo import api, fields, models


class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    state = fields.Selection([
        ('new', 'New'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='done', string='Stage', group_expand='_expand_states')

    vendor = fields.Char('Fournisseur')
    facture = fields.Char('N° Facture')


