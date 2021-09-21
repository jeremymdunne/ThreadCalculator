from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
QApplication, QMainWindow, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,
QGridLayout, QLabel)

from ThreadCalculator import *
from threaddatReader import *
from materialdatReader import *
from UI.ThreadMaterialSelectionWidget import *

# import sys

class ThreadCalcUI(QMainWindow):
    def __init__(self, thread_data, material_data):
        super().__init__()
        print(material_data)
        self.setWindowTitle("Thread Calc V0.1")
        self.setFixedSize(400,300)

        # main layout



        thread_selection_widget = ThreadMaterialSelectionWidget()
        self.setCentralWidget(thread_selection_widget)


        self.setCentralWidget(thread_selection_widget)
        self.sanitizeThreadData(thread_data)

    def sanitizeThreadData(self, thread_data):
        # organize the thread data
        new_thread_data = []
        for set in thread_data:
            data = []
            #entry = {
            #    'screw_size':None, 'possible_threads_per_inch' : [], 'possible_thread_class' : []
            #}
            for d in set['external_data']:
                # check if a new entry is desired
                found = False
                for e in data:
                    if e['screw_size'] == d['screw_size']:
                        # add
                        if d['threads_per_inch'] not in e['possible_threads_per_inch']:
                            e['possible_threads_per_inch'].append(d['threads_per_inch'])
                        if d['thread_class'] not in e['possible_thread_class']:
                            e['possible_thread_class'].append(d['thread_class'])
                        found = True
                        break
                if not found:
                    entry = {}
                    entry['screw_size'] = d['screw_size']
                    entry['possible_threads_per_inch'] = [d['threads_per_inch']]
                    entry['possible_thread_class'] = [d['thread_class']]
                    data.append(entry)
            new_thread_data.append(data)
        print(new_thread_data)


class ThreadCalculationWidget(QWidget):
    def __init__(self, thread_data):
        pass;


class oldThreadSelectionWidget(QWidget):
    def __init__(self, thread_data):
        super().__init__()

        # variable initilize
        self.standards = []
        self.standard_combo = None
        self.external_thread_combo = None
        self.internal_thread_combo = None
        self.thread_data = thread_data

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.standard_combo = QComboBox()
        self.external_thread_combo = QComboBox()
        self.internal_thread_combo = QComboBox()

        self.getStandards()
        self.populateCombosBoxes()

        layout.addWidget(self.standard_combo)
        layout.addWidget(self.external_thread_combo)
        layout.addWidget(self.internal_thread_combo)

        self.standard_combo.activated[str].connect(self.onStandardChange)

    def getStandards(self):
        for t in self.thread_data:
            if t['standard'] not in self.standards:
                self.standards.append(t['standard'])
        self.standard_combo.addItems(self.standards)

    def onStandardChange(self):
        self.external_thread_combo.clear()
        self.internal_thread_combo.clear()
        self.populateCombosBoxes()

    def populateCombosBoxes(self):
        # get a list of the standards
        # get the current standard
        current_standard = self.standard_combo.currentText()
        external = []
        internal = []
        for t in self.thread_data:
            if t['standard'] == current_standard:
                if t['type'] == 'external':
                    for e in t['data']:
                        external.append(e['screw_size'] + '-' + str(e['threads_per_inch']))
                elif t['type'] == 'internal':
                    for e in t['data']:
                        internal.append(e['screw_size'] + '-' + str(e['threads_per_inch']))
        self.external_thread_combo.addItems(external)
        self.internal_thread_combo.addItems(internal)


def main():
    # read in the threads
    threadFiles = getThreadDataFiles()
    materialFiles = getMaterialdatFiles()
    materials = []
    for m in materialFiles:
        materials += readMaterialdat(m)
    threads = []
    for f in threadFiles:
        threads.append(readThreaddat(f))
    print(threads)
    app = QApplication([])

    window = ThreadCalcUI(threads, materials)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
