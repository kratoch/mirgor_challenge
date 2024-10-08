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
        'views/sale_order_views.xml',
        'views/credit_group_views.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
    'application': True,
}
