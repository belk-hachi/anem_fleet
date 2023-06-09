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
    pieces_lines = fields.One2many('fleet.vehicle.log.services.lines', 'service_id', string="Opération")
    amount = fields.Monetary('Cost', compute="_count_services", inverse="_inverse_count_services", store=True)

    @api.depends('pieces_lines')
    def _count_services(self):
        for record in self:
            record.amount = 0
            for piece in record.pieces_lines:
                record.amount = record.amount + piece.total_amount

    def _inverse_count_services(self):
        for record in self:
            pass

    def action_extraire_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Intervention details',
            'res_model': 'fleet.vehicle.log.services.lines',
            'view_type': 'tree',
            'domain': [('service_id', 'in', self.mapped('id'))],
            'view_mode': 'tree',
            'target': 'current',
        }
