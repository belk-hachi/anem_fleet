from odoo import fields, models, api


class FleetVehicleLogServicesOperation(models.Model):
    _name = 'fleet.vehicle.log.services.operation'
    _description = 'Les opération utilisées '
    _rec_name = 'operation'
    _sql_constraints = [('operation', 'unique(operation)', "Opération deja exist")]

    operation = fields.Char(string="Nature de l'opération", required=True)
    sequence = fields.Integer()


class FleetVehicleLogServicesLines(models.Model):
    _name = 'fleet.vehicle.log.services.lines'
    _description = 'Les prix'

    service_id = fields.Many2one('fleet.vehicle.log.services', string='Interventions ID')
    operation_id = fields.Many2one('fleet.vehicle.log.services.operation', string="Nature de l'opération")
    qty = fields.Integer(string="Quantité", default=1)
    currency_id = fields.Many2one("res.currency", string="currency", required=True)
    operation_price = fields.Monetary(string='Montant' , currency_field="currency_id")
    total_amount = fields.Monetary(string='Montant', compute="_count_total_amount" , currency_field="currency_id")

    @api.depends('qty')
    def _count_total_amount(self):
        for record in self:
            record.total_amount = record.operation_price * record.qty
