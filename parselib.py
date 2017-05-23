import numpy as np


class Matrix(object):
    def __init__(self, model=None):
        if model is None:
            self.model = self
        else:
            self.model = model
        model = self.model
        self.mtx = None
        model.header_lines = []
        model.aof = None
        model.term_vel = None
        model.burst_height = None
        model.cls_range, model.cls_defl = None, None
        model.offset_range, model.offset_defl = None, None
        model.gridlines_range, model.gridlines_defl = None, None
        model.gridlines_range_mid, model.gridlines_defl_mid = None, None
        model.cell_size_range, model.cell_size_defl = None, None
        model.pks = None

    def read(self, mtx_file):
        """
        Reads matrix file data.

        :param mtx_file: Matrix filename.
        :return: None
        """
        model = self.model

        def read_line(file_obj):
            ln = file_obj.readline()
            model.header_lines.append(ln.strip())
            return ln

        with open(mtx_file) as self.mtx:
            while 1:
                line = read_line(self.mtx)
                if not line:
                    raise IOError('Error in matrix file parsing')
                elif 'ANGLE_OF_FALL:' in line:
                    model.aof = float(line.split(':')[1].strip())
                elif 'TERMINAL_VELOCITY:' in line:
                    model.term_vel = float(line.split(':')[1].strip())
                elif 'BURST_HEIGHT:' in line:
                    model.burst_height = float(line.split(':')[1].strip())
                elif line.startswith('<MATRIX DIMENSIONS'):
                    break
            line = read_line(self.mtx)
            tokens = line.split(',')
            model.cls_range, model.cls_defl = int(tokens[0]), int(tokens[1])
            read_line(self.mtx)  # skip <matrix offset coordinate> header
            line = read_line(self.mtx).strip()
            tokens = line.split(',')
            model.offset_range, model.offset_defl = float(tokens[0]), float(tokens[1])
            read_line(self.mtx)  # skip <matrix gridlines range> header
            line = read_line(self.mtx).strip()
            model.gridlines_range = [float(x) for x in line.split()]
            read_line(self.mtx)  # skip <matrix gridlines deflection> header
            line = read_line(self.mtx).strip()
            model.gridlines_defl = [float(x) for x in line.split()]
            read_line(self.mtx)  # skip <matrix pks> header
            model.pks = np.zeros((model.cls_range, model.cls_defl))
            for r in range(model.cls_range):
                line = self.mtx.readline().strip()
                tokens = line.split()
                for d in range(model.cls_defl):
                    model.pks[r, d] = float(tokens[d])
