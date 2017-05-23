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
                for r in range(mtx.cls_range):
                    for d in range(mtx.cls_defl):
                        ws.write(pk_row + r, d, mtx.pks[r, d])
                ws.conditional_format(pk_row, 0, pk_row + mtx.cls_range, mtx.cls_defl,  {'type': '3_color_scale',
                                                                                         'min_color': '#63BE7B',
                                                                                         'mid_color': '#F7B97B',
                                                                                         'max_color': '#EF676A'})
