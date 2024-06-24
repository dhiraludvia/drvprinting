# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class stationary(models.Model):
    _name = 'printing.jenisbarang'
    _description = 'Daftar Barang Stationary'

    name = fields.Char(
        string='Nama Stationary',
        required=True)
    
    harga_atk = fields.Integer(
        string='Harga Barang',
        required=True)

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
        )
    
    @api.onchange('satuan')
    def _onchange_satuan(self):
        if self.satuan == 'pcs':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Harus COD A / JNE'
                }
            }
        elif self.satuan == 'pack':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Harus JNT'
                }
            }
        elif self.satuan == 'box':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Harus COD B '
                }
            }
        
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            name = self.env['printing.jenisbarang'].search([('name','=',record.name), ('id', '!=', record.id)])
            if (name)  :
                raise ValidationError('%s sudah ada di daftar !' % (str(record.name).upper()))

    