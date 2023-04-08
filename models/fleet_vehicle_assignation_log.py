from odoo import fields, models


class FleetVehicleAssignationLog(models.Model):
    _inherit = 'fleet.vehicle.assignation.log'

    driver_id = fields.Many2one('res.partner', string="Driver", required=True)

    driver_employee_id = fields.Many2one('hr.employee', string='Driver (Employee)',
                                         compute='_compute_driver_employee_id', store=True, readonly=False)

    note = fields.Char(help='Description')

    company_id = fields.Integer(compute="_compute_company_id", string='Company', store=True)

    def _compute_company_id(self):

        print("ALLAH AKBAR")
