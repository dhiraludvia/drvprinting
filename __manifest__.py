# -*- coding: utf-8 -*-
{
    'name': "DRV Printing",

    'summary': """
        Print, Art & Stationary""",

    'description': """
        Check out my shop if you want to print something unique and fulfill your work needs 
    """,

    'author': "dRV Corp",
    'website': "http://www.drvcorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base','hr','report_xlsx'],


    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/customer.xml',
        'views/kirim.xml',
        'views/order.xml',
        'views/karyawan.xml',
        'views/printing.xml',
        'views/stationary.xml',
        'views/templates.xml',
        'wizard/reportorderwz.xml',
        'report/report.xml',
        'report/report_order_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
