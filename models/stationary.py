# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class stationary(models.Model):
    _name = 'printing.jenisbarang'
    _description = 'Daftar Barang Stationary'

    atk_id = fields.Many2one('res.users', string='PIC Stationary', readonly=True, default=lambda self: self.env.user)
    
    name = fields.Char(
        string='Nama Stationary',
        required=True)
    
    harga_atk = fields.Integer(
        string='Harga Barang',
        required=True)

    stok = fields.Integer(string='Jumlah Stok')

    satuan = fields.Selection(
        string='Satuan',
        selection=[("pcs","Pcs"),("pack","Pack"), ("box","Box")],
        required=True)
    
    ket_atk = fields.Char(
        string='Detail Stationary',
        required=True)

    active = fields.Boolean(string='Active',
                             default=True)

    jeniskirim_id = fields.Many2one('printing.jeniskirim', 
                                    string='Teknik Pengiriman', 
                                    required=True)

    pegawaistationary_id = fields.Many2one(
        comodel_name='hr.employee', 
        string='PIC Stationary',
        domain="[('is_pegawainya','ilike',True)]")
    
    @api.onchange('satuan')
    def _onchange_satuan(self):
        if self.satuan == 'pcs':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Kecuali COD'
                }
            }
        elif self.satuan == 'pack':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Kecuali JNT'
                }
            }
        elif self.satuan == 'box':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Harus Pick Up / JNE'
                }
            }
        
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            name = self.env['printing.jenisbarang'].search([('name','=',record.name), ('id', '!=', record.id)])
            if (name)  :
                raise ValidationError('%s sudah ada di daftar !' % (str(record.name).upper()))

    