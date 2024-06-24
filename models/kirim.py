# -*- coding: utf-8 -*-

from odoo import models, fields, api


class kirim(models.Model):
    _name = 'printing.jeniskirim'
    _description = 'Daftar Teknik Kirim'

    name = fields.Selection(
        [("COD A","COD A"),("COD B","COD B"),("JNE","JNE"),("JNT","JNT")], 
        string='Teknik Pengiriman',
        required=True)
    
    packaging = fields.Selection(
        [("plastik","Plastik"),("bubble wrap","Bubble wrap"),("kardus","Kardus")], 
        string='Teknik Pengemasan',
        required=True)
    
    berat = fields.Selection(
        [("kurang dari 5"," Kurang dari 5 kg"),("5-10","5-10 kg"),("lebih dari 15","Lebih dari 15 kg")], 
        string='Berat Pengemasan Max')
    
    wilayah = fields.Char(string='Jangkauan Wilayah Pengiriman')
    
    ket_kirim = fields.Char(
        string='Detail Delivery',
        required=True)

    active = fields.Boolean(string='Active',
                             default=True)
    
    teknikkirim_ids = fields.One2many('printing.jenisbarang', 
                                      'jeniskirim_id', 
                                      string='Data Teknik Pengiriman Stationary')

    teknikcetak_ids = fields.One2many('printing.jenisprint', 
                                      'kirim_id', 
                                      string='Data Teknik Pengiriman Printing')
    
    pegawai_id = fields.Many2one(
        comodel_name='hr.employee', 
        string='Nama Kurir',
        domain="[('is_pegawainya','ilike',True)]")
    
    
    