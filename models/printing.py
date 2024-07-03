# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class cetak(models.Model):
    _name = 'printing.jeniscetak'
    _description = 'Daftar Teknik Cetak'
    
    print_id = fields.Many2one('res.users', string='PIC Print', readonly=True, default=lambda self: self.env.user)

    bahan = fields.Selection(
        string='Bahan yang Digunakan',
        selection=[("kertas","Kertas"),("stiker","Stiker"),("banner","Banner"), ("kain","Kain")],
        required=True)
    
    ukuran = fields.Char(
        string='Ukuran Printing')
    
    stok_bahanprinting = fields.Integer(
        string='Stok Bahan Printing',
        required=True)

    
    
class printing(models.Model):
    _name = 'printing.jenisprint'
    _description = 'Daftar Layanan Printing'
    _inherit = 'printing.jeniscetak'

    name = fields.Char(
        string='Nama Printing',
        required=True)
    
    harga_print = fields.Integer(
        string='Harga Printing',
        required=True)

    keterangan = fields.Char(
        string='Detail Printing',
        required=True)

    active = fields.Boolean(string='Active',
                             default=True)
                            
    kirim_id = fields.Many2one(
        'printing.jeniskirim', 
        string='Teknik Pengiriman',
        required=True)

    pegawaiprinting_id = fields.Many2one(
        comodel_name='hr.employee', 
        string='PIC Printing',
        domain="[('is_pegawainya','ilike',True)]")
    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            name = self.env['printing.jenisprint'].search([('name','=',record.name), ('id', '!=', record.id)])
            if (name)  :
                raise ValidationError('%s sudah ada di daftar !' % (str(record.name).upper()))

    @api.onchange('bahan')
    def _onchange_bahan(self):
        if self.bahan == 'kertas':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Kecuali COD'
                }
            }
        elif self.bahan == 'stiker':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Harus Pick Up'
                }
            }
        elif self.bahan == 'banner':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Kecuali JNT'
                }
            }
        
        elif self.bahan == 'kain':
            return {
                'warning' :{
                    'title' : 'DELIVERY',
                    'message' : 'Teknik Pengiriman Kecuali JNE'
                }
            }