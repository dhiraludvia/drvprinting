from odoo import models, fields, api

class ReportPenjualanWz(models.TransientModel):
    _name = 'printing.reportorderwz'
    _description = 'Report Order Wizard'

    dari_tgl = fields.Date(string='Dari Tanggal', required=True)
    ke_tgl = fields.Date(string='Ke Tanggal', required=True)
    penjualan_id = fields.Many2one(comodel_name='printing.order', string='Order')

    def action_order_report(self):
        laporan = []
        dari = self.dari_tgl
        ke = self.ke_tgl
        if dari:
            laporan += [('tanggal_transaksi','>=',dari)]
        if ke:
            laporan += [('tanggal_transaksi','<=',ke)]
        laporan_jadi = self.env['printing.order'].search_read(laporan)

        data = {
            'form' : self.read(0),
            'laporannya' : laporan_jadi
        }
        report_action = self.env.ref('printing.report_order_wizard').report_action(self, data=data)
        report_action['close_on_report_download'] = True
        return report_action
    
    