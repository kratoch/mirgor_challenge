{
    'name': 'Mirgor Challenge',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom Sale Channels',
    'author': 'Kratochvil Claudio',
    'depends': ['sale_management', 'stock', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_channel_views.xml',
    ],
    'installable': True,
    'application': True,
}
