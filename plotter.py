from xlsxwriter import Workbook
from parselib import Matrix
from util import measure_between

MIN_CELL_WIDTH = 3
MIN_CELL_HEIGHT = 12
MUTED_RED = '#63BE7B'
MUTED_YELLOW = '#F7B97B'
MUTED_GREEN = '#EF676A'


class ExcelPlot:
    def __init__(self, mtx_files, out_file):
        self.mtx_files = mtx_files
        self.out_file = out_file

    def plot(self):
        with Workbook(self.out_file) as wb:
            format = wb.add_format({'font_size': 8, 'num_format': '0.00'})
            for m in self.mtx_files:
                mtx = Matrix()
                mtx.read(m)
                min_grid_width = min(measure_between(mtx.gridlines_defl))
                min_grid_height = min(measure_between(mtx.gridlines_range))
                worksheet_name = '{0} AOF, {1} fps TV, {2} ft BH'.format(int(mtx.aof), int(mtx.term_vel),
                                                                         int(mtx.burst_height))
                ws = wb.add_worksheet(worksheet_name)
                pk_row = 0
                for row, item in enumerate(mtx.header_lines):
                    ws.write(row, 0, item)
                    pk_row = row
                for d in range(mtx.cls_defl):
                    ws.write(pk_row + 1, d + 2, mtx.gridlines_defl[d])
                    ws.write(pk_row + 2, d + 2, mtx.gridlines_defl[d] + mtx.offset_defl)
                    grid_width = mtx.gridlines_defl[d + 1] - mtx.gridlines_defl[d]
                    ws.set_column(d + 2, d + 2, (grid_width * MIN_CELL_WIDTH) / min_grid_width)
                for r in range(mtx.cls_range):
                    grid_height = mtx.gridlines_range[r + 1] - mtx.gridlines_range[r]
                    ws.write(pk_row + r + 3, 0, mtx.gridlines_range[r])
                    ws.write(pk_row + r + 3, 1, mtx.gridlines_range[r] + mtx.offset_range)
                    ws.write(pk_row + r + 3, 0, mtx.gridlines_range[r])
                    ws.set_row(pk_row + r + 3, (grid_height * MIN_CELL_HEIGHT) / min_grid_height)
                    for d in range(mtx.cls_defl):
                        ws.write(pk_row + r + 3, d + 2, mtx.pks[r, d])
                ws.set_column(0, mtx.cls_defl + 2, 5, format)
                ws.conditional_format(pk_row + 3, 2, pk_row + mtx.cls_range + 3, mtx.cls_defl + 2,
                                      {'type': '3_color_scale',
                                       'min_color': MUTED_RED,
                                       'mid_color': MUTED_YELLOW,
                                       'max_color': MUTED_GREEN})
