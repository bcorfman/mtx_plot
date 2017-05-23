import os
from ConfigParser import SafeConfigParser

__author__ = 'brandon.corfman'


class IniParser(object):
    def __init__(self, dlg):
        self.dlg = dlg
        self.input_dir = None
        self.output_dir = None
        self.x, self.y, self.width, self.height = None, None, None, None
        self.case = None
        self.term_cond_option = None
        self.parser = SafeConfigParser()

    def read_ini_file(self):
        ini_path = os.path.abspath(os.curdir) + os.sep + 'mtxplot.ini'
        if os.path.exists(ini_path):
            self.parser.read(ini_path)
            self.input_dir = self.parser.get('settings', 'input_directory')
            if not os.path.exists(self.input_dir):
                self.input_dir = os.path.abspath(os.curdir)
            self.output_dir = self.parser.get('settings', 'output_directory')
            if not os.path.exists(self.output_dir):
                self.output_dir = os.path.abspath(os.curdir)
            geometry = self.parser.get('settings', 'geometry').split(',')
            self.x, self.y = int(geometry[0]), int(geometry[1])
            self.width, self.height = int(geometry[2]), int(geometry[3])
            self.case = self.parser.get('settings', 'case')
            self.term_cond_option = self.parser.get('settings', 'terminal_conditions_option')
        else:
            self.input_dir = os.path.abspath(os.curdir)
            self.output_dir = os.path.abspath(os.curdir)
            self.write_ini_file()
            if os.path.exists(ini_path):
                self.read_ini_file()

    def write_ini_file(self):
        ini_path = os.path.abspath(os.curdir) + os.sep + 'mtxplot.ini'
        if not self.parser.has_section('settings'):
            self.parser.add_section('settings')
        self.parser.set('settings', 'input_directory', self.input_dir)
        self.parser.set('settings', 'output_directory', self.output_dir)
        rect = self.dlg.geometry()
        self.x, self.y, self.width, self.height = rect.x(), rect.y(), rect.width(), rect.height()
        self.parser.set('settings', 'geometry', '{0},{1},{2},{3}'.format(self.x, self.y, self.width, self.height))
        self.case = self.dlg.lstCase.currentItem().text() if self.dlg.lstCase.currentItem() else ''
        self.parser.set('settings', 'case', self.case)
        self.term_cond_option = 'spreadsheets' if self.dlg.rdoSpreadsheets.isChecked() else 'worksheets'
        self.parser.set('settings', 'terminal_conditions_option', self.term_cond_option)
        with open(ini_path, 'w') as f:
            self.parser.write(f)
