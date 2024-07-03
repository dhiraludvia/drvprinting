from odoo import fields, models, api, _

class Order(models.Model):
    _name = 'printing.order'
    _description = 'Daftar Order DRV Printing'
    _rec_name = "order_id"
    
    ref = fields.Char(string='No. Referensi', required=True,
                          readonly=True, default=lambda self: _('New'))
    
    user_id = fields.Many2one('res.users', string='Kasir', readonly=True, default=lambda self: self.env.user)
    
    member = fields.Boolean(string='Apakah member ?', required=True)
    
    order_id = fields.Many2one('res.partner', 
                               string='Nama Member',
                               domain="[('is_member','ilike',True)]")
    
    name = fields.Many2one('res.partner', 
                               string='Nama Customer',
                               domain="['&',('is_customernya','ilike',True),('is_member','ilike',False)]")
    
    # name = fields.Char(string='Nama Customer')

    tanggal_pesan = fields.Datetime(
        string='Tanggal Pesanan',
        default=fields.Datetime.now, 
        required=True)
        
    is_atk = fields.Boolean('Stationary')

    is_banner = fields.Boolean('Banner')

    is_stiker = fields.Boolean('Stiker')

    detailorder_ids = fields.One2many(
        comodel_name='printing.detailorderatk', 
        inverse_name='orderatk_id', 
        string='Detail Order Stationary')
    
    detailorder2_ids = fields.One2many(
        comodel_name='printing.detailorderprint', 
        inverse_name='orderprinting_id', 
        string='Detail Order Printing Banner')
    
    detailorder3_ids = fields.One2many(
        comodel_name='printing.detailorderstiker', 
        inverse_name='orderstiker_id', 
        string='Detail Order Printing Stiker')
  
    jumlah_pesanan = fields.Char(
        compute='_compute_jumlah_pesanan', 
        string='Jumlah Order')
    
    state = fields.Selection([
        ('draft', 'draft'),
        ('confirm', 'confirm'),
        ('done', 'done'),
        ('cancel', 'cancel'),
    ], string='state',
    readonly=True, default="draft")

    def action_confirm(self):
        self.write({'state':'confirm'})

    def action_done(self):
        self.write({'state':'done'})

    def action_cancel(self):
        self.write({'state':'cancel'})
    
    def action_draft(self):
        self.write({'state':'draft'})
    
    @api.depends('detailorder_ids','detailorder2_ids')
    def _compute_jumlah_pesanan(self):
        for record in self:
            record.jumlah_pesanan += (len(record.detailorder_ids)+len(record.detailorder2_ids)+len(record.detailorder3_ids))

    total_tagihan = fields.Integer(
        compute='_compute_total_tagihan', 
        string='Total Tagihan')
    
    @api.model
    def _compute_total_tagihan(self):
        for record in self:
            total1 = sum(self.env['printing.detailorderatk'].search([('orderatk_id','=',record.id)]).mapped('jumlah_harga'))
            total2 = sum(self.env['printing.detailorderprint'].search([('orderprinting_id','=',record.id)]).mapped('jumlah_harga_banner'))
            total3 = sum(self.env['printing.detailorderstiker'].search([('orderstiker_id','=',record.id)]).mapped('jumlah_harga_stiker'))
            record.total_tagihan = total1 + total2 + total3

    total_tagihan_pivot = fields.Integer(compute='_compute_total_tagihan_pivot', string='Total Tagihan')
    
    @api.depends('total_tagihan')
    def _compute_total_tagihan_pivot(self):
        for record in self:
            record.total_tagihan_pivot = record.total_tagihan
    
    @api.model
    def create(self, vals):
        if vals.get('ref', _("New")) == _("New"):
            member = vals.get('member', False)
            if member == True:
                vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.ordermember') or _("New")
            else:
                vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.ordernonmember') or _("New")
        record = super(Order, self).create(vals)
        return record


class DetailOrderStationary(models.Model):
    _name = 'printing.detailorderatk'
    _description = 'Detail Order Stationary'

    orderatk_id = fields.Many2one(
        comodel_name='printing.order', 
        string='Order Stationary')

    name_atk = fields.Many2one(
        comodel_name='printing.jenisbarang', 
        string='Nama Stationary')

    harga_atk = fields.Integer(
        compute='_compute_harga_atk', 
        string='Harga Barang')
    
    @api.depends('name_atk')
    def _compute_harga_atk(self):
        for record in self:
            record.harga_atk = record.name_atk.harga_atk
        
    banyaknya_atk = fields.Integer(string='Banyaknya')

    jumlah_harga = fields.Integer(
        compute='_compute_jumlah_harga', 
        string='Jumlah Harga Stationary')
    
    @api.depends('banyaknya_atk')
    def _compute_jumlah_harga(self):
        for record in self:
            record.jumlah_harga = record.harga_atk * record.banyaknya_atk 

    

class DetailOrderPrinting(models.Model):
    _name = 'printing.detailorderprint'
    _description = 'Detail Order Printing Banner'

    orderprinting_id = fields.Many2one(
        comodel_name='printing.order', 
        string='Order Printing')

    name_print = fields.Many2one(
        comodel_name='printing.jenisprint', 
        string='Nama Printing')
    
    banyaknya_print = fields.Integer(string='Qty')

    panjang = fields.Integer(
        string='P',
        required=True)
    
    lebar = fields.Integer(
        string='L',
        required=True)

    harga_print = fields.Integer(
        compute='_compute_harga_print', 
        string='Harga Cetak')

    jumlah_harga_banner = fields.Integer(
        compute='_compute_jumlah_harga_banner', 
        string='Jumlah Harga Printing Banner')


    @api.depends('name_print')
    def _compute_harga_print(self):
        for record in self:
            record.harga_print = record.name_print.harga_print 
            
    @api.depends('harga_print','banyaknya_print','panjang','lebar')
    def _compute_jumlah_harga_banner(self):
        for record in self:
            record.jumlah_harga_banner = record.harga_print * record.banyaknya_print * record.panjang * record.lebar



class DetailOrderPrintingStiker(models.Model):
    _name = 'printing.detailorderstiker'
    _description = 'Detail Order Printing Stiker'

    orderstiker_id = fields.Many2one(
        comodel_name='printing.order', 
        string='Order Stiker')

    name_stiker = fields.Many2one(
        comodel_name='printing.jenisprint', 
        string='Nama Stiker')
    
    banyaknya_stiker = fields.Integer(string='Qty')

    harga_stiker = fields.Integer(
        compute='_compute_harga_stiker', 
        string='Harga Cetak Stiker')
    
    jumlah_harga_stiker = fields.Integer(
        compute='_compute_jumlah_harga_stiker', 
        string='Jumlah Harga Printing Stiker')

    @api.depends('name_stiker')
    def _compute_harga_stiker(self):
        for record in self:
            record.harga_stiker = record.name_stiker.harga_print 
            
    @api.depends('harga_stiker','banyaknya_stiker')
    def _compute_jumlah_harga_stiker(self):
        for record in self:
            record.jumlah_harga_stiker = record.harga_stiker * record.banyaknya_stiker