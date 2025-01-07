# __manifest__.py
{
    'name': 'Mi Módulo',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Descripción corta de lo que hace el módulo',
    'depends': ['base'],
    'data': [
        'views/my_model_views.xml',
    ],
    'installable': True,
    'application': True,
}