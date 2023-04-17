from odoo import fields, models, api


class FleetVehicleAssignationLog(models.Model):
    _inherit = 'fleet.vehicle.assignation.log'

    driver_id = fields.Many2one('res.partner', string="Driver", required=True)

    driver_employee_id = fields.Many2one('hr.employee', string='Driver (Employee)',
                                         compute='_compute_driver_employee_id', store=True, readonly=False)

    note = fields.Char(help='Description')
    # i need to fix this and turn it to related field
    company_id = fields.Integer(compute="_compute_company_id", string='Company')

    # get the company_id from the vehicle for domain
    @api.depends("vehicle_id")
    def _compute_company_id(self):
        for record in self:
            record.company_id = record.vehicle_id.company_id
