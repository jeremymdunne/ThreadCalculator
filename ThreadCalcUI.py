from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
QApplication, QMainWindow, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,
QGridLayout, QLabel)

from ThreadCalculator import *
from threaddatReader import *
from materialdatReader import *

# import sys

class ThreadCalcUI(QMainWindow):
    def __init__(self, thread_data, material_data):
        super().__init__()
        print(material_data)
        self.setWindowTitle("Thread Calc V0.1")
        self.setFixedSize(400,300)

        # main layout

        thread_selection_widget = ThreadSelectionWidget(thread_data)
        self.setCentralWidget(thread_selection_widget)


        self.setCentralWidget(thread_selection_widget)

class ThreadCalculationWidget(QWidget):
    def __init__(self, thread_data):
        pass;

class ThreadSelectionWidget(QWidget):
    def __init__(self, thread_data, material_data):
        super().__init__()

        # variables
        self.thread_data = thread_data

        standard_label = QLabel("Standard")
        self.standard_combo = QComboBox()
        external_thread_label = QLabel("External Thread")
        self.external_thread_widget = ThreadWidget(None, None)
        internal_thread_label = QLabel("Internal Thread")
        self.internal_thread_widget = ThreadWidget(None, None)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(standard_label)
        layout.addWidget(self.standard_combo)
        layout.addWidget(external_thread_label)
        layout.addWidget(self.external_thread_widget)
        layout.addWidget(internal_thread_label)
        layout.addWidget(self.internal_thread_widget)

    def onStandardChange(self):
        # get the new standard
        standard = self.standard_combo.currentText()
        screw_info = []
        # find the thread data with the standard




class ThreadWidget(QWidget):
    def __init__(self, thread_data, material_data):
        super().__init__()

        # boxes & labels
        screw_size_label = QLabel("Screw Size")
        self.screw_size_combo = QComboBox()
        threads_per_inch_label = QLabel("Threads Per Inch")
        self.threads_per_inch_combo = QComboBox()
        thread_class_label = QLabel("Thread Class")
        self.thread_class_combo = QComboBox()
        material_label = QLabel("Material")
        self.material_combo = QComboBox()

        self.thread_data = thread_data
        self.material_data = material_data


        # layout
        layout = QGridLayout()
        self.setLayout(layout)
        # labels
        layout.addWidget(screw_size_label, 0, 0)
        layout.addWidget(threads_per_inch_label, 0, 1)
        layout.addWidget(thread_class_label, 0, 2)
        layout.addWidget(material_label, 0, 3)
        # combos
        layout.addWidget(self.screw_size_combo, 1, 0)
        layout.addWidget(self.threads_per_inch_combo, 1, 1)
        layout.addWidget(self.thread_class_combo, 1, 2)
        layout.addWidget(self.material_combo, 1, 3)

    def setThreadOptions(self, dict):
        screw_sizes = None
        threads_per_inch_options = []
        thread_class_options = []

        for a in dict:
            if a['screw_size'] not in screw_sizes:
                screw_size


    def setScrewSizeOptions(self,sizes):
        self.screw_size_combo.clear()
        self.screw_size_combo.addItems(sizes)

    def setThreadsPerInchOptions(self,tpi):
        self.threads_per_inch_combo.clear()
        self.threads_per_inch_combo.addItems(tpi)

    def setThreadClassOptions(self, classes):
        self.thread_class_combo.clear()
        self.thread_class_combo.addItems(classes)

    def setMaterialsOptions(self, materials):
        self.material_combo.clear()
        self.material_combo.addItems(materials)

    def getValues(self):
        dict = {}
        dict['screw_size'] = self.screw_size_combo.currentText()
        dict['threads_per_inch'] = self.threads_per_inch_combo.currentText()
        dict['thread_class'] = self.thread_class_combo.currentText()
        dict['material'] = self.material_combo.currentText()
        return dict


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
    app = QApplication([])

    window = ThreadCalcUI(threads, materials)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
