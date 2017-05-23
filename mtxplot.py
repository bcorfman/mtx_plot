import sys
import os
import logging
from PySide import QtGui, QtCore
from paramcontroller import ParamController
from uiloader import load_ui_widget
from inifile import IniParser

if __name__ == '__main__':
    logging.basicConfig(filename='mtxplot.log', filemode='w', level=logging.ERROR)
    logging.debug('Running in ' + os.getcwd() + '.\n')
    try:
        app = QtGui.QApplication(sys.argv)
    except RuntimeError:
        app = QtCore.QCoreApplication.instance(sys.argv)
    param_dlg = load_ui_widget('paramdlg.ui')
    geo = param_dlg.frameGeometry()
    height, width = geo.height(), geo.width()
    x, y = geo.x(), geo.y()
    desktop = app.desktop()
    desk_rect = desktop.screenGeometry(desktop.screenNumber(QtGui.QCursor.pos()))
    screen_height, screen_width = desk_rect.height(), desk_rect.width()
    param_dlg.setGeometry((screen_width - width) / 2 + desk_rect.left(),
                          (screen_height - height) / 2 + desk_rect.top(), width, height)
    ini_parser = IniParser(param_dlg)
    ini_parser.read_ini_file()
    param_dlg.setGeometry(ini_parser.x, ini_parser.y, ini_parser.width, ini_parser.height)
    mtx_files = [x for x in os.listdir(ini_parser.input_dir) if x.endswith('.mtx')]
    param_dlg_ctlr = ParamController(param_dlg, ini_parser, mtx_files)

    param_dlg.lstCase.clicked.connect(param_dlg_ctlr.on_case_item_clicked)
    param_dlg.btnChooseInputDir.clicked.connect(param_dlg_ctlr.on_btn_choose_input_dir)
    param_dlg.btnChooseOutputDir.clicked.connect(param_dlg_ctlr.on_btn_choose_output_dir)
    param_dlg.btnMakePlot.clicked.connect(param_dlg_ctlr.on_btn_make_plot)
    app.aboutToQuit.connect(param_dlg_ctlr.about_to_quit)
    param_dlg.show()
    app.exec_()
