{
    'name': 'Advanced Product Filter',
    'version': '1.0',
    'author':'ANFEPI: Roberto Requejo Fernández',
    'depends': ['base','product', 'bias_custom_cosal'],
    'description': """
Advanced Product Filter for Cosal
=================================
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/advanced_product_filter_wiew.xml',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    "license": "AGPL-3",
}