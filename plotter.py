from xlsxwriter import Workbook
from parselib import Matrix


class ExcelPlot:
    def __init__(self, mtx_files, out_file):
        self.mtx_files = mtx_files
        self.out_file = out_file

    def plot(self):
        with Workbook(self.out_file) as wb:
            for m in self.mtx_files:
                mtx = Matrix()
                mtx.read(m)
                worksheet_name = '{0} AOF, {1} fps TV, {2} ft BH'.format(int(mtx.aof), int(mtx.term_vel),
                                                                         int(mtx.burst_height))
                ws = wb.add_worksheet(worksheet_name)
                pk_row = 0
                for row, item in enumerate(mtx.header_lines):
                    ws.write(row, 0, item)
                    pk_row = row
                for d in range(mtx.cls_defl):
                    ws.write(pk_row + 1, d, mtx.gridlines_defl[d])
                    ws.write(pk_row + 2, d, mtx.gridlines_defl[d] + mtx.offset_defl)
                for r in range(mtx.cls_range):
                    ws.write(pk_row + r + 3, 0, mtx.gridlines_range[r])
                    ws.write(pk_row + r + 3, 1, mtx.gridlines_range[r] + mtx.offset_range)
                    for d in range(mtx.cls_defl):
                        ws.write(pk_row + r + 3, d + 2, mtx.pks[r, d])
                ws.conditional_format(pk_row + 3, 2, pk_row + mtx.cls_range + 3, mtx.cls_defl + 2,
                                      {'type': '3_color_scale', 'min_color': '#63BE7B', 'mid_color': '#F7B97B',
                                       'max_color': '#EF676A'})
