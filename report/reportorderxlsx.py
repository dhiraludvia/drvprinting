from odoo import models, fields, api

class ReportOrder(models.AbstractModel):
    _name = 'report.drvprinting.reportorderxlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Order'

    def generate_xlsx_report(self, workbook, data, order):
        sheet = workbook.add_worksheet('Daftar Purchase Order')
        bold_format = workbook.add_format({'bold': True})
        row = 1
        col = 0
        # sheet.write(row,col,'Nama Order',bold_format)
        sheet.write(row+1,col,'Tanggal Pesan',bold_format)
        # sheet.write(row+2,col,'Detail Order Stationary',bold_format)
        # sheet.write(row+3,col,'Detail Order Printing',bold_format)
        sheet.write(row+3,col,'Jumlah Order',bold_format)
        sheet.write(row+3,col,'Total Tagihan',bold_format)
        for obj in order:
            row = 1
            col += 1
            # sheet.write(row,col,obj.order_id)
            sheet.write(row+1,col,obj.tanggal_pesan)
            # sheet.write(row+2,col,obj.detailorder_ids)
            # sheet.write(row+3,col,obj.detailorder2_ids)
            sheet.write(row+3,col,obj.jumlah_pesanan)
            sheet.write(row+3,col,obj.total_tagihan)