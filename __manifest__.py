{
    'name': "ANEM Voiture",
    'version': '1.0',
    'website': 'https://www.anem.dz',
    'description': "Un module customisé pour la gestion flotte de l'agence national de l'emploi -ANEM-",
    'depends': ['hr_fleet', 'fleet', 'web'],
    'author': "B.Hachi",
    'category': 'Human Resources',
    'data': [
        'security/ir.model.access.csv',
        'security/fleet_security.xml',
        'views/fleet_vehicle_views.xml',
        'views/fleet_vehicle_fuels_views.xml',
        'views/fleet_vehicle_services_views.xml',
        'views/fleet_vehicle_services_operation_views.xml',
        'views/login_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
