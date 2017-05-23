import os
import logging
from fnmatch import fnmatch
from PySide.QtGui import QFileDialog, QApplication
from PySide.QtCore import Qt
from textlabel import TextLabel
from plotter import ExcelPlot


class ParamController:
    def __init__(self, dlg, ini_parser, mtx_files):
        self.win = None
        self.ini_parser = ini_parser
        self.mtx_files = mtx_files
        self.dlg = dlg
        self.dlg.lblInputDir = TextLabel(self.dlg, objectName='lblInputDir')
        self.dlg.lblInputDir.setText('Input directory: ' + ini_parser.input_dir)
        self.dlg.lblInputDir.setGeometry(30, 20, 251, 16)
        self.dlg.lblOutputDir = TextLabel(self.dlg, objectName='lblOutputDir')
        self.dlg.lblOutputDir.setText('Output directory: ' + ini_parser.output_dir)
        self.dlg.lblOutputDir.setGeometry(30, 60, 251, 16)
        choose_btn = self.dlg.lblLayout.itemAt(0).widget()
        self.dlg.lblLayout.removeWidget(choose_btn)
        self.dlg.lblLayout.addWidget(self.dlg.lblInputDir)
        self.dlg.lblLayout.addWidget(choose_btn)
        self.dlg.frameInputDir.setLayout(self.dlg.lblLayout)
        choose_btn = self.dlg.lblLayout_2.itemAt(0).widget()
        self.dlg.lblLayout_2.removeWidget(choose_btn)
        self.dlg.lblLayout_2.addWidget(self.dlg.lblOutputDir)
        self.dlg.lblLayout_2.addWidget(choose_btn)
        self.dlg.frameOutputDir.setLayout(self.dlg.lblLayout_2)
        self._populate_list_box()
        if self.ini_parser.term_cond_option == 'worksheets':
            self.dlg.rdoWorksheets.setChecked(True)
            self.dlg.rdoSpreadsheets.setChecked(False)
        else:
            self.dlg.rdoWorksheets.setChecked(False)
            self.dlg.rdoSpreadsheets.setChecked(True)
        self.dlg.btnMakePlot.setEnabled(False)
        self.plotter = None
        self.model = None
        self.stop_events = False

    def _populate_list_box(self):
        cases = set((x.rsplit('-', 2)[0].rsplit('_', 2)[0] for x in self.mtx_files))
        self.dlg.lstCase.clear()
        if cases:
            self.dlg.lstCase.addItems(sorted(cases))

    # noinspection PyUnusedLocal
    def on_case_item_clicked(self, item):
        self.dlg.btnMakePlot.setEnabled(True)

    def on_btn_choose_input_dir(self):
        # noinspection PyTypeChecker
        d = QFileDialog.getExistingDirectory(None, 'Select Input Directory', self.ini_parser.input_dir,
                                             QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if d:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.dlg.lblInputDir.setText('Input directory: ' + d)
            self.ini_parser.input_dir = d
            self.ini_parser.write_ini_file()
            self.mtx_files = [os.path.splitext(x)[0] for x in os.listdir(d) if x.endswith('.mtx')]
            self._populate_list_box()
            self.dlg.btnMakePlot.setEnabled(False)
            QApplication.restoreOverrideCursor()

    def on_btn_choose_output_dir(self):
        # noinspection PyTypeChecker
        d = QFileDialog.getExistingDirectory(None, 'Select Output Directory', self.ini_parser.output_dir,
                                             QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if d:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.dlg.lblOutputDir.setText('Output directory: ' + d)
            self.ini_parser.output_dir = d
            self.ini_parser.write_ini_file()
            QApplication.restoreOverrideCursor()

    # noinspection PyUnusedLocal
    def on_btn_make_plot(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        for i in self.dlg.lstCase.selectedItems():
            if self.dlg.rdoWorksheets.isEnabled():
                try:
                    case = i.text()
                    excel_file = os.path.join(self.ini_parser.output_dir, case + '.xlsx')
                    plotter = ExcelPlot(self._get_files_in_case(case), excel_file)
                    plotter.plot()
                except Exception, e:
                    logging.error(e.message)
                    error = 'Error(s) occurred. Check mtxplot.log in output directory for details.'
                    self.dlg.lblErrorReport.setText(error)
            elif self.dlg.rdoSpreadsheets.isEnabled():
                case = i.text()
                for m in self._get_files_in_case(case):
                    try:
                        excel_file = os.path.join(self.ini_parser.output_dir, os.path.splitext(m)[0] + '.xlsx')
                        plotter = ExcelPlot([m], excel_file)
                        plotter.plot()
                    except Exception, e:
                        logging.error(e.message)
                        error = 'Error(s) occurred. Check mtxplot.log in output directory for details.'
                        self.dlg.lblErrorReport.setText(error)
        QApplication.restoreOverrideCursor()

    def about_to_quit(self):
        self.ini_parser.write_ini_file()

    def _get_files_in_case(self, case):
        prefix = case + '_'
        file_lst = [os.path.join(self.ini_parser.input_dir, f) for f in self.mtx_files if fnmatch(f, prefix + '*')]
        return file_lst
