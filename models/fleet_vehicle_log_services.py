from odoo import api, fields, models, _
from odoo.exceptions import UserError


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

    def _set_odometer(self):
        for record in self:
            if not record.odometer:
                raise UserError(_('Emptying the odometer value of a vehicle is not allowed.'))
            odometer = self.env['fleet.vehicle.odometer'].create({
                'value': record.odometer,
                'date': record.date or fields.Date.context_today(record),
                'vehicle_id': record.vehicle_id.id,
                'chauffeur_id': record.purchaser_id.id
            })
            self.odometer_id = odometer

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
