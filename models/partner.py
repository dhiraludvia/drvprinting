from odoo import models, fields, api

class karyawan(models.Model):
    _inherit = 'hr.employee'
    
    is_pegawainya = fields.Boolean(string='Pegawai', 
                                   default=False)


class customer(models.Model):
    _inherit = 'res.partner'

    is_customernya = fields.Boolean(string='Customer', 
                                    default=False) 

    is_member = fields.Boolean(string='Member ?',
                           default=False)
